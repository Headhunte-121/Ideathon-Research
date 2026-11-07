"""C7 prep: causal per-person baseline residuals (running median of previous 600 s, >=30 beats).  -> data/edge/edb_resid_<k>.npz"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E

def run_median(t, X, win=600.0, minhist=30):
    out = np.full(X.shape, np.nan, dtype=np.float32); ok = np.zeros(len(t), bool)
    for i in range(len(t)):
        lo = np.searchsorted(t, t[i] - win)
        if i - lo >= minhist: out[i] = np.median(X[lo:i], axis=0); ok[i] = True
    return out, ok

def one(a):
    k, ri = a; d = E.load_fold(k); m = np.where(d["rec"] == ri)[0]
    med, ok = run_median(d["t"][m], d["win"][m].astype(np.float32)); res = np.clip(d["win"][m].astype(np.float32) - np.round(med), -128, 127)
    fm, _ = run_median(d["t"][m], d["feat"][m].astype(np.float32))
    return k, m, np.nan_to_num(res).astype(np.int8), ok, d["feat"][m] - fm

if __name__ == "__main__":
    from multiprocessing import Pool
    jobs = []
    for k in range(5):
        d = E.load_fold(k); jobs += [(k, ri) for ri in np.unique(d["rec"])]
    with Pool(max(1, os.cpu_count() - 2)) as p: res = p.map(one, jobs, chunksize=1)
    for k in range(5):
        d = E.load_fold(k); n = len(d["t"]); rw = np.zeros((n, 75), np.int8); rok = np.zeros(n, bool); rf = np.zeros((n, 6), np.float32)
        for kk, m, r, ok, f in res:
            if kk == k: rw[m] = r; rok[m] = ok; rf[m] = f
        # history rule identical to R1's (>=30 eligible beats in previous 600 s): check
        print("history rule matches R1:", bool((rok == ~np.isnan(d["r1"])).all()))
        np.savez_compressed(f"data/edge/edb_resid_{k}.npz", resid=rw, hist_ok=rok, featres=rf); print(k, n, int(rok.sum()))
