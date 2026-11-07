"""C6: 'an hour before' weak hypothesis test on EDB, frozen fold models, no retraining.  Replayed, HYPOTHESIS ONLY - never a lead-time or prediction claim.
Pre-window beats: onset-60 min .. onset-15 min of each ST episode, kept only if no other ST/T episode overlaps [onset-60 min, onset].  Comparison: ordinary negatives (label 0)
of the same test patients that are not in any pre-window.  Statistic = mean over the 5 test folds of per-fold AUROC; subject bootstrap 2000.  -> results/c6_prelead.csv"""
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import c1_lib as C
META = json.load(open("data/edge/edb_meta.json")); RECS = C.records()
METHODS = ["R0", "R1", "M1", "M2_s0", "M2_s1", "M2_s2"]

def wauc(sc_pos, w_pos, sc_neg, w_neg):
    o = np.argsort(sc_neg); sn = sc_neg[o]; cw = np.concatenate([[0], np.cumsum(w_neg[o])]); lo = np.searchsorted(sn, sc_pos, "left"); hi = np.searchsorted(sn, sc_pos, "right")
    below = cw[lo] + 0.5 * (cw[hi] - cw[lo]); den = w_pos.sum() * w_neg.sum()
    return (w_pos * below).sum() / den if den > 0 else np.nan

if __name__ == "__main__":
    S = [dict(np.load(f"data/edge/c2_scores_fold{k}.npz")) for k in range(5)]; pre = []; 
    subs = sorted({META[r]["subject"] for r in RECS}); sidx = {s: i for i, s in enumerate(subs)}
    data = []; nep = 0
    for k, d in enumerate(S):
        pm = np.zeros(len(d["t"]), bool)
        for ri in np.unique(d["rec"]):
            mt = META[RECS[ri]]; allep = [(s, e) for s, e, _ in mt["st"] + mt["tw"]]; sel = d["rec"] == ri
            for s, e, _ in mt["st"]:
                if any((e2 >= s - 3600 and s2 <= s and (s2, e2) != (s, e)) for s2, e2 in allep): continue
                nep += 1; pm |= sel & (d["t"] >= s - 3600) & (d["t"] < s - 900)
        pm &= d["ok"]; neg = d["ok"] & (d["label"] == 0) & ~pm
        sid = np.array([sidx[META[RECS[r]]["subject"]] for r in d["rec"]]); data.append((pm, neg, sid, d))
    npre = sum(int(p.sum()) for p, _, _, _ in data); nneg = sum(int(n.sum()) for _, n, _, _ in data)
    rng = np.random.default_rng(7); rows = []; B = 2000; W = [rng.multinomial(len(subs), np.ones(len(subs)) / len(subs), size=1)[0] for _ in range(0)]
    ws = [np.bincount(rng.integers(0, len(subs), len(subs)), minlength=len(subs)).astype(float) for _ in range(B)]
    for m in METHODS:
        pt = []; 
        for pm, neg, sid, d in data:
            if pm.sum() and neg.sum(): pt.append(wauc(d[m][pm], np.ones(pm.sum()), d[m][neg], np.ones(neg.sum())))
        bs = []
        for w in ws:
            a = []
            for pm, neg, sid, d in data:
                if pm.sum() and neg.sum(): a.append(wauc(d[m][pm], w[sid[pm]], d[m][neg], w[sid[neg]]))
            bs.append(np.nanmean(a))
        rows.append(dict(method=m, mean_fold_AUROC=float(np.mean(pt)), lo=float(np.nanpercentile(bs, 2.5)), hi=float(np.nanpercentile(bs, 97.5)), per_fold=";".join(f"{x:.3f}" for x in pt),
                         episodes_used=nep, pre_beats=npre, ordinary_negative_beats=nneg, includes_0p5=bool(np.nanpercentile(bs, 2.5) <= 0.5 <= np.nanpercentile(bs, 97.5)), label="Replayed, hypothesis only"))
    df = pd.DataFrame(rows); df.to_csv("results/c6_prelead.csv", index=False); print(df.round(3).to_string())
