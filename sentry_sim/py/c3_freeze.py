"""C3 freeze: integer parameters of the fold-0 / seed-0 model (first attempt, per-tensor) -> configs/c3_quant_frozen.json, rtl_edge/weights/*.mem, results/c3_layers.csv, fig_c3_int8.png.  Calculated + Replayed."""
import os, sys, json, pickle, hashlib
import numpy as np, pandas as pd, torch
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E, edge_int_model as IM
P = pickle.load(open("data/edge/quant/f0_first_(per.pkl", "rb"))
os.makedirs("rtl_edge/weights", exist_ok=True)
def hx(v, bits): return f"{int(v) & ((1 << bits) - 1):0{bits // 4}x}"
def dump(name, arr, bits): open(f"rtl_edge/weights/{name}.mem", "w").write("\n".join(hx(v, bits) for v in np.asarray(arr).reshape(-1)) + "\n")
for nm in ("conv1", "conv2", "conv3"):
    dump(f"{nm}_w", P[f"{nm}_w"], 8); dump(f"{nm}_b", P[f"{nm}_b"], 32); dump(f"{nm}_m0", P[f"{nm}_M0"], 32); dump(f"{nm}_n", P[f"{nm}_n"], 8)
dump("fc_w", P["fc_w"], 8); dump("fc_b", P["fc_b"], 32)
# integer threshold for fold 0 (same positive-fraction rule as c3_quantize)
ck = torch.load("data/edge/models/m2_f0_s0.pt"); thr_f = ck["thr"]; dv = E.load_fold(1); mv = dv["ok"] & (dv["label"] >= 0)
Sv = np.load("data/edge/c2_scores_fold1.npz"); frac = float((Sv["M2_s0"][mv] > thr_f).mean())
iv = np.concatenate([IM.forward_int_batch(dv["win"][mv][i:i + 4096], P) for i in range(0, mv.sum(), 4096)]); thr_i = float(np.quantile(iv, 1 - frac))
meta = P["_meta"]
cfg = dict(name="c3_quant_frozen", model="outer fold 0, seed 0, post-training INT8, first attempt (per-tensor weight scales)", input_shift="window = clip(((pair_avg - baseline) >> 8), -128, 127), baseline = sum(250 Hz samples R-18..R-11)>>3",
           float_input_scale=E.IN_SCALE, rounding="y = (acc*M0 + (1<<(n-1))) >> n, int64 product, arithmetic shift (floor), clamp [0,127]", gap="sum of 19 positions, no division", score="logit1 - logit0 (int32)",
           integer_threshold_fold0=thr_i, float_threshold_fold0=thr_f, threshold_rule="integer threshold gives same positive fraction as float threshold on inner-validation fold 1",
           layers={nm: dict(s_in=meta[nm]["s_in"], s_w=meta[nm]["s_w"], s_out=meta[nm]["s_out"], M0=P[f"{nm}_M0"].tolist(), n=P[f"{nm}_n"].tolist(), bias_q=P[f"{nm}_b"].tolist()) for nm in ("conv1", "conv2", "conv3")},
           fc=dict(s_w=meta["fc"]["s_w"], logit_scale=meta["fc"]["logit_scale"], bias_q=P["fc_b"].tolist()),
           weights_sha256={f: hashlib.sha256(open(f"rtl_edge/weights/{f}", "rb").read()).hexdigest() for f in sorted(os.listdir("rtl_edge/weights"))}, weights_files="rtl_edge/weights/*.mem (hex two's complement, one value per line)",
           pass_rule_2_note="evaluated in results/c3_int8_vs_float.csv; first attempt and fallbacks a, b all listed")
json.dump(cfg, open("configs/c3_quant_frozen.json", "w"), indent=1)
# layers table (Calculated)
rows = []; prev = 75; tot = dict(macs=0, w=0, b=0)
for nm, cin, cout, k, s, pad, lo in IM.SPEC:
    macs = cin * cout * k * lo; w = cin * cout * k; rows.append(dict(layer=nm, out_channels=cout, out_length=lo, macs=macs, weights=w, biases=cout, int8_weight_bytes=w, int32_bias_bytes=4 * cout, requant_const_bytes=5 * cout, out_activation_bytes=cout * lo))
    tot["macs"] += macs; tot["w"] += w; tot["b"] += cout
rows.append(dict(layer="fc (after GAP sum)", out_channels=2, out_length=1, macs=32, weights=32, biases=2, int8_weight_bytes=32, int32_bias_bytes=8, requant_const_bytes=0, out_activation_bytes=8)); tot["macs"] += 32; tot["w"] += 32; tot["b"] += 2
df = pd.DataFrame(rows); acts = [r["out_activation_bytes"] for r in rows[:3]]; peak = max(75 + acts[0], acts[0] + acts[1], acts[1] + acts[2])
df["label"] = "Calculated"; tail = dict(layer="TOTAL", macs=tot["macs"], weights=tot["w"], biases=tot["b"], int8_weight_bytes=df.int8_weight_bytes.sum(), int32_bias_bytes=df.int32_bias_bytes.sum(), requant_const_bytes=df.requant_const_bytes.sum(),
            peak_pingpong_activation_bytes=peak, total_flash_bytes=int(df.int8_weight_bytes.sum() + df.int32_bias_bytes.sum() + df.requant_const_bytes.sum()), ideal_cycles_2MAC=tot["macs"] / 2, ideal_time_us_at_128MHz=tot["macs"] / 2 / 128e6 * 1e6,
            label="Calculated, ideal lower bound; real firmware is slower")
df = pd.concat([df, pd.DataFrame([tail])]); df.to_csv("results/c3_layers.csv", index=False); print(df.T)
# figure
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sf, si, y = pickle.load(open("data/edge/quant/scatter_f0.pkl", "rb")); fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
sub = np.random.default_rng(0).choice(len(sf), 5000, replace=False); ax[0].scatter(sf[sub], si[sub] * meta["fc"]["logit_scale"], s=2); ax[0].plot([-15, 15], [-15, 15], "r:"); ax[0].set_xlabel("float score"); ax[0].set_ylabel("INT8 score (rescaled)"); ax[0].set_title("Fold 0, seed 0: float vs INT8 score (5000 test beats)")
from sklearn.metrics import roc_curve
for nm, s in (("float", sf), ("INT8", si)): f, t, _ = roc_curve(y, s); ax[1].plot(f, t, label=nm)
ax[1].set_xlim(0, .1); ax[1].set_xlabel("false-positive rate"); ax[1].set_ylabel("sensitivity (beats)"); ax[1].legend(); ax[1].set_title("Fold 0 ROC, low-FPR part")
plt.tight_layout(); plt.savefig("results/fig_c3_int8.png", dpi=110)
