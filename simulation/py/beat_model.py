"""Functional Python port of rtl/ecg_beat_detector.sv (v2, slope based), so that long recordings (hours of DaLiA ECG) can be
run without Verilog.  NOT bit-exact: the Verilog replay testbench's own sample timing shifts its reported indices by a few
samples, so the two lists never match index for index.  Checked by scoring both against the same beat annotations
(results/tweak_beat_model_vs_rtl.csv): agreement within 0.12 percentage points on 18 clean NSRDB recordings, within 2.8 points
in the heaviest NSTDB noise (-6 dB).
Optional `reject_early` is a PROPOSAL (tweak 5), Python only: not in the RTL."""
import numpy as np


def detect(ecg, FS=250, MIN_THR=1500, DECAY_SH=10, SLOPE_N=3, reject_early=None):
    """ecg: int array (16-bit codes at FS Hz).  Returns sample indices where the RTL would pulse `beat`.
    reject_early = (frac, big): PROPOSAL - a candidate arriving sooner than frac*(median of last 5 RR) after the last beat is
    ignored unless its slope exceeds big * threshold."""
    e = [int(v) for v in ecg]
    n = len(e)
    env = 0; rr_cnt = 0; refr = 0; have_prev = False
    h1 = h2 = h3 = 0
    refr_len = (FS * 3) // 10
    out = []; rr_hist = []
    for i in range(n):
        x = e[i]
        a = abs(x - h3)
        if a > 65535: a = 65535
        thr0 = (env >> 1) + (env >> 3)
        thr = MIN_THR if thr0 < MIN_THR else thr0
        # old-value semantics of the non-blocking assignments
        fire = (a > thr) and refr == 0
        if reject_early and fire and have_prev and len(rr_hist) >= 3:
            med = sorted(rr_hist[-5:])[len(rr_hist[-5:]) // 2]
            if rr_cnt < reject_early[0] * med and a <= reject_early[1] * thr:
                fire = False
        new_rr = rr_cnt + 1 if rr_cnt != 0xFFFF else rr_cnt
        new_refr = refr - 1 if refr != 0 else 0
        new_have = have_prev
        if rr_cnt > 2 * FS: new_have = False
        new_env = a if a > env else env - (env >> DECAY_SH)
        if fire:
            new_refr = refr_len
            if have_prev and rr_cnt >= refr_len:
                out.append(i)
                rr_hist.append(rr_cnt)
            new_rr = 0
            new_have = True
        env, rr_cnt, refr, have_prev = new_env, new_rr, new_refr, new_have
        h3, h2, h1 = h2, h1, x
    return np.array(out, dtype=np.int64)


class StreamDetector:
    """Same logic as detect(), but keeps its state between calls so that day-long records can be fed in chunks."""
    def __init__(self, FS=250, MIN_THR=1500, DECAY_SH=10):
        self.FS, self.MIN_THR, self.DECAY_SH = FS, MIN_THR, DECAY_SH
        self.env = 0; self.rr_cnt = 0; self.refr = 0; self.have_prev = False; self.h1 = self.h2 = self.h3 = 0; self.i = 0
        self.refr_len = (FS * 3) // 10

    def feed(self, ecg):
        out = []; FS = self.FS; env = self.env; rr_cnt = self.rr_cnt; refr = self.refr; have_prev = self.have_prev
        h1, h2, h3, i0 = self.h1, self.h2, self.h3, self.i; refr_len = self.refr_len; MIN_THR = self.MIN_THR; sh = self.DECAY_SH
        for k, v in enumerate(ecg):
            x = int(v); a = abs(x - h3)
            if a > 65535: a = 65535
            thr0 = (env >> 1) + (env >> 3); thr = MIN_THR if thr0 < MIN_THR else thr0
            fire = (a > thr) and refr == 0
            new_rr = rr_cnt + 1 if rr_cnt != 0xFFFF else rr_cnt
            new_refr = refr - 1 if refr != 0 else 0
            new_have = False if rr_cnt > 2 * FS else have_prev
            new_env = a if a > env else env - (env >> sh)
            if fire:
                new_refr = refr_len
                if have_prev and rr_cnt >= refr_len: out.append(i0 + k)
                new_rr = 0; new_have = True
            env, rr_cnt, refr, have_prev = new_env, new_rr, new_refr, new_have
            h3, h2, h1 = h2, h1, x
        self.env, self.rr_cnt, self.refr, self.have_prev, self.h1, self.h2, self.h3 = env, rr_cnt, refr, have_prev, h1, h2, h3
        self.i = i0 + len(ecg)
        return out
