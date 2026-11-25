"""C8 random search (tabular families).  python py/c8_search.py <n_configs> [workers]   Appends to results/c8_search_log.csv as jobs finish.
Each job = (config, outer fold): fit on the train folds, evaluate on inner validation AND test (both logged; selection later uses validation only)."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import sys, json, time, csv
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
FSETS = ["H", "HC", "HCz", "H+HC", "W", "WR", "WR+HC", "H+WR", "HCz+WR"]
MM = "data/edge/c8mm"; _CACHE = {}


def make_cache():
    import edge_nets as E
    os.makedirs(MM, exist_ok=True)
    for k in range(5):
        if os.path.exists(f"{MM}/{k}_t.npy"): continue
        d = E.load_fold(k); z = np.load(f"data/edge/c8_{k}.npz")
        for key in ("win", "feat", "t", "label", "ok", "rec", "subject"): np.save(f"{MM}/{k}_{key}.npy", d[key])
        for key in z.files: np.save(f"{MM}/{k}_{key}.npy", z[key])
        rec = d["rec"]; start = np.zeros(len(rec), np.int64); chg = np.where(np.diff(rec) != 0)[0] + 1; b = np.zeros(len(rec), bool); b[np.concatenate([[0], chg])] = True
        start = np.maximum.accumulate(np.where(b, np.arange(len(rec)), 0)); np.save(f"{MM}/{k}_start.npy", start)


def arr(k, key):
    if (k, key) not in _CACHE: _CACHE[(k, key)] = np.load(f"{MM}/{k}_{key}.npy", mmap_mode="r")
    return _CACHE[(k, key)]


def sample_config(i):
    r = np.random.default_rng(8000 + i); c = dict(id=i, fset=str(r.choice(FSETS)), span_f=int(r.choice([120, 300, 600, 1800])), span_w=int(r.choice([300, 600, 1800])),
                                                  smooth=int(r.choice([1, 5, 15, 30])), n_train=int(r.choice([5000, 20000])), model=str(r.choice(["lr", "hgb", "hgb", "mlp"])))
    if c["model"] == "lr": c.update(C=float(r.choice([0.01, 0.1, 1, 10])))
    elif c["model"] == "hgb": c.update(max_depth=int(r.choice([2, 3, 4, 6])), lr=float(r.choice([0.03, 0.1, 0.3])), max_iter=int(r.choice([50, 100, 200])), l2=float(r.choice([0, 1, 10])))
    else: c.update(hidden=[[16], [32, 16], [64, 32]][int(r.integers(3))], alpha=float(r.choice([0.0001, 0.001, 0.01])))
    return c


def features(k, c, idx):
    parts = []; fs = c["fset"]
    f = np.asarray(arr(k, "feat")[idx], np.float32)
    if "H" in fs.replace("HC", "").replace("HCz", ""): parts.append(f)
    if "HCz" in fs: parts.append(np.clip((f - arr(k, f"fmed{c['span_f']}")[idx]) / (arr(k, f"fmad{c['span_f']}")[idx] + 1e-3 * (1 + np.abs(f))), -20, 20))
    elif "HC" in fs: parts.append(f - arr(k, f"fmed{c['span_f']}")[idx])
    w = np.asarray(arr(k, "win")[idx], np.float32)
    if "WR" in fs: parts.append(w - np.asarray(arr(k, f"wmed{c['span_w']}")[idx], np.float32))
    elif "W" in fs.split("+") or fs == "W": parts.append(w)
    return np.nan_to_num(np.concatenate(parts, axis=1))


def smooth(score, start, n):
    if n <= 1: return score
    cs = np.concatenate([[0.0], np.cumsum(score)]); i = np.arange(len(score)); lo = np.maximum(i - n + 1, start)
    return (cs[i + 1] - cs[lo]) / (i + 1 - lo)


def fit_predict(c, Xtr, ytr, Xs):
    if c["model"] == "lr":
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        m = make_pipeline(StandardScaler(), LogisticRegression(C=c["C"], max_iter=500)).fit(Xtr, ytr); return [m.decision_function(X) for X in Xs]
    if c["model"] == "hgb":
        from sklearn.ensemble import HistGradientBoostingClassifier
        m = HistGradientBoostingClassifier(max_depth=c["max_depth"], learning_rate=c["lr"], max_iter=c["max_iter"], l2_regularization=c["l2"], early_stopping=False, random_state=8000 + c["id"]).fit(Xtr, ytr)
        return [m.decision_function(X) for X in Xs]
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler().fit(Xtr); m = MLPClassifier(tuple(c["hidden"]), alpha=c["alpha"], max_iter=40, random_state=8000 + c["id"]).fit(sc.transform(Xtr), ytr)
    def dec(X):
        q = np.clip(m.predict_proba(sc.transform(X))[:, 1], 1e-6, 1 - 1e-6); return np.log(q / (1 - q))
    return [dec(X) for X in Xs]


def job(a):
    c, k = a; t0 = time.time(); val = (k + 1) % 5; trf = [f for f in range(5) if f not in (k, val)]; r = np.random.default_rng(8000 + c["id"] + 100 * k)
    X, y = [], []
    for f in trf:
        ok = np.asarray(arr(f, "ok")); lab = np.asarray(arr(f, "label")); idx = np.where(ok & (lab >= 0))[0]; lab = lab[idx]
        for cls in (0, 1):
            sel = r.choice(idx[lab == cls], size=min(c["n_train"] // 3 + 1, (lab == cls).sum()), replace=False); sel.sort(); X.append(features(f, c, sel)); y.append(np.full(len(sel), cls))
    X = np.concatenate(X); y = np.concatenate(y); out = dict(cfg=c["id"], fold=k)
    evs = {}
    for name, f in (("val", val), ("test", k)):
        ok = np.asarray(arr(f, "ok")); lab = np.asarray(arr(f, "label")); idx = np.where(ok & (lab >= 0))[0] if False else np.arange(len(ok)); evs[name] = (f, idx)
    preds = fit_predict(c, X, y, [features(f, c, idx) for f, idx in evs.values()])
    from sklearn.metrics import roc_auc_score, average_precision_score
    thr = None
    for (name, (f, idx)), s in zip(evs.items(), preds):
        s = smooth(s, np.asarray(arr(f, "start")), c["smooth"]); ok = np.asarray(arr(f, "ok")); lab = np.asarray(arr(f, "label")); m = ok & (lab >= 0); yy = (lab[m] == 1).astype(int); ss = s[m]
        t_own = np.quantile(ss[yy == 0], 0.99); out[f"{name}_auroc"] = roc_auc_score(yy, ss); out[f"{name}_auprc"] = average_precision_score(yy, ss); out[f"{name}_sens1"] = float((ss[yy == 1] > t_own).mean())
        if name == "val": thr = t_own
        else: out["test_dep_sens"] = float((ss[yy == 1] > thr).mean()); out["test_dep_fpr"] = float((ss[yy == 0] > thr).mean())
        if name == "test": np.save(f"data/edge/c8_scores/{c['id']}_{k}.npy", ss.astype(np.float32)) if c["id"] < 0 else None
    out["sec"] = time.time() - t0; return out


if __name__ == "__main__":
    from multiprocessing import Pool
    n = int(sys.argv[1]); workers = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    make_cache(); cfgs = [sample_config(i) for i in range(n)]; json.dump(cfgs, open("results/c8_configs.json", "w"))
    done = set()
    if os.path.exists("results/c8_search_log.csv"):
        import pandas as pd; d = pd.read_csv("results/c8_search_log.csv"); done = set(zip(d.cfg, d.fold))
    jobs = [(c, k) for c in cfgs for k in range(5) if (c["id"], k) not in done]
    fields = ["cfg", "fold", "val_auroc", "val_auprc", "val_sens1", "test_auroc", "test_auprc", "test_sens1", "test_dep_sens", "test_dep_fpr", "sec"]
    new = not os.path.exists("results/c8_search_log.csv")
    with open("results/c8_search_log.csv", "a", newline="") as fh, Pool(workers) as p:
        w = csv.DictWriter(fh, fieldnames=fields);
        if new: w.writeheader()
        for i, o in enumerate(p.imap(job, jobs, chunksize=1)):
            w.writerow({k: o.get(k) for k in fields}); fh.flush()
            if i % 200 == 0: print(i, len(jobs), flush=True)
