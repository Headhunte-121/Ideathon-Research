"""C8 analysis of the random search.  python py/c8_analyze.py [N_prefix]
 1) nested selection (validation only) per outer fold; 2) winner's-curse measurements; 3) family breakdown; 4) subject bootstrap of nested picks vs R1 / A3 / M2."""
import os, sys, json
os.environ.setdefault("OMP_NUM_THREADS", "4")
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import c8_search as S8, edge_nets as E
from scipy.stats import spearmanr


def refit_scores(c, k):
    """Deterministic refit of one config on outer fold k; returns (test scores smoothed (all beats), val thr)."""
    val = (k + 1) % 5; trf = [f for f in range(5) if f not in (k, val)]; r = np.random.default_rng(8000 + c["id"] + 100 * k); X, y = [], []
    for f in trf:
        ok = np.asarray(S8.arr(f, "ok")); lab = np.asarray(S8.arr(f, "label")); idx = np.where(ok & (lab >= 0))[0]; lab = lab[idx]
        for cls in (0, 1):
            sel = r.choice(idx[lab == cls], size=min(c["n_train"] // 3 + 1, (lab == cls).sum()), replace=False); sel.sort(); X.append(S8.features(f, c, sel)); y.append(np.full(len(sel), cls))
    X = np.concatenate(X); y = np.concatenate(y); out = []
    preds = S8.fit_predict(c, X, y, [S8.features(f, c, np.arange(len(S8.arr(f, "ok")))) for f in (val, k)])
    for f, s in zip((val, k), preds): out.append(S8.smooth(s, np.asarray(S8.arr(f, "start")), c["smooth"]))
    return out[0], out[1]


def main():
    d = pd.read_csv("results/c8_search_log.csv"); cfgs = {c["id"]: c for c in json.load(open("results/c8_configs.json"))}
    full = d.groupby("cfg").fold.nunique(); ids = sorted(full[full == 5].index); N = int(sys.argv[1]) if len(sys.argv) > 1 else len(ids)
    # prefix rule: first N config ids that completed (ids are the random-draw order)
    ids = [i for i in range(max(ids) + 1) if i in set(ids)][:N]; d = d[d.cfg.isin(ids)]; print("configs used:", len(ids), "jobs:", len(d))
    # ---- nested selection ----
    rows = []; picks = {}
    for crit in ("val_auroc", "val_sens1"):
        for k in range(5):
            g = d[d.fold == k]; best = g.loc[g[crit].idxmax()]; picks[(crit, k)] = int(best.cfg)
            rows.append(dict(criterion=crit, fold=k, cfg=int(best.cfg), val_auroc=best.val_auroc, val_sens1=best.val_sens1, test_auroc=best.test_auroc, test_sens1=best.test_sens1, test_dep_sens=best.test_dep_sens, test_dep_fpr=best.test_dep_fpr,
                             config=json.dumps({a: b for a, b in cfgs[int(best.cfg)].items() if a != "id"})))
    sel = pd.DataFrame(rows); sel.to_csv("results/c8_nested_picks.csv", index=False); print(sel.drop(columns="config").round(3).to_string())
    # ---- winner's curse ----
    wc = []
    for k in range(5):
        g = d[d.fold == k]
        for m in ("auroc", "sens1"):
            rho = spearmanr(g[f"val_{m}"], g[f"test_{m}"])[0]; top = g.nlargest(10, f"val_{m}")
            wc.append(dict(fold=k, metric=m, spearman_val_vs_test=rho, mean_all_test=g[f"test_{m}"].mean(), best_val=g[f"val_{m}"].max(), test_of_best_val=g.loc[g[f"val_{m}"].idxmax(), f"test_{m}"],
                           mean_test_top10_by_val=top[f"test_{m}"].mean(), mean_val_top10=top[f"val_{m}"].mean(), best_test_any=g[f"test_{m}"].max()))
    wc = pd.DataFrame(wc); wc.to_csv("results/c8_winners_curse.csv", index=False); print(wc.round(3).to_string())
    # ---- family breakdown ----
    m = d.merge(pd.DataFrame(cfgs.values()), left_on="cfg", right_on="id")
    fam = []
    for col in ("model", "fset", "smooth", "span_f", "span_w", "n_train"):
        for v, g in m.groupby(col): fam.append(dict(factor=col, level=v, jobs=len(g), mean_val_auroc=g.val_auroc.mean(), mean_test_auroc=g.test_auroc.mean(), mean_test_sens1=g.test_sens1.mean()))
    pd.DataFrame(fam).to_csv("results/c8_family_breakdown.csv", index=False); print(pd.DataFrame(fam).round(3).to_string())
    # ---- bootstrap of nested picks (refit selected configs to get test scores) ----
    res = {}
    for crit in ("val_auroc", "val_sens1"):
        sc = {}
        for k in range(5):
            _, ts = refit_scores(cfgs[picks[(crit, k)]], k); sc[k] = ts
        res[crit] = sc
    S2 = [dict(np.load(f"data/edge/c2_scores_fold{k}.npz")) for k in range(5)]; S7 = [dict(np.load(f"data/edge/c7_scores_fold{k}.npz")) for k in range(5)]
    methods = {"nested pick (val AUROC)": [res["val_auroc"][k] for k in range(5)], "nested pick (val sens@1%FPR)": [res["val_sens1"][k] for k in range(5)],
               "R1": [S2[k]["R1"] for k in range(5)], "R0": [S2[k]["R0"] for k in range(5)], "M1": [S2[k]["M1"] for k in range(5)]}
    for p in ("M2", "A3"):
        for s in range(3): methods[f"{p}_s{s}"] = [(S2 if p == "M2" else S7)[k][f"{p}_s{s}"] for k in range(5)]
    subs = sorted(set(np.concatenate([S2[k]["subject"][S2[k]["ok"] & (S2[k]["label"] >= 0)] for k in range(5)]).tolist())); sidx = {s: i for i, s in enumerate(subs)}; rng = np.random.default_rng(7); B = 2000
    prep = {}
    for k in range(5):
        mk = S2[k]["ok"] & (S2[k]["label"] >= 0); y = S2[k]["label"][mk] == 1; sid = np.array([sidx[s] for s in S2[k]["subject"][mk]])
        for n, v in methods.items():
            sc = np.asarray(v[k])[mk]; pn = np.where(~y)[0]; pp = np.where(y)[0]; on = np.argsort(sc[pn]); op = np.argsort(sc[pp]); prep[(k, n)] = (sc[pn][on], sid[pn][on], sc[pp][op], sid[pp][op])
    pt = {}; boot = {n: np.zeros(B) for n in methods}
    for n in methods:
        tp = pos = 0
        for k in range(5): sn, _, sp, _ = prep[(k, n)]; tp += (sp > np.quantile(sn, .99)).sum(); pos += len(sp)
        pt[n] = tp / pos
    for b in range(B):
        w = np.bincount(rng.integers(0, len(subs), len(subs)), minlength=len(subs)).astype(float)
        for n in methods:
            tp = pos = 0.0
            for k in range(5):
                sn, idn, sp, idp = prep[(k, n)]; cw = np.cumsum(w[idn])
                if cw[-1] == 0: continue
                t_ = sn[min(np.searchsorted(cw, .99 * cw[-1]), len(sn) - 1)]; wp = w[idp]; pos += wp.sum(); tp += wp[sp > t_].sum()
            boot[n][b] = tp / pos if pos else np.nan
    ci = lambda x: np.nanpercentile(x, [2.5, 97.5]); out = []
    for n in methods: out.append(dict(quantity=f"{n}: sens@1%FPR", point=pt[n], lo=ci(boot[n])[0], hi=ci(boot[n])[1]))
    a3 = lambda f: np.mean([f(f"A3_s{s}") for s in range(3)], axis=0)
    for lbl in ("nested pick (val AUROC)", "nested pick (val sens@1%FPR)"):
        d1 = boot[lbl] - boot["R1"]; out.append(dict(quantity=f"{lbl} - R1", point=pt[lbl] - pt["R1"], lo=ci(d1)[0], hi=ci(d1)[1]))
        d2 = boot[lbl] - a3(lambda n: boot[n]); out.append(dict(quantity=f"{lbl} - A3 (3-seed mean)", point=pt[lbl] - np.mean([pt[f"A3_s{s}"] for s in range(3)]), lo=ci(d2)[0], hi=ci(d2)[1]))
    bt = pd.DataFrame(out); bt.to_csv("results/c8_bootstrap.csv", index=False); print(bt.round(3).to_string())
    au = []
    for n, v in methods.items():
        a = [E.auroc((S2[k]["label"][S2[k]["ok"] & (S2[k]["label"] >= 0)] == 1).astype(int), np.asarray(v[k])[S2[k]["ok"] & (S2[k]["label"] >= 0)]) for k in range(5)]; au.append(dict(method=n, **{f"fold{k}": a[k] for k in range(5)}, mean=np.mean(a)))
    pd.DataFrame(au).to_csv("results/c8_auroc_by_fold.csv", index=False); print(pd.DataFrame(au).round(3).to_string())


if __name__ == "__main__":
    main()
