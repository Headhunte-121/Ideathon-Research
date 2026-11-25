"""C4: 2,000 held-out fold-0 test beats (1000 positive-label, 1000 negative-label, seeded) + 64 synthetic extreme vectors -> rtl_edge/tb/vectors_in.mem, vectors_expected.txt, results/c4_vector_manifest.csv"""
import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E, edge_int_model as IM
P = pickle.load(open("data/edge/quant/f0_first_(per.pkl", "rb")); d = E.load_fold(0); rng = np.random.default_rng(4242)
ok = d["ok"] & (d["label"] >= 0)
pos = np.where(ok & (d["label"] == 1))[0]; neg = np.where(ok & (d["label"] == 0))[0]
sel = np.concatenate([rng.choice(pos, 1000, replace=False), rng.choice(neg, 1000, replace=False)]); rng.shuffle(sel)
vec = [d["win"][i] for i in sel]; man = [dict(kind="real test beat", fold0_index=int(i), subject=int(d["subject"][i]), record=int(d["rec"][i]), t=float(d["t"][i]), label=int(d["label"][i])) for i in sel]
cnt = pd.Series([m["subject"] for m in man]).value_counts(); assert (cnt >= 20).sum() >= 5, cnt
ext = [np.full(75, 127), np.full(75, -128), np.zeros(75), np.where(np.arange(75) % 2, 127, -128), np.where(np.arange(75) % 2, -128, 127), np.full(75, 1), np.full(75, -1), np.arange(75) - 37, 37 - np.arange(75),
       np.where(np.arange(75) < 37, 127, -128), np.where(np.arange(75) < 37, -128, 127), np.where(np.arange(75) % 3 == 0, 127, 0), np.where(np.arange(75) % 4 < 2, 127, -128)]
for i in range(3): ext.append(np.zeros(75, int)); ext[-1][[0, 37, 74][i]] = 127
for i in range(3): ext.append(np.zeros(75, int)); ext[-1][[0, 37, 74][i]] = -128
while len(ext) < 64: ext.append(rng.integers(-128, 128, 75))
ext = [np.asarray(e, dtype=np.int8) for e in ext[:64]]
for e in ext: vec.append(e); man.append(dict(kind="synthetic extreme", fold0_index=-1, subject=-1, record=-1, t=-1.0, label=-1))
W = np.stack(vec).astype(np.int8); S = IM.forward_int_batch(W, P)
mx = max(P["_maxacc"].values()); assert mx < 2 ** 31, mx
os.makedirs("rtl_edge/tb", exist_ok=True)
open("rtl_edge/tb/vectors_in.mem", "w").write("\n".join(f"{int(v) & 255:02x}" for v in W.reshape(-1)) + "\n"); open("rtl_edge/tb/vectors_expected.txt", "w").write("\n".join(str(int(s)) for s in S) + "\n")
m = pd.DataFrame(man); m["expected_score"] = S; m.to_csv("results/c4_vector_manifest.csv", index=False)
print(len(W), "vectors; max |acc| over all layers", mx, "(< 2^31); score range", S.min(), S.max(), "; subjects with >=20 beats:", int((cnt >= 20).sum()))
