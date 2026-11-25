"""Charts for results/REAL_DATA_REPORT.md.  Reads the CSVs in results/, writes PNGs to results/figures/.
Colours: first slots of the reference categorical palette (blue, orange, aqua); light surface; one axis per chart.
  python py/make_charts.py"""
import os, re
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, AQUA, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 130,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True})
R = "results"


def save(fig, name):
    fig.tight_layout(); fig.savefig(f"{R}/{name}", facecolor="#fcfcfb"); plt.close(fig); print("wrote", f"{R}/{name}")


# ---- E1: beat detector vs noise (NSTDB, noisy segments only) -------------------------------------------------------
d = pd.read_csv(f"{R}/real_ecg_nstdb.csv")
d = d[d.segment == "noisy"].copy()
d["snr"] = d.record.map(lambda r: -6 if r.endswith("e_6") else int(re.search(r"e(\d+)$", r).group(1)))
d["person"] = d.record.str[:3]
fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
for ax, (person, g) in zip(axes, d.groupby("person")):
    g = g.sort_values("snr")
    ax.plot(g.snr, g.sens, color=BLUE, lw=2, marker="o", ms=5, mec="#fcfcfb", mew=1.5)
    ax.plot(g.snr, g.ppv, color=ORANGE, lw=2, marker="o", ms=5, mec="#fcfcfb", mew=1.5)
    ax.text(g.snr.iloc[0] + 0.5, g.sens.iloc[0] + 3, "sensitivity", color=BLUE, fontsize=9)
    ax.text(g.snr.iloc[0] + 0.5, g.ppv.iloc[0] - 7, "positive predictivity", color=ORANGE, fontsize=9)
    ax.set_title(f"NSTDB record {person}, noisy minutes only", loc="left", color=INK, fontsize=10)
    ax.set_xlabel("signal-to-noise ratio of the added real noise (dB)")
    ax.set_ylim(35, 102)
axes[0].set_ylabel("% of beats")
save(fig, "fig_e1_beat_detector_vs_snr.png")

# ---- E2: beat detector on 18 clean recordings ----------------------------------------------------------------------
d = pd.read_csv(f"{R}/real_ecg_nsrdb.csv").sort_values("ppv")
fig, ax = plt.subplots(figsize=(8, 4.2))
y = np.arange(len(d))
ax.hlines(y, d.ppv, d.sens, color=GRID, lw=3)
ax.plot(d.sens, y, "o", color=BLUE, ms=6, mec="#fcfcfb", mew=1.5, label="sensitivity")
ax.plot(d.ppv, y, "o", color=ORANGE, ms=6, mec="#fcfcfb", mew=1.5, label="positive predictivity")
ax.set_yticks(y); ax.set_yticklabels(d.record); ax.set_xlim(97.5, 100.2)
ax.set_xlabel("% of beats (30 min per person, NSRDB)"); ax.legend(frameon=False, loc="lower left")
ax.set_title("E2: beat detector, 18 real clean recordings", loc="left", color=INK)
save(fig, "fig_e2_beat_detector_clean.png")

# ---- E3: drift detector -------------------------------------------------------------------------------------------
v = pd.read_csv(f"{R}/drift_variants.csv")
v["K"] = v["K"].map(lambda x: f"{float(x):.1f}")
r = v[v.variant == "rtl"]
piv = r.pivot(index="record", columns="K", values="per24h")
fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(len(piv)); w = 0.27
for i, (k, col) in enumerate(zip(["3.0", "3.8", "4.5"], [BLUE, ORANGE, AQUA])):
    ax.bar(x + (i - 1) * w, piv[k], w - 0.04, color=col, label=f"K = {k}")
ax.axhline(1, color=MUTED, lw=1, ls=":"); ax.text(len(piv) - 0.5, 1.03, "target: at most 1 per 24 h", ha="right", color=MUTED, fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(piv.index, rotation=60, fontsize=8)
ax.set_ylabel("false check-ins per 24 h"); ax.legend(frameon=False)
ax.set_title("E3: drift detector on ~20 h of real heart rate per person (NSRDB, 18 people)", loc="left", color=INK, fontsize=10)
save(fig, "fig_e3_false_checkins_per_person.png")

fig, ax = plt.subplots(figsize=(7.5, 4))
for k, col in zip(["3.0", "3.8", "4.5"], [BLUE, ORANGE, AQUA]):
    ys = []
    for pct in [10, 15, 25]:
        g = r[r.K == k]; ys.append(100 * (pd.to_numeric(g[f"delay_min_{pct}pct"], errors="coerce").notna().mean()))
    ax.plot([10, 15, 25], ys, color=col, lw=2, marker="o", ms=6, mec="#fcfcfb", mew=1.5, label=f"K = {k}")
ax.set_xticks([10, 15, 25]); ax.set_ylim(-2, 100)
ax.set_xlabel("injected step in heart rate, last quarter of each recording (%)"); ax.set_ylabel("% of the 18 people flagged")
ax.legend(frameon=False, loc="upper left")
ax.set_title("E3: how often a sustained heart-rate shift is caught (as built)", loc="left", color=INK, fontsize=10)
save(fig, "fig_e3_detection_vs_shift.png")

# ---- E4: chest vibration energy of living, resting people vs the 'still' threshold ---------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [1.1, 1]})
ax = axes[0]
for name, col, lab in [("e4_scg_baseline_660mVg", BLUE, "660 mV/g (datasheet, +/-2 g range)"),
                       ("e4_scg_baseline_220mVg", AQUA, "220 mV/g (datasheet, +/-6 g range)")]:
    s = pd.read_csv(f"{R}/{name}_seconds.csv")
    ax.hist(s.energy_codes, bins=np.logspace(0, 2.4, 70), color=col, alpha=0.75, label=lab)
ax.set_ylim(0, 900); ax.axvline(5, color=ORANGE, lw=2)
ax.text(4.5, 450, "'chest still' threshold = 5", color=ORANGE, fontsize=9, rotation=90, ha="right", va="center")
ax.set_xscale("log"); ax.set_xlabel("chest vibration, mean |a| per second (codes of 122 µg)")
ax.set_ylabel("seconds (20 people x 5 min, lying at rest)"); ax.legend(frameon=False, fontsize=8, loc="upper right")
ax.set_title("E4: living people never look 'still'", loc="left", color=INK, fontsize=10)
ax = axes[1]
b = pd.read_csv(f"{R}/e4_scg_baseline_660mVg.csv").sort_values("median")
y = np.arange(len(b))
ax.hlines(y, b.p1, b["median"], color=GRID, lw=3)
ax.plot(b["median"], y, "o", color=BLUE, ms=5, mec="#fcfcfb", mew=1.2, label="median second")
ax.plot(b.p1, y, "o", color=MUTED, ms=4, mec="#fcfcfb", mew=1.0, label="weakest 1% of seconds")
ax.axvline(5, color=ORANGE, lw=2)
ax.set_yticks(y); ax.set_yticklabels(b.record, fontsize=7); ax.set_xlabel("codes (660 mV/g)")
ax.legend(frameon=False, fontsize=8, loc="lower right"); ax.set_title("per person", loc="left", color=INK, fontsize=10)
save(fig, "fig_e4_chest_vibration_vs_still_threshold.png")

# ---- E5: wrist pulse loss and motion (only if the DaLiA run exists) ---------------------------------------------------
p = f"{R}/real_ppg_dalia.csv"
if os.path.exists(p):
    d = pd.read_csv(p)
    t = d.assign(l=d.pct_lost_and_still * d.seconds, s=d.seconds).groupby("activity")[["l", "s"]].sum()
    t["pct"] = t.l / t.s; t = t.sort_values("pct")      # pct_lost_and_still is already a percentage: seconds-weighted mean, no extra x100
    fig, ax = plt.subplots(figsize=(7, 4))
    t = t.drop(index=[a for a in ["walking","cycling","stairs"] if a in t.index])   # motion artefact masks pulse loss there
    ax.barh(t.index, t.pct, color=BLUE, height=0.55)
    for i, v in enumerate(t.pct): ax.text(v + 0.015 * t.pct.max(), i, f"{v:.2f}%", va="center", color=INK, fontsize=9)
    ax.set_xlabel("% of the seconds of that activity (15 people pooled): wrist pulse lost AND chest not moving", fontsize=8)
    ax.set_title("E5: PPG-DaLiA, 15 people, by activity", loc="left", color=INK, fontsize=10)
    save(fig, "fig_e5_pulse_lost_and_still_by_activity.png")
