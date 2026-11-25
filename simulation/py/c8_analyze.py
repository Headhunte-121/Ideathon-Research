"""C8 analysis of the random searches (tabular + GPU CNN).  python py/c8_analyze.py      (env C8_DRY=1 -> 50 bootstrap resamples, outputs prefixed c8dry_)
 1) nested selection (validation only) per outer fold and family; 2) winner's-curse measurements; 3) factor breakdown; 4) subject bootstrap of nested picks vs R1 / A3 / M2."""
import os, sys, json, traceback
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".torch_cuda"))   # optional local CUDA build of PyTorch
os.environ.setdefault("OMP_NUM_THREADS", "4")
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import c8_search as S8, c8_cnn_search as CN, edge_nets as E
from scipy.stats import spearmanr
DRY = os.environ.get("C8_DRY") == "1"; P = "c8dry_" if DRY else "c8_"; B = 50 if DRY else 2000


def refit(key, cfgs, k):
    """Deterministic refit of one config on outer fold k -> smoothed test scores over all beats of fold k."""
    fam, i = key[0], int(key[1:]); c = cfgs[key]
    if fam == "C": return CN.job(c, k)[1]
    val = (k + 1) % 5; trf = [f for f in range(5) if f not in (k, val)]; r = np.random.default_rng(8000 + c["id"] + 100 * k); X, y = [], []
    for f in trf:
        ok = np.asarray(S8.arr(f, "ok")); lab = np.asarray(S8.arr(f, "label")); idx = np.where(ok & (lab >= 0))[0]; lab = lab[idx]
        for cls in (0, 1):
            sel = r.choice(idx[lab == cls], size=min(c["n_train"] // 3 + 1, (lab == cls).sum()), replace=False); sel.sort(); X.append(S8.features(f, c, sel)); y.append(np.full(len(sel), cls))
    X = np.concatenate(X); y = np.concatenate(y); s = S8.fit_predict(c, X, y, [S8.features(k, c, np.arange(len(S8.arr(k, "ok"))))])[0]
    return S8.smooth(s, np.asarray(S8.arr(k, "start")), c["smooth"])


def load():
    cfgs = {f"T{c['id']}": c for c in json.load(open("results/c8_configs.json"))}; cfgs.update({f"C{c['id']}": c for c in json.load(open("results/c8_cnn_configs.json"))})
    t = pd.read_csv("results/c8_search_log.csv"); t["family"] = "tabular"; t["key"] = "T" + t.cfg.astype(int).astype(str)
    cs = []
    import glob
    for p in sorted(glob.glob("results/c8_cnn_log_*.csv")): cs.append(pd.read_csv(p))
    c = pd.concat(cs); c["family"] = "cnn"; c["key"] = "C" + c.cfg.astype(int).astype(str)
    d = pd.concat([t, c]).reset_index(drop=True); d = d.drop_duplicates(["key", "fold"]).reset_index(drop=True); full = d.groupby("key").fold.nunique(); d = d[d.key.isin(full[full == 5].index)].reset_index(drop=True)
    return d, cfgs


def main():
    d, cfgs = load(); print("complete configs:", d.groupby("family").key.nunique().to_dict(), flush=True)
    rows = []; picks = {}
    for crit in ("val_auroc", "val_sens1"):
        for fam in ("tabular", "cnn", "all"):
            for k in range(5):
                g = d[(d.fold == k) & ((d.family == fam) | (fam == "all"))]; best = g.loc[g[crit].idxmax()]; picks[(crit, fam, k)] = best["key"]
                rows.append(dict(criterion=crit, family=fam, fold=k, key=best["key"], val_auroc=best.val_auroc, val_sens1=best.val_sens1, test_auroc=best.test_auroc, test_sens1=best.test_sens1, test_dep_sens=best.test_dep_sens, test_dep_fpr=best.test_dep_fpr,
                                 config=json.dumps({a: b for a, b in cfgs[best["key"]].items() if a != "id"})))
    sel = pd.DataFrame(rows); sel.to_csv(f"results/{P}nested_picks.csv", index=False)
    summ = sel.groupby(["criterion", "family"])[["val_auroc", "test_auroc", "test_sens1"]].mean().round(3); print(summ, flush=True)
    wc = []
    for fam in ("tabular", "cnn"):
        for k in range(5):
            g = d[(d.fold == k) & (d.family == fam)]
            for m in ("auroc", "sens1"):
                top = g.nlargest(10, f"val_{m}")
                wc.append(dict(family=fam, fold=k, metric=m, n_configs=len(g), spearman_val_vs_test=spearmanr(g[f"val_{m}"], g[f"test_{m}"])[0], mean_all_test=g[f"test_{m}"].mean(), best_val=g[f"val_{m}"].max(),
                               test_of_best_val=g.loc[g[f"val_{m}"].idxmax(), f"test_{m}"], mean_test_top10_by_val=top[f"test_{m}"].mean(), best_test_any=g[f"test_{m}"].max()))
    pd.DataFrame(wc).to_csv(f"results/{P}winners_curse.csv", index=False)
    m = d.merge(pd.DataFrame([{**c, "key": k} for k, c in cfgs.items()]), on="key", suffixes=("", "_cfg")); fam = []
    for f in ("tabular", "cnn"):
        for col in (["model", "fset", "smooth", "span_f", "span_w", "n_train"] if f == "tabular" else ["inp", "smooth", "aug", "lr", "drop", "batch", "per_class", "wd"]):
            for v, g in m[m.family == f].groupby(col): fam.append(dict(family=f, factor=col, level=v, jobs=len(g), mean_val_auroc=g.val_auroc.mean(), mean_test_auroc=g.test_auroc.mean(), mean_test_sens1=g.test_sens1.mean()))
    pd.DataFrame(fam).to_csv(f"results/{P}factor_breakdown.csv", index=False)
    # ---- bootstrap ----
    S2 = [dict(np.load(f"data/edge/c2_scores_fold{k}.npz")) for k in range(5)]; S7 = [dict(np.load(f"data/edge/c7_scores_fold{k}.npz")) for k in range(5)]
    methods = {}
    for fam in ("tabular", "cnn", "all"):
        for crit in ("val_auroc",):
            methods[f"nested pick: {fam} (val AUROC)"] = [refit(picks[(crit, fam, k)], cfgs, k) for k in range(5)]
    methods.update({"R1": [S2[k]["R1"] for k in range(5)], "R0": [S2[k]["R0"] for k in range(5)], "M1": [S2[k]["M1"] for k in range(5)]})
    for p_ in ("M2", "A3"):
        for s in range(3): methods[f"{p_}_s{s}"] = [(S2 if p_ == "M2" else S7)[k][f"{p_}_s{s}"] for k in range(5)]
    subs = sorted(set(np.concatenate([S2[k]["subject"][S2[k]["ok"] & (S2[k]["label"] >= 0)] for k in range(5)]).tolist())); sidx = {s: i for i, s in enumerate(subs)}; rng = np.random.default_rng(7)
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
    ci = lambda x: np.nanpercentile(x, [2.5, 97.5]); out = [dict(quantity=f"{n}: sens@1%FPR", point=pt[n], lo=ci(boot[n])[0], hi=ci(boot[n])[1]) for n in methods]
    for lbl in [n for n in methods if n.startswith("nested")]:
        d1 = boot[lbl] - boot["R1"]; out.append(dict(quantity=f"{lbl} - R1", point=pt[lbl] - pt["R1"], lo=ci(d1)[0], hi=ci(d1)[1]))
        a3 = np.mean([boot[f"A3_s{s}"] for s in range(3)], axis=0); d2 = boot[lbl] - a3; out.append(dict(quantity=f"{lbl} - A3 (3-seed mean)", point=pt[lbl] - np.mean([pt[f"A3_s{s}"] for s in range(3)]), lo=ci(d2)[0], hi=ci(d2)[1]))
    bt = pd.DataFrame(out); bt.to_csv(f"results/{P}bootstrap.csv", index=False); print(bt.round(3).to_string(), flush=True)
    au = []
    for n, v in methods.items():
        a = [E.auroc((S2[k]["label"][S2[k]["ok"] & (S2[k]["label"] >= 0)] == 1).astype(int), np.asarray(v[k])[S2[k]["ok"] & (S2[k]["label"] >= 0)]) for k in range(5)]; au.append(dict(method=n, **{f"fold{k}": a[k] for k in range(5)}, mean=np.mean(a)))
    au = pd.DataFrame(au); au.to_csv(f"results/{P}auroc_by_fold.csv", index=False); print(au.round(3).to_string(), flush=True)
    write_report(d, sel, wc, bt, au, summ)


def write_report(d, sel, wc, bt, au, summ):
    wc = pd.DataFrame(wc); n = d.groupby("family").key.nunique().to_dict(); lo = bt[bt.quantity == "nested pick: all (val AUROC) - R1"].iloc[0]
    verdict = "SEARCH ADDS VALUE (lower end above 0)" if lo.lo > 0 else "NO ADDED VALUE SHOWN (lower end not above 0)"
    rho = wc.groupby(["family", "metric"]).spearman_val_vs_test.mean().round(3).to_string()
    gap = wc.groupby(["family", "metric"]).apply(lambda g: pd.Series(dict(best_val=g.best_val.mean(), test_of_best_val=g.test_of_best_val.mean(), mean_all_test=g.mean_all_test.mean(), best_test_any=g.best_test_any.mean())), include_groups=False).round(3).to_string()
    txt = f"""# C8: large nested random search on EDB (auto-generated; numbers come from results/{P}*.csv)

Protocol frozen before any result (`configs/c8_frozen.json`, `c8_cnn_frozen.json`). Configurations completed: {n}. Each outer fold picks its own best configuration by inner-validation AUROC only; test scores of all configurations are logged only to measure the winner's curse. EDB subjects were already used as test folds earlier in this project, so any winner here is a **hypothesis, not a result**; the raw LTSTDB ECG (the only fresh ST-labelled source) was not downloaded (about 114 KB/s measured, about 17 hours). Label: **Replayed**.

## Pass rule (written in advance)
Search adds value only if the lower end of the 95 % subject-bootstrap range of (nested pick, all families, sensitivity at 1 % FPR) minus R1 is above 0.
Outcome: **{verdict}**; point {lo.point:.3f}, range {lo.lo:.3f} to {lo.hi:.3f}.

## Nested picks, mean over the 5 outer folds (validation-selected)
```
{summ.to_string()}
```
## Bootstrap (sensitivity at 1 % false-positive rate, pooled over 5 folds)
```
{bt.round(3).to_string(index=False)}
```
## AUROC by fold (unseen patients)
```
{au.round(3).to_string(index=False)}
```
## Winner's curse: how well validation rank predicts test rank
Spearman correlation between validation and test metric across configurations (mean over folds):
```
{rho}
```
Mean over folds: best validation value vs the test value of that same configuration vs the average configuration vs the best test value of any configuration:
```
{gap}
```
A big gap between "best_val" and "test_of_best_val" is the optimism of picking the best of thousands; "best_test_any" is what you would wrongly report if you picked on test.

## What this does NOT show
Nothing about early warning, lead time or ischemia: labels are ST episodes marked by an amplitude rule (circular), all 79 subjects were already used as test folds before, and no fresh data exists. The drift-absorption risk of a running baseline in a truly ischemic person is untested.

"""
    open("../docs/reports/C8_SEARCH_REPORT.md" if not DRY else "results/c8dry_report.md", "w", encoding="utf-8").write(txt)


if __name__ == "__main__":
    try: main()
    except Exception: open(f"results/{P}analysis_error.txt", "w").write(traceback.format_exc()); raise
