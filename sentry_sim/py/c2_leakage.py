"""C2.6 leakage demo: same M2 recipe (seed 0), RANDOM beat-wise split with fold-0-sized test, fold-1-sized validation, folds-2..4-sized train (subjects mixed).  Replayed.
 -> results/c2_leakage_demo.csv, results/fig_c2_leakage.png"""
import os, sys, json, time
import numpy as np, pandas as pd, torch
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E
CFG = json.load(open("configs/c2_frozen.json"))
if __name__ == "__main__":
    torch.set_num_threads(8)
    ds = [E.load_fold(k) for k in range(5)]
    ms = [d["scored"] & (d["label"] >= 0) for d in ds]
    n = [int(m.sum()) for m in ms]
    win = np.concatenate([d["win"][m] for d, m in zip(ds, ms)]); lab = np.concatenate([d["label"][m] for d, m in zip(ds, ms)])
    rng = np.random.default_rng(0); perm = rng.permutation(len(lab))
    te, va, tr = perm[:n[0]], perm[n[0]:n[0] + n[1]], perm[n[0] + n[1]:]
    net = E.BeatNet(); torch.manual_seed(0); net = E.BeatNet(); opt = torch.optim.Adam(net.parameters(), lr=1e-3, weight_decay=1e-4)
    pos = tr[lab[tr] == 1]; neg = tr[lab[tr] == 0]; xv = E.to_input(win[va]); best = (-1, None, None); bad = 0; r2 = np.random.default_rng(0)
    for ep in range(30):
        net.train(); idx = np.concatenate([pos, r2.choice(neg, size=len(pos), replace=len(neg) < len(pos))]); r2.shuffle(idx)
        for i in range(0, len(idx), 256):
            b = idx[i:i + 256]; loss = torch.nn.functional.cross_entropy(net(E.to_input(win[b])), torch.from_numpy(lab[b].astype(np.int64))); opt.zero_grad(); loss.backward(); opt.step()
        net.eval()
        with torch.no_grad(): sv = torch.cat([net.score(xv[i:i + 8192]) for i in range(0, len(xv), 8192)]).numpy()
        ap = E.auprc(lab[va], sv)
        if ap > best[0]: best = (ap, {k: v.clone() for k, v in net.state_dict().items()}, sv.copy(), ep); bad = 0
        else:
            bad += 1
            if bad >= 5: break
    net.load_state_dict(best[1]); net.eval(); thr = E.thr_at_fpr(best[2][lab[va] == 0])
    with torch.no_grad(): st = net.score(E.to_input(win[te])).numpy()
    y = lab[te]; sens, _ = E.sens_at_fpr(st[y == 1], st[y == 0])
    row_leak = dict(split="random beat-wise (subjects mixed)", best_epoch=best[3], val_AUPRC=best[0], test_AUROC=E.auroc(y, st), test_AUPRC=E.auprc(y, st), sens_at_1pct_FPR_curve=sens,
                    deployed_sens=float((st[y == 1] > thr).mean()), deployed_FPR=float((st[y == 0] > thr).mean()), n_test=len(te))
    bm = pd.read_csv("results/c2_beat_metrics.csv"); r = bm[(bm.method == "M2_s0") & (bm.fold.astype(str) == "0")].iloc[0]
    row_pw = dict(split="patient-wise (outer fold 0, seed 0)", val_AUPRC=float(pd.read_csv("results/c2_train_log.csv").query("kind=='M2' and fold==0 and seed==0").val_auprc.iloc[0]), test_AUROC=r.AUROC, test_AUPRC=r.AUPRC,
                  sens_at_1pct_FPR_curve=r.sens_at_1pct_FPR_curve, deployed_sens=r.deployed_sens, deployed_FPR=r.deployed_FPR, n_test=int(r.n_pos + r.n_neg))
    df = pd.DataFrame([row_pw, row_leak]); df.to_csv("results/c2_leakage_demo.csv", index=False); print(df.round(3).to_string())
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4)); xs = np.arange(3); w = .35
    for i, (rw, lbl) in enumerate(((row_pw, "patient-wise"), (row_leak, "random beat-wise"))): ax.bar(xs + i * w, [rw["test_AUROC"], rw["test_AUPRC"], rw["sens_at_1pct_FPR_curve"]], w, label=lbl)
    ax.set_xticks(xs + w / 2); ax.set_xticklabels(["AUROC", "AUPRC", "sens @1% FPR"]); ax.legend(); ax.set_title("Leakage demo (tiny CNN, EDB, seed 0)"); plt.tight_layout(); plt.savefig("results/fig_c2_leakage.png", dpi=110)
