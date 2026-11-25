"""C7: score outer-test folds once with frozen models / calibrated variants, then evaluate (beat level, subject bootstrap, episode level).  Replayed.
   python py/c7_score_eval.py -> results/c7_*.csv, fig_c7_calibration.png"""
import os, sys, json, pickle
import numpy as np, pandas as pd, torch
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E, c7_prep as P
import torch.nn.functional as F
torch.set_num_threads(8)


def pooled_feats(net, win):
    x = E.to_input(win).unsqueeze(1); out = []
    with torch.no_grad():
        for i in range(0, len(x), 8192):
            b = x[i:i + 8192]; b = F.relu(net.c1(F.pad(b, (3, 3)))); b = F.relu(net.c2(F.pad(b, (2, 2)))); b = F.relu(net.c3(F.pad(b, (0, 1)))); out.append(b.mean(2).numpy())
    return np.concatenate(out)


def score_all():
    for k in range(5):
        d = E.load_fold(k); r = np.load(f"data/edge/edb_resid_{k}.npz"); out = dict(np.load(f"data/edge/c2_scores_fold{k}.npz")); out["ok"] = d["ok"]
        recs = d["rec"]; t = d["t"]
        def by_record(X):                                                     # running median per record, causal
            X = X.astype(np.float32).reshape(len(X), -1); out_ = np.zeros_like(X)
            for ri in np.unique(recs):
                m = np.where(recs == ri)[0]; med, ok = P.run_median(t[m], X[m]); out_[m] = np.nan_to_num(X[m] - med)
            return out_
        m1 = pickle.load(open(f"data/edge/models/m1_f{k}.pkl", "rb"))["model"]; out["M1c"] = m1.decision_function(np.nan_to_num(r["featres"]))
        for s in range(3):
            ck = torch.load(f"data/edge/models/m2_f{k}_s{s}.pt"); net = E.BeatNet(); net.load_state_dict(ck["state"]); net.eval()
            sc = out[f"M2_s{s}"]; out[f"A1_s{s}"] = by_record(sc[:, None])[:, 0]
            h = pooled_feats(net, d["win"]); hr = by_record(h); w = net.fc.weight.detach().numpy(); out[f"A2_s{s}"] = hr @ (w[1] - w[0])
            ck = torch.load(f"data/edge/models/a3_f{k}_s{s}.pt"); net3 = E.BeatNet(); net3.load_state_dict(ck["state"]); net3.eval()
            with torch.no_grad(): out[f"A3_s{s}"] = torch.cat([net3.score(E.to_input(r["resid"][i:i + 8192])) for i in range(0, len(r["resid"]), 8192)]).numpy()
        np.savez_compressed(f"data/edge/c7_scores_fold{k}.npz", **out); print("scored", k)


def main():
    if not all(os.path.exists(f"data/edge/c7_scores_fold{k}.npz") for k in range(5)): score_all()
    import c2_eval as C2
    S = [dict(np.load(f"data/edge/c7_scores_fold{k}.npz")) for k in range(5)]; C2.S = S
    seeds = lambda p: [f"{p}_s{s}" for s in range(3)]
    METHODS = ["R0", "R1", "M1", "M1c"] + seeds("M2") + seeds("A1") + seeds("A2") + seeds("A3")
    thr = {m: {} for m in METHODS}
    for k in range(5):
        v = S[(k + 1) % 5]; mk = v["ok"] & (v["label"] == 0)
        for m in METHODS: thr[m][k] = E.thr_at_fpr(v[m][mk])
    C2.METHODS = METHODS
    # beat level + bootstrap
    rng = np.random.default_rng(7); B = 2000
    subs = sorted(set(np.concatenate([S[k]["subject"][S[k]["ok"] & (S[k]["label"] >= 0)] for k in range(5)]).tolist())); sidx = {s: i for i, s in enumerate(subs)}
    prep = {}
    for k in range(5):
        mk = S[k]["ok"] & (S[k]["label"] >= 0); y = (S[k]["label"][mk] == 1); sid = np.array([sidx[s] for s in S[k]["subject"][mk]])
        for m in METHODS:
            sc = S[k][m][mk]; pn = np.where(~y)[0]; pp = np.where(y)[0]; on = np.argsort(sc[pn]); op = np.argsort(sc[pp]); prep[(k, m)] = (sc[pn][on], sid[pn][on], sc[pp][op], sid[pp][op])
    res = {m: np.zeros(B) for m in METHODS}; pt = {}
    for m in METHODS:
        tp = pos = 0
        for k in range(5):
            sn, _, sp, _ = prep[(k, m)]; t_ = np.quantile(sn, 0.99); tp += (sp > t_).sum(); pos += len(sp)
        pt[m] = tp / pos
    ws = [np.bincount(rng.integers(0, len(subs), len(subs)), minlength=len(subs)).astype(float) for _ in range(B)]
    for b, w in enumerate(ws):
        for m in METHODS:
            tp = pos = 0.0
            for k in range(5):
                sn, idn, sp, idp = prep[(k, m)]; cw = np.cumsum(w[idn])
                if cw[-1] == 0: continue
                t_ = sn[min(np.searchsorted(cw, 0.99 * cw[-1]), len(sn) - 1)]; wp = w[idp]; pos += wp.sum(); tp += wp[sp > t_].sum()
            res[m][b] = tp / pos if pos else np.nan
    grp = lambda p: (np.mean([res[x] for x in seeds(p)], axis=0), float(np.mean([pt[x] for x in seeds(p)])))
    G = {"R0": (res["R0"], pt["R0"]), "R1": (res["R1"], pt["R1"]), "M1": (res["M1"], pt["M1"]), "M1c (M1 + calibration)": (res["M1c"], pt["M1c"]), "M2 frozen (3 seeds)": grp("M2"),
         "A1 score-level calibration (3 seeds)": grp("A1"), "A2 feature-level calibration (3 seeds)": grp("A2"), "A3 retrained on residual windows (3 seeds)": grp("A3")}
    ci = lambda x: np.nanpercentile(x, [2.5, 97.5]); rows = []
    for n, (r_, p_) in G.items(): rows.append(dict(quantity=f"{n}: sens@1%FPR", point=p_, lo=ci(r_)[0], hi=ci(r_)[1]))
    for s in range(3): rows.append(dict(quantity=f"A3 seed {s}: sens@1%FPR", point=pt[f"A3_s{s}"], lo=ci(res[f"A3_s{s}"])[0], hi=ci(res[f"A3_s{s}"])[1]))
    A3 = "A3 retrained on residual windows (3 seeds)"
    for lbl, a, b in (("PRIMARY A3 - R1", A3, "R1"), ("A3 - M2 frozen", A3, "M2 frozen (3 seeds)"), ("A3 - M1c", A3, "M1c (M1 + calibration)"), ("A3 - R0", A3, "R0"),
                      ("A1 - R1", "A1 score-level calibration (3 seeds)", "R1"), ("A2 - R1", "A2 feature-level calibration (3 seeds)", "R1"),
                      ("M1c - R1", "M1c (M1 + calibration)", "R1"), ("M1c - M1", "M1c (M1 + calibration)", "M1")):
        d = G[a][0] - G[b][0]; rows.append(dict(quantity=lbl, point=G[a][1] - G[b][1], lo=ci(d)[0], hi=ci(d)[1]))
    bt = pd.DataFrame(rows); bt["note"] = "subject bootstrap 2000, per-fold 1% FPR thresholds, pooled over 5 folds"; bt.to_csv("results/c7_bootstrap.csv", index=False); print(bt.round(3).to_string())
    # per fold AUROC / AUPRC for seed-0 variants
    fr = []
    for m in ["R1", "M2_s0", "A1_s0", "A2_s0", "A3_s0", "A3_s1", "A3_s2", "M1", "M1c"]:
        for k in range(5):
            mk = S[k]["ok"] & (S[k]["label"] >= 0); y = (S[k]["label"][mk] == 1).astype(int); s_ = S[k][m][mk]; fr.append(dict(method=m, fold=k, AUROC=E.auroc(y, s_), AUPRC=E.auprc(y, s_), sens1pct=float((s_[y == 1] > np.quantile(s_[y == 0], .99)).mean())))
    pd.DataFrame(fr).to_csv("results/c7_beat_metrics.csv", index=False); print(pd.DataFrame(fr).pivot(index="method", columns="fold", values="AUROC").round(3))
    # episode level
    META = C2.META; rowsE = []
    for m in METHODS:
        e = C2.episode_metrics(thr, methods=[m])[m]; rowsE.append({k: v for k, v in e.items() if k != "per_ep"})
    ep = pd.DataFrame(rowsE); ep.to_csv("results/c7_episode_metrics.csv", index=False); print(ep.round(3).to_string())
    json.dump({m: {str(k): v for k, v in t.items()} for m, t in thr.items()}, open("results/c7_thresholds.json", "w"), indent=1)


if __name__ == "__main__":
    main()
