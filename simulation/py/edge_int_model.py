"""Integer reference model of beatnet-tiny = the SPECIFICATION the Verilog (rtl_edge/rtl/edge_cnn_beat.sv) must match bit for bit.
Pure integer numpy.  Conventions (identical in Verilog):
  * conv: acc[co,p] = bias_q[co] + sum_{ci,j} x[ci, p*stride + j - pad_left] * w_q[co,ci,j]   (zero padding, int8 x int8 -> int32 accumulate)
  * requantise: y = (acc * M0[co] + (1 << (n[co]-1))) >> n[co]   (int64 product, ARITHMETIC shift = floor), then clamp to [0,127] (ReLU folded in)
  * global 'average' pooling keeps the SUM over 19 positions (no division; 1/19 folded into the final-layer scale)
  * fc: logit_j = bias_q[j] + sum_c gsum[c]*w_q[j,c]  (int32); score = logit_1 - logit_0 (int32)
Weight layout (flattened for ROM): w[co][ci][k] row-major."""
import numpy as np

SPEC = [("conv1", 1, 8, 7, 1, (3, 3), 75), ("conv2", 8, 16, 5, 2, (2, 2), 38), ("conv3", 16, 16, 3, 2, (0, 1), 19)]


def _conv_acc(x, w, b, stride, pad, lout):
    B, cin, L = x.shape; cout, _, k = w.shape
    xp = np.pad(x.astype(np.int64), ((0, 0), (0, 0), pad))
    idx = np.arange(lout)[:, None] * stride + np.arange(k)[None, :]
    cols = xp[:, :, idx]                                           # B, cin, lout, k
    cols = cols.transpose(0, 2, 1, 3).reshape(B, lout, cin * k)
    acc = cols @ w.reshape(cout, cin * k).T.astype(np.int64)       # B, lout, cout
    return acc.transpose(0, 2, 1) + b.astype(np.int64)[None, :, None]


def requant(acc, M0, n):
    M0 = np.asarray(M0, dtype=np.int64)[None, :, None]; n = np.asarray(n, dtype=np.int64)[None, :, None]
    y = (acc.astype(np.int64) * M0 + (np.int64(1) << (n - 1))) >> n
    return np.clip(y, 0, 127)


def forward_int_batch(win, P, debug=False):
    """win: (B,75) int8.  P: params dict (see c3_quantize).  Returns int64 scores (B,) [and dict of intermediates]."""
    x = np.asarray(win, dtype=np.int64)[:, None, :]; dbg = {"input": x.copy()}
    for name, cin, cout, k, s, pad, lo in SPEC:
        acc = _conv_acc(x, P[f"{name}_w"], P[f"{name}_b"], s, pad, lo)
        x = requant(acc, P[f"{name}_M0"], P[f"{name}_n"])
        if debug: dbg[f"{name}_acc"] = acc; dbg[f"{name}_out"] = x
        P.setdefault("_maxacc", {}); P["_maxacc"][name] = max(P["_maxacc"].get(name, 0), int(np.abs(acc).max()))
    g = x.sum(axis=2)                                              # B,16
    logit = g @ P["fc_w"].T.astype(np.int64) + P["fc_b"].astype(np.int64)[None, :]
    score = logit[:, 1] - logit[:, 0]
    if debug: dbg["gap_sum"] = g; dbg["logit"] = logit; return score, dbg
    return score


def forward_int(window_int8, P, debug=False):
    r = forward_int_batch(np.asarray(window_int8)[None, :], P, debug)
    return (r[0][0], {k: v[0] for k, v in r[1].items()}) if debug else int(r[0])
