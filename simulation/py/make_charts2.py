"""Round-2 figures (results/fig_b2_*, fig_b3_*, fig_b4_*, fig_a1_*, fig_a3_*, fig_a4_*, fig_b5_*).  A chart is drawn only if its CSV exists.   python py/make_charts2.py
Same palette as make_charts.py (reference categorical palette slots: blue, orange, aqua, magenta); light surface; one axis per chart; thin marks."""
import os, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, AQUA, MAG, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#e87ba4", "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 130, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True})
R = "results"; have = lambda f: os.path.exists(f"{R}/{f}")


def save(fig, name): fig.tight_layout(); fig.savefig(f"{R}/{name}", facecolor="#fcfcfb"); plt.close(fig); print("wrote", name)


if have("b2_scales_nstdb.csv"):
    d = pd.read_csv(f"{R}/b2_scales_nstdb.csv"); d = d[(d.segment == "noisy") & d.variant.str.contains("scaled|E1")]
    d["scale"] = d.variant.str.extract(r"scale(\d+)")[0].astype(int)
    g = d.groupby(["scale", "snr_db"]).agg(sens=("sens", "mean"), ppv=("ppv", "mean"), rail=("pct_samples_clipped", "mean")).reset_index()
    fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.8), sharex=True)
    for sc, col in zip([16, 8, 4, 2], [BLUE, ORANGE, AQUA, MAG]):
        x = g[g.scale == sc].sort_values("snr_db")
        for a_, k in zip(ax, ("sens", "ppv")): a_.plot(x.snr_db, x[k], color=col, lw=2, marker="o", ms=4, label=f"{sc} codes/uV (rail at -6 dB: {x[x.snr_db == -6].rail.iloc[0]:.1f}%)")
    ax[0].set_ylabel("% of beats found (sensitivity)"); ax[1].set_ylabel("% of detections correct (PPV)")
    for a_ in ax: a_.set_xlabel("SNR of the added real noise (dB)")
    ax[0].legend(frameon=False, fontsize=7.5, loc="lower right"); fig.suptitle("B2: NSTDB records 118 and 119 (noisy minutes), MIN_THR scaled with the ADC scale", x=0.01, ha="left", fontsize=10, color=INK)
    save(fig, "fig_b2_scales.png")

if have("b3_test.csv"):
    d = pd.read_csv(f"{R}/b3_test.csv"); d = d[d.loss_frac == 0.15]
    fig, ax = plt.subplots(figsize=(7.5, 3.8)); y = np.arange(len(d))[::-1]
    ax.barh(y, d.per_person_hour, color=BLUE, height=0.55)
    for yy, v, n in zip(y, d.per_person_hour, d.false_arms): ax.text(v + 0.01, yy, f"{v:.2f}  ({n} false arms)", va="center", fontsize=8, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([c.replace("PRE-SPECIFIED: ", "") for c in d.config], fontsize=8)
    ax.set_xlabel("false arms per person-hour (7 TEST people, 17.9 h; pulse-lost threshold 15%)"); ax.set_xlim(0, d.per_person_hour.max() * 1.45)
    ax.set_title("B3: arming conditions in living people (PPG-DaLiA)", loc="left", color=INK, fontsize=10); save(fig, "fig_b3_false_arms.png")

if have("a1_tune_grid.csv") and have("a1_test_grid_descriptive.csv"):
    t1 = pd.read_csv(f"{R}/a1_tune_grid.csv"); t2 = pd.read_csv(f"{R}/a1_test_grid_descriptive.csv"); cfg = json.load(open("configs/a1_frozen.json"))
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for df, mk, fc, lab in ((t1, "o", "none", "tune subjects (40)"), (t2, "o", BLUE, "test subjects (40)")):
        fam = df.config.str.startswith("rest_proxy")
        ax.scatter(df[fam].false_per_24h.clip(lower=0.03), df[fam].ischemic_sens, s=34, marker=mk, facecolors=fc, edgecolors=BLUE, linewidths=1.3, label=f"rest_proxy, {lab}")
        ax.scatter(df[~fam].false_per_24h.clip(lower=0.03), df[~fam].ischemic_sens, s=34, marker="s", facecolors=("none" if fc == "none" else ORANGE), edgecolors=ORANGE, linewidths=1.3, label=f"per-beat / averaged detector, {lab}")
    ax.set_xscale("log"); ax.set_xlabel("false check-ins per 24 h (outside labelled ST episodes; zero plotted at 0.03)"); ax.set_ylabel("share of ischemic episodes with a check-in")
    ax.axvline(1, color=MUTED, lw=1, ls=":"); ax.text(1.05, 0.95, "1 per 24 h", color=MUTED, fontsize=8)
    fz = t2[t2.config == cfg["selected_name"]]; ax.annotate("frozen choice (test)", (fz.false_per_24h.iloc[0], fz.ischemic_sens.iloc[0]), (2.2, 0.18), arrowprops=dict(arrowstyle="-", color=INK, lw=0.8), fontsize=8)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left"); ax.set_title("A1: LTSTDB heart-rate check-ins vs labelled ischemic ST episodes", loc="left", color=INK, fontsize=10); save(fig, "fig_a1_sens_vs_false.png")

if have("a3_test_fold10.csv"):
    d = pd.read_csv(f"{R}/a3_test_fold10.csv"); lo = d.AUC_95CI.str.split("-", expand=True).astype(float); d["lo"], d["hi"] = lo[0], lo[1]
    fig, ax = plt.subplots(figsize=(7.5, 4.4)); cols = {"heart rate only": MUTED, "ST only": BLUE, "all five": ORANGE}
    for i, (lead, g) in enumerate(d.groupby("lead", sort=False)):
        for j, (_, r) in enumerate(g.iterrows()):
            x = i + (j - 1) * 0.22; ax.errorbar(x, r.AUC, yerr=[[r.AUC - r.lo], [r.hi - r.AUC]], fmt="o", color=cols[r.features], ms=5, lw=1.4, capsize=2, label=r.features if i == 0 else None)
    ax.set_xticks(range(d.lead.nunique())); ax.set_xticklabels(d.lead.unique()); ax.set_ylabel("AUC, MI vs NORM, test fold 10 (95% CI)"); ax.axhline(0.5, color=MUTED, lw=1, ls=":")
    ax.legend(frameon=False, fontsize=8); ax.set_title("A3: PTB-XL resting 10-s ECGs, one lead at a time", loc="left", color=INK, fontsize=10); save(fig, "fig_a3_auc.png")

if have("a4_test_episodes.csv"):
    d = pd.read_csv(f"{R}/a4_test_episodes.csv"); d = d[d.record.str.startswith("sddb")]
    fig, ax = plt.subplots(figsize=(7.5, 3.8)); y = np.arange(len(d))[::-1]
    ax.barh(y, d.pct_seconds_with_beat_in_last_6s, color=BLUE, height=0.55)
    for yy, v in zip(y, d.pct_seconds_with_beat_in_last_6s): ax.text(v + 1, yy, f"{v:.0f}%", va="center", fontsize=8, color=INK)
    ax.set_yticks(y); ax.set_yticklabels(d.record.str.replace("sddb/", "record "), fontsize=8); ax.set_xlim(0, 112)
    ax.set_xlabel("% of seconds in the 5 min after VF onset with a detector 'beat' in the last 6 s (100% = the no-beat check never fires)")
    ax.set_title("A4: Verilog beat detector during real ventricular fibrillation (SDDB, 10 test records)", loc="left", color=INK, fontsize=10); save(fig, "fig_a4_vf_beats.png")

srcs = {"b5_sweep_slowfloor.csv": {"baseline": "baseline (fixed threshold 5)", "adaptive KN=8": "k=1.0, slow floor", "adaptive KN=12": "k=1.5, slow floor"},
        "b5_sweep_slow_final.csv": {"adaptive KN=14 UP=1 DOWN=9 HOLD=0": "k=1.75, slow floor", "adaptive KN=12 UP=1 DOWN=9 HOLD=1": "k=1.5, slow floor + 16 s holdoff"},
        "b5_sweep_fast.csv": {"adaptive KN=12 UP=16 DOWN=144": "k=1.5, fast floor"}}
parts = []
for f, m in srcs.items():
    if have(f):
        x = pd.read_csv(f"{R}/{f}"); x = x[(x.scenario == "S5 arrest") & x.variant.isin(m)]; x["label"] = x.variant.map(m); parts.append(x)
if parts:
    d = pd.concat(parts).drop_duplicates(["label", "acc_noise_ug"])
    fig, ax = plt.subplots(figsize=(8, 4)); order = ["baseline (fixed threshold 5)", "k=1.0, slow floor", "k=1.5, slow floor", "k=1.75, slow floor", "k=1.5, slow floor + 16 s holdoff", "k=1.5, fast floor"]
    cols = [MUTED, BLUE, ORANGE, AQUA, MAG, "#6250d6"]
    for k, v in enumerate(order):
        x = d[d.label == v].sort_values("acc_noise_ug")
        if len(x): ax.plot(x.acc_noise_ug + (k - 2.5) * 5, x.passed, marker="o", ms=4, lw=1.6, color=cols[k], label=v)
    ax.set_xlabel("simulated chest-accelerometer noise (ug RMS)"); ax.set_ylabel("arrest-scenario checks passed (of 7)"); ax.set_ylim(-0.3, 7.5)
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    ax.set_title("B5 (simulator): arrest scenario vs noise. Note: k=1.5 and 1.75 would call 95%+ of REAL living seconds 'still'", loc="left", color=INK, fontsize=9)
    save(fig, "fig_b5_noise.png")
