"""C8 prep: causal per-person calibrations at several spans (median over previous S seconds, >=30 beats; current beat excluded; no labels).
 Hand features (6): median and MAD at S in 120,300,600,1800;  windows (75): median at S in 300,600,1800.  -> data/edge/c8_<fold>.npz"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E
FS_SPANS = [120, 300, 600, 1800]; WIN_SPANS = [300, 600, 1800]


def run_stats(t, X, span, mad=False, minhist=30):
    med = np.full(X.shape, np.nan, np.float32); md = np.full(X.shape, np.nan, np.float32)
    for i in range(len(t)):
        lo = np.searchsorted(t, t[i] - span)
        if i - lo >= minhist:
            h = X[lo:i]; m = np.median(h, axis=0); med[i] = m
            if mad: md[i] = np.median(np.abs(h - m), axis=0)
    return med, md


def one(a):
    k, ri = a; d = E.load_fold(k); m = np.where(d["rec"] == ri)[0]; t = d["t"][m]; f = d["feat"][m].astype(np.float32); w = d["win"][m].astype(np.float32); out = {"m": m}
    for s in FS_SPANS:
        med, md = run_stats(t, f, s, True); out[f"fmed{s}"] = med; out[f"fmad{s}"] = md
    for s in WIN_SPANS:
        med, _ = run_stats(t, w, s); out[f"wmed{s}"] = med
    return k, out


if __name__ == "__main__":
    from multiprocessing import Pool
    jobs = []
    for k in range(5):
        d = E.load_fold(k); jobs += [(k, ri) for ri in np.unique(d["rec"])]
    with Pool(max(1, os.cpu_count() - 2)) as p: res = p.map(one, jobs, chunksize=1)
    for k in range(5):
        n = len(E.load_fold(k)["t"]); store = {f"fmed{s}": np.full((n, 6), np.nan, np.float32) for s in FS_SPANS}
        store.update({f"fmad{s}": np.full((n, 6), np.nan, np.float32) for s in FS_SPANS}); store.update({f"wmed{s}": np.full((n, 75), np.nan, np.float32) for s in WIN_SPANS})
        for kk, o in res:
            if kk == k:
                for key in store: store[key][o["m"]] = o[key]
        np.savez_compressed(f"data/edge/c8_{k}.npz", **{kk: v.astype(np.float16 if kk.startswith("wmed") else np.float32) for kk, v in store.items()}); print("fold", k, "done")
