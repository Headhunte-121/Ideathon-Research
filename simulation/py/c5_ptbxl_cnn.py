"""C5: tiny CNN vs five-feature model on PTB-XL (MI vs NORM).  Replayed (Python; not a wearable, not early warning).  python py/c5_ptbxl_cnn.py train | test"""
import os, sys, json
import numpy as np, pandas as pd, torch
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E
CFG = json.load(open("configs/c5_frozen.json")); LEADS = CFG["leads"]
Z = np.load("data/edge/ptbxl_windows.npz")


def sel(li, folds):
    m = Z["valid"][:, li] & np.isin(Z["fold"], folds); return Z["win"][m, li], Z["label"][m].astype(int), Z["patient"][m], Z["ecg_id"][m]


def job(a):
    li, seed = a; torch.set_num_threads(1); rs = 100 * li + seed; rng = np.random.default_rng(rs); torch.manual_seed(rs)
    wt, yt, _, _ = sel(li, range(1, 9)); wv, yv, _, _ = sel(li, [9]); net = E.BeatNet(); opt = torch.optim.Adam(net.parameters(), lr=1e-3, weight_decay=1e-4)
    pos = np.where(yt == 1)[0]; neg = np.where(yt == 0)[0]; xv = E.to_input(wv); best = (-1, None, None); bad = 0
    for ep in range(30):
        idx = np.concatenate([pos, rng.choice(neg, len(pos), replace=False)]); rng.shuffle(idx); net.train()
        for i in range(0, len(idx), 256):
            b = idx[i:i + 256]; l = torch.nn.functional.cross_entropy(net(E.to_input(wt[b])), torch.from_numpy(yt[b])); opt.zero_grad(); l.backward(); opt.step()
        net.eval()
        with torch.no_grad(): sv = net.score(xv).numpy()
        ap = E.auprc(yv, sv)
        if ap > best[0]: best = (ap, {k: v.clone() for k, v in net.state_dict().items()}, sv.copy()); bad = 0
        else:
            bad += 1
            if bad >= 5: break
    from sklearn.metrics import roc_curve
    f, t, th = roc_curve(yv, best[2]); thr = float(th[np.argmax(t - f)]); torch.save(dict(state=best[1], thr=thr), f"data/edge/models/c5_l{li}_s{seed}.pt")
    return dict(lead=LEADS[li], seed=seed, val_auprc=best[0], val_auroc=E.auroc(yv, best[2]), youden_thr=thr)


def wauc(sp, wp, sn, wn):
    o = np.argsort(sn); cw = np.concatenate([[0], np.cumsum(wn[o])]); s = sn[o]; lo = np.searchsorted(s, sp, "left"); hi = np.searchsorted(s, sp, "right")
    return (wp * (cw[lo] + 0.5 * (cw[hi] - cw[lo]))).sum() / (wp.sum() * wn.sum())


def boot_auc(y, s, pat, B=2000, seed=7):
    rng = np.random.default_rng(seed); u, inv = np.unique(pat, return_inverse=True); out = []
    for _ in range(B):
        w = np.bincount(rng.integers(0, len(u), len(u)), minlength=len(u)).astype(float)[inv]
        out.append(wauc(s[y == 1], w[y == 1], s[y == 0], w[y == 0]))
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


if __name__ == "__main__":
    if sys.argv[1] == "train":
        from multiprocessing import Pool
        with Pool(12) as p: res = p.map(job, [(li, s) for li in range(4) for s in range(3)])
        df = pd.DataFrame(res); df.to_csv("results/c5_ptbxl_train_val.csv", index=False); print(df); mean = df.groupby("lead").val_auroc.mean(); best = mean.idxmax(); print(mean, "chosen", best)
        CFG["chosen_lead"] = best; json.dump(CFG, open("configs/c5_frozen.json", "w"), indent=1)
    else:
        import c3_quantize as Q
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        import a3_ptbxl as A
        feats = pd.read_csv("data/a3/features.csv"); a3 = json.load(open("configs/a3_frozen.json")); db = A.labels(); rows = []; pat_of = db.patient_id; NB = 2000
        for li, lead in enumerate(LEADS):
            wte, yte, pte, ide = sel(li, [10]); scs = []
            for s in range(3):
                ck = torch.load(f"data/edge/models/c5_l{li}_s{s}.pt"); net = E.BeatNet(); net.load_state_dict(ck["state"]); net.eval()
                with torch.no_grad(): sc = net.score(E.to_input(wte)).numpy()
                scs.append(sc); lo, hi = boot_auc(yte, sc, pte, NB); rows.append(dict(model=f"CNN float seed {s}", lead=lead, AUC=E.auroc(yte, sc), lo=lo, hi=hi, n=len(yte), MI=int(yte.sum()), chosen_lead=lead == CFG["chosen_lead"]))
            if lead == CFG["chosen_lead"]:
                ck = torch.load(f"data/edge/models/c5_l{li}_s0.pt"); state = {n: v.numpy().astype(np.float64) for n, v in ck["state"].items()}; wt, yt, _, _ = sel(li, range(1, 9)); wv, yv, _, _ = sel(li, [9])
                calib = wt[np.random.default_rng(100).choice(len(wt), 4000, replace=False)]; P = Q.quantize(state, calib)
                si = Q.int_scores(wte, P); sf = scs[0]; lo, hi = boot_auc(yte, si, pte, NB)
                rows.append(dict(model="CNN INT8 (seed 0)", lead=lead, AUC=E.auroc(yte, si), lo=lo, hi=hi, n=len(yte), MI=int(yte.sum()), chosen_lead=True))
                net = E.BeatNet(); net.load_state_dict(ck["state"]); net.eval()
                with torch.no_grad(): fv = net.score(E.to_input(wv)).numpy()
                iv = Q.int_scores(wv, P); frac = float((fv > ck["thr"]).mean()); ti = float(np.quantile(iv, 1 - frac))
                for nm, s_, t_ in (("float", sf, ck["thr"]), ("INT8", si, ti)):
                    p_ = s_ > t_; rows.append(dict(model=f"CNN {nm} seed 0 at fold-9 operating point", lead=lead, sens=float(p_[yte == 1].mean()), spec=float((~p_)[yte == 0].mean()), n=len(yte), chosen_lead=True))
                rows.append(dict(model="CNN INT8 vs float: decision agreement", lead=lead, agreement=float(((si > ti) == (sf > ck["thr"])).mean()), chosen_lead=True))
            for sname, cols in A.SETS.items():
                C = a3["models"][f"{lead}|{sname}"]["C"]; d = feats[feats.lead == lead]; tr = d[d.strat_fold.isin(range(1, 9))]; te = d[d.strat_fold == 10].dropna(subset=["st_level"])
                med = tr[cols].median(); m = make_pipeline(StandardScaler(), LogisticRegression(C=C, class_weight="balanced", max_iter=1000)).fit(tr[cols].fillna(med), tr.label)
                p = m.predict_proba(te[cols].fillna(med))[:, 1]; pt = pat_of.loc[te.ecg_id].values; yy = te.label.values.astype(int); lo, hi = boot_auc(yy, p, pt, NB)
                rows.append(dict(model=f"A3 logistic: {sname}", lead=lead, AUC=E.auroc(yy, p), lo=lo, hi=hi, n=len(te), MI=int(yy.sum()), chosen_lead=lead == CFG["chosen_lead"]))
        df = pd.DataFrame(rows); df["label"] = "Replayed (PTB-XL fold 10; resting diagnostic ECG; not early warning)"; df.to_csv("results/c5_ptbxl_test.csv", index=False); print(df.round(3).to_string())
