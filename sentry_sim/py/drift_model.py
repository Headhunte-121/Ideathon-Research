"""Bit-exact Python replica of rtl/baseline_drift_detector.sv (used to diagnose and to try alternative features
WITHOUT touching the RTL).  `run_rtl_replica` must reproduce the Verilog flag counts / delays (checked in
py/analyze_drift.py); `run_variant` is a PROPOSAL (smoothed feature) and is Python-only, not RTL.

Feature units: heart rate in bpm*16 (Q12.4), one value per beat, like the RTL."""
import numpy as np


def run_rtl_replica(hr, K2X16, LOG2N=13, WIN=60, WIN_THR=30, CONSEC=5, CLEAN=2, VAR_FLOOR=256, ADAPT_SHIFT=10,
                    first_after=None, return_state=False, return_edges=False):
    """Returns (number of rising edges of drift_flag, index of first rising edge at/after `first_after` or -1)
    (+ the final drift_flag if return_state)."""
    N = 1 << LOG2N
    hr = [int(v) for v in hr]
    s = sq = 0
    for x in hr[:N]:
        s += x; sq += x * x
    if len(hr) <= N:
        return (0, -1, False) if return_state else (0, -1)
    mean = s >> LOG2N
    var = (sq >> LOG2N) - mean * mean
    wcnt = ecnt = consec = cleanw = 0
    flag = False; edges = 0; first = -1; edge_idx = []
    half = 1 << (ADAPT_SHIFT - 1) if ADAPT_SHIFT > 0 else 0
    for i in range(N, len(hr)):
        x = hr[i]
        d = x - mean; d2 = d * d
        vv = VAR_FLOOR if var < VAR_FLOOR else var
        exceed = (d2 * 16) > (K2X16 * vv)
        if ADAPT_SHIFT > 0 and not exceed:
            mean = mean + ((d + half) >> ADAPT_SHIFT)
            var = var + ((d2 - var + half) >> ADAPT_SHIFT)
        if wcnt == WIN - 1:
            tot = ecnt + (1 if exceed else 0)
            if tot >= WIN_THR:
                cleanw = 0; consec += 1
                if consec >= CONSEC and not flag:
                    flag = True; edges += 1; edge_idx.append(i)
                    if first_after is not None and i >= first_after and first < 0:
                        first = i - first_after
            else:
                consec = 0; cleanw += 1
                if cleanw >= CLEAN:
                    flag = False
            wcnt = 0; ecnt = 0
        else:
            wcnt += 1
            if exceed:
                ecnt += 1
    if return_edges: return edge_idx
    return (edges, first, flag) if return_state else (edges, first)


def inject(hr, pct):
    """Same step as tb_drift_false_alarms: +pct % over the last quarter of the beats."""
    hr = np.asarray(hr, dtype=np.int64).copy()
    at = len(hr) * 3 // 4
    hr[at:] = hr[at:] + (hr[at:] * pct) // 100
    return hr, at


def smooth_feature(hr, n):
    """PROPOSAL: replace each beat's heart rate by the mean of the last n beats (causal, one value per beat)."""
    hr = np.asarray(hr, dtype=np.float64)
    c = np.cumsum(np.insert(hr, 0, 0.0))
    out = np.empty(len(hr))
    for i in range(len(hr)):
        j = max(0, i - n + 1)
        out[i] = (c[i + 1] - c[j]) / (i + 1 - j)
    return np.round(out).astype(np.int64)
