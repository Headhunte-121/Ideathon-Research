import os, sys; sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve
S = [dict(np.load(f"data/edge/c2_scores_fold{k}.npz")) for k in range(5)]
ms = ["R0", "R1", "M1", "M2_s0", "M2_s1", "M2_s2"]
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
for m in ms:
    y = np.concatenate([(d["label"][d["ok"] & (d["label"] >= 0)] == 1) for d in S]); s = np.concatenate([d[m][d["ok"] & (d["label"] >= 0)] for d in S])
    f, t, _ = roc_curve(y, s); p, r, _ = precision_recall_curve(y, s); ax[0].plot(f, t, label=m); ax[1].plot(r, p, label=m)
ax[0].plot([0, 1], [0, 1], "k:"); ax[0].axvline(.01, c="gray", lw=.5); ax[0].set_xlabel("false-positive rate"); ax[0].set_ylabel("sensitivity (beats)"); ax[0].set_title("Pooled raw scores, 5 outer-test folds (EDB, Replayed)")
prev = y.mean(); ax[1].axhline(prev, c="k", ls=":", label=f"prevalence {prev:.2f}"); ax[1].set_xlabel("recall"); ax[1].set_ylabel("precision"); ax[1].legend(fontsize=7); ax[1].set_title("PR (balanced-ish test set: prevalence ~0.5)")
plt.tight_layout(); plt.savefig("results/fig_c2_roc_pr.png", dpi=110)
ep = pd.read_csv("results/c2_episode_metrics.csv"); fig, ax = plt.subplots(figsize=(7, 5))
for _, r in ep.iterrows():
    if r.window in ("24/30", "(heart-rate drift)") and not str(r.method).startswith("R0 at"):
        ax.scatter(max(r.false_per_24h, .1), r.sensitivity, marker="s" if "drift" in str(r.method) else "o"); ax.annotate(r.method.replace("drift: ", "")[:22], (max(r.false_per_24h, .1), r.sensitivity), fontsize=7)
ax.set_xscale("log"); ax.set_xlabel("false alerts per 24 h of episode-free time (log; few events, mostly too uncertain)"); ax.set_ylabel("ST-episode sensitivity"); ax.set_title("Episode level, EDB 90 records (Replayed)")
plt.tight_layout(); plt.savefig("results/fig_c2_episode.png", dpi=110)
