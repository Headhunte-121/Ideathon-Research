"""Fill py/report2_template.md from the round-2 CSVs -> ../docs/reports/REAL_DATA_REPORT_2.md.   python py/build_report2.py"""
import json, os, re
import numpy as np, pandas as pd

R = "results"; have = lambda f: os.path.exists(f"{R}/{f}")


def md(df):
    cols = list(df.columns); out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows(): out.append("| " + " | ".join("" if (isinstance(r[c], float) and np.isnan(r[c])) else str(r[c]) for c in cols) + " |")
    return "\n".join(out)


T = {}
# ---- B2
d = pd.read_csv(f"{R}/b2_scales_nstdb.csv"); n = d[(d.segment == "noisy") & d.snr_db.isin([12, 6, 0, -6])]
g = n.groupby(["variant", "snr_db"]).agg(sens=("sens", "mean"), ppv=("ppv", "mean"), rail=("pct_samples_clipped", "mean")).reset_index()
rows = []
for v in dict.fromkeys(n.variant):
    x = g[g.variant == v].set_index("snr_db")
    rows.append({"Variant": v, **{f"sens/PPV % at {s} dB": f"{x.loc[s, 'sens']:.1f} / {x.loc[s, 'ppv']:.1f}" for s in (12, 6, 0, -6)}, "samples on the rail % at -6 dB": f"{x.loc[-6, 'rail']:.1f}"})
T["<<B2>>"] = md(pd.DataFrame(rows))
# ---- B3
d = pd.read_csv(f"{R}/b3_test.csv")
t = d.pivot_table(index=["config", "hold_s", "wrist_still_x", "ecg_veto", "added_dispatch_delay_s"], columns="loss_frac", values="false_arms", aggfunc="first", sort=False).reset_index()
t15 = d[d.loss_frac == 0.15].set_index("config")
rows = [{"Configuration": r.config, "Hold (s)": r.hold_s, "Wrist still (x)": ("" if pd.isna(r.wrist_still_x) else int(r.wrist_still_x)), "ECG veto": "yes" if r.ecg_veto else "no", "Added delay (s)": r.added_dispatch_delay_s,
         "False arms at 10 / 15 / 25 %": f"{int(r[0.1])} / {int(r[0.15])} / {int(r[0.25])}", "Per person-hour (15 %)": f"{t15.loc[r.config, 'per_person_hour']:.2f}",
         "People affected (15 %)": int(t15.loc[r.config, "people_affected"]), "Worst person (15 %)": f"{t15.loc[r.config, 'worst_person']} ({int(t15.loc[r.config, 'worst_person_arms'])})"} for _, r in t.iterrows()]
T["<<B3>>"] = md(pd.DataFrame(rows))
# ---- B4
rows = []
for f, g_ in (("b4_tune.csv", "tune (8 people)"), ("b4_test.csv", "TEST (7 people)")):
    if not have(f): continue
    x = pd.read_csv(f"{R}/{f}")
    for _, r in x.iterrows():
        if f == "b4_tune.csv" and r.K != 4.5: pass
        rows.append({"Set": g_, "Stream": r.stream, "K": r.K, "People used": r.people_used, "False check-ins": r.false_checkins, "Stream hours": round(r.stream_hours, 1), "Caught +10%": r.caught_10pct,
                     "Caught +15%": r.caught_15pct, "Caught +25%": r.caught_25pct})
T["<<B4>>"] = md(pd.DataFrame(rows))
# ---- A1
cfg = json.load(open("configs/a1_frozen.json"))
x = pd.read_csv(f"{R}/a1_tune_grid.csv")
x = x[["config", "ischemic_episodes", "ischemic_caught", "ischemic_sens", "median_lead_min", "false_checkins", "false_per_24h", "fraction_records_with_false"]]
x.columns = ["Setting", "Ischemic episodes", "Caught", "Sensitivity", "Median lead (min, + = before onset)", "False check-ins", "False per 24 h", "Records with >= 1 false"]
x["Setting"] = [("**" + s + " (selected)**") if s == cfg["selected_name"] else s for s in x["Setting"]]
T["<<A1TUNE>>"] = md(x)
x = pd.read_csv(f"{R}/a1_test.csv")[["config", "ischemic_episodes", "ischemic_caught", "ischemic_sens", "median_lead_min", "rate_episodes", "rate_caught", "false_checkins", "nonepisode_hours", "false_per_24h", "records_with_false"]]
x.columns = ["Setting", "Ischemic episodes", "Caught", "Sensitivity", "Median lead (min)", "Heart-rate-related episodes", "Caught (HR-related)", "False check-ins", "Episode-free hours", "False per 24 h", "Records with >= 1 false"]
T["<<A1TEST>>"] = md(x)
if have("a1_hint.csv"):
    h = pd.read_csv(f"{R}/a1_hint.csv"); hh = h[["set", "records", "ischemic_episodes", "ischemic_sens", "median_lead_min", "false_per_24h", "fraction_records_with_false"]]
    T["<<A1HINT>>"] = "**ST hint (fixed rule, not tuned; `.16a` ST level at J+60 ms, deviation above 100 uV for 60 s):**\n\n" + md(hh)
else:
    T["<<A1HINT>>"] = "**The ST hint (database `.16a` ST measurements) was not run:** the LTSTDB raw-signal and ST-measurement files (about 7 GB) downloaded too slowly from PhysioNet and the team decided to skip them. Everything in A1 uses the complete annotation files (`.atr` beats, `.stc` episodes, `.hea`, `.cnt`)."
# ---- A2
x = pd.read_csv(f"{R}/a2_edb_test.csv")[["config", "records", "ST_change_episodes", "ST_change_caught", "ST_change_sens", "median_lead_min", "T_wave_episodes", "T_wave_caught", "false_checkins", "nonepisode_hours", "false_per_24h"]]
x["nonepisode_hours"] = x["nonepisode_hours"].round(1); x["false_per_24h"] = x["false_per_24h"].round(2)
T["<<A2>>"] = md(x)
# ---- A3
x = pd.read_csv(f"{R}/a3_test_fold10.csv")[["lead", "features", "AUC", "AUC_95CI", "sensitivity", "sens_95CI", "specificity", "spec_95CI"]]
x.columns = ["Lead", "Features", "AUC", "AUC 95% CI", "Sensitivity", "Sens. 95% CI", "Specificity", "Spec. 95% CI"]
T["<<A3>>"] = md(x)
# ---- A4
e = pd.read_csv(f"{R}/a4_test_episodes.csv"); f = pd.read_csv(f"{R}/a4_test_false_flags.csv")
e2 = e[["record", "kind", "onset_s", "beats_per_min", "median_bpm", "pct_seconds_with_beat_in_last_6s", "t_to_POD_s", "t_to_PROPOSAL_s"]].copy()
e2.columns = ["Record", "Kind", "Onset (s)", "Beats per min after onset", "Median bpm", "% seconds with a beat in last 6 s", "Pod 6 s no-beat rule fired after (s)", "Proposed flag fired after (s)"]
e2 = e2.fillna("never")
fs = f"\n\n**False flags in pre-onset sinus time (test records, {f.hours.sum():.0f} h):** Pod 6 s rule {f.POD_flags.sum()} ({f.POD_flags.sum()/f.hours.sum():.2f} per hour; worst record {f.loc[f.POD_per_h.idxmax(), 'record']} at {f.POD_per_h.max():.2f} per hour); proposed flag {f.PROPOSAL_flags.sum()} ({f.PROPOSAL_flags.sum()/f.hours.sum():.2f} per hour; worst record {f.loc[f.PROPOSAL_per_h.idxmax(), 'record']} at {f.PROPOSAL_per_h.max():.2f} per hour; excluding that record {(f.PROPOSAL_flags.sum()-f.PROPOSAL_flags.max())/(f.hours.sum()-f.loc[f.PROPOSAL_flags.idxmax(), 'hours']):.2f} per hour). Records with no VF onset: {', '.join(f[~f.has_vf_onset].record)}."
T["<<A4>>"] = md(e2) + fs
# ---- B5
srcs = [("b5_sweep_slowfloor.csv", "UP 1, DOWN 9, no holdoff, first run"), ("b5_sweep_slow_final.csv", "UP 1, DOWN 9, final run"), ("b5_sweep_fast.csv", "UP 16, DOWN 144, no holdoff"), ("b5_sweep_hold.csv", "UP 16, DOWN 144, 16 s holdoff")]
parts = []
for fn, tag in srcs:
    if not have(fn): continue
    x = pd.read_csv(f"{R}/{fn}"); x["variant"] = [("baseline (unchanged)" if v == "baseline" else re.sub(r" UP=\d+ DOWN=\d+( HOLD=\d)?", lambda m_: (" HOLD=" + m_.group(1).split("=")[1]) if m_.group(1) else "", v) + f" [{tag}]") for v in x.variant]; parts.append(x)
if parts:
    x = pd.concat(parts).drop_duplicates(["variant", "acc_noise_ug", "scenario"])
    sc = {"S1 normal rest": "S1", "S3 watch loose (living)": "S3", "S5 arrest": "S5"}
    rows = []
    for v in dict.fromkeys(x.variant):
        row = {"Variant": v}
        for nz in (350, 500, 650, 800, 1000):
            y = x[(x.variant == v) & (x.acc_noise_ug == nz)].set_index("scenario").passed
            row[f"{nz} ug"] = "/".join(str(int(y.get(k, -1))) if k in y.index else "-" for k in sc)
        rows.append(row)
    full = [pd.read_csv(f"{R}/{f}") for f in ("b5_full_350.csv", "b5_full_800.csv") if have(f)]
    fulltxt = "; ".join(f"{r.variant} at {r.acc_noise_ug} ug: {r.passed}/{r.passed+r.failed}" for df_ in full for _, r in df_.iterrows())
    T["<<B5>>"] = "Checks passed in scenarios **S1 / S3 / S5** (maximum 8 / 2 / 7) at each simulated accelerometer noise (RMS):" + chr(10)*2 + md(pd.DataFrame(rows)) + chr(10)*2 + "![B5](fig_b5_noise.png)" + chr(10)*2 + "Full 35-check system run (Simulated): " + fulltxt + "."
else:
    T["<<B5>>"] = "(sweep results missing)"
# ---- B5 CEBS emulation
if have("b5_cebs_emulation.csv"):
    x = pd.read_csv(f"{R}/b5_cebs_emulation.csv"); x = x[x.chest_sensitivity == "660 mV/g"]
    x = x.assign(Tracker=np.where(x.UP == 1, "UP 1, DOWN 9", "UP 16, DOWN 144"))[["Tracker", "k", "living_seconds_called_still_pct_mean", "worst_person_pct", "people_over_5pct", "people"]]
    x.columns = ["Floor tracker", "k", "Living seconds called still, % (mean)", "Worst person, %", "People above 5%", "People"]
    T["<<B5CEBS>>"] = md(x)
else:
    T["<<B5CEBS>>"] = "(emulation missing)"
# ---- poster table
may = [
    ("B3", "In 17.9 person-hours of living people (7 test people), wrist pulse loss with a quiet chest held for 3 s occurred 13 times (2 people); an ECG-beat veto removed all 13 and a 10 s hold removed them at the default threshold (7 s slower). The veto would also suppress pulseless electrical activity. Not an independent test.", "Replayed (PPG-DaLiA)"),
    ("B2", "The beat detector misses about 20% (0 dB) to 40% (-6 dB) of beats in heavy real noise and 40-55% of its detections are wrong; this is not an ADC-scaling artefact.", "Replayed (NSTDB, 2 records)"),
    ("B4", "Feeding only resting beats to the unchanged drift detector did not let it detect +10 to +25% heart-rate steps in 7 people (about 2 h each).", "Replayed + Simulated step (PPG-DaLiA)"),
    ("A1", "A heart-rate drift check (tuned on 40 patients, tested on 40 other patients, 43 records) caught 8 of 178 ischemic ST episodes at 1.07 false check-ins per 24 h; catching most episodes costs tens of false check-ins per day. Most episodes follow heart-rate rises.", "Replayed (LTSTDB)"),
    ("A2", "The same setting, unchanged, caught 3.8% of ST-change episodes in 75 two-hour recordings of a second database (15 overlapping records excluded); the false-alarm rate is too uncertain to quote.", "Replayed (EDB)"),
    ("A3", "On 10-second resting 12-lead ECGs (test fold 10, 1462 ECGs), ST level and slope alone give an AUC of 0.59 to 0.77 for MI vs normal depending on the lead; five simple features give 0.71 to 0.86. Not early warning, not wearable.", "Replayed (PTB-XL, Python)"),
    ("A4", "On real recordings of ventricular fibrillation (10 test records) the beat detector kept finding beats in the fibrillation waves, so a 6 s 'no beat' rule fired within 5 minutes in only 5 of 10 records. ECG only; not representative of our device.", "Replayed (SDDB, Verilog on windows)"),
    ("B5", "A fixed 'chest still' threshold stops recognising a chest with no heartbeat once simulated sensor noise reaches about 0.65-0.8 mg RMS; the real chip's noise was not verified.", "Simulated (end-to-end testbench)"),
    ("B5", "In the simulator a fixed 'chest still' threshold fails to recognise a chest with no heartbeat once sensor noise reaches about 0.65-0.8 mg RMS. An adaptive threshold that fixes this in the simulator would call 95% of real resting seconds 'still' (emulated on 40 recordings), so it is not adopted.", "Simulated + Replayed emulation (CEBS)"),
]
T["<<POSTERMAY>>"] = md(pd.DataFrame(may, columns=["Result", "Exact wording", "Label"]))
# ---- assumptions
A = [
    "SDDB `vfon` header times are elapsed time from the record start (checked on five records by the detector's beat count and ECG amplitude; record 52 unclear).",
    "CUDB episodes run from a `(VT` / `(VF` rhythm annotation to the next rhythm change; CUDB onsets are hard to pin down (per its documentation).",
    "SDDB/CUDB records are treated as patients (no patient identifiers are given); the SDDB analysis window is onset -10 min to +5 min.",
    "Invalid ADC samples (NaN) in SDDB/CUDB are forward-filled; counts are in the logs.",
    "The ECG front end is emulated as 250 Hz, 16 codes/uV, 0.5 Hz AC coupling, channel 0 (same as rounds 1 and 2); the Python beat-detector port is not bit-exact (scores within 0.12 percentage points of the Verilog on clean ECG, up to 2.8 in heavy noise).",
    "The Pod's ECG fallback is `nobeat_s >= 6` (from `pod_node.sv`); the Pod only uses it when the wrist band is silent. The A4 rate rule (above 180 or below 30 bpm over 5 s or 10 s) and the irregularity score (CV of the last 8 RR intervals) are proposals.",
    "LTSTDB: `.stc` criterion set (100 uV, 60 s); episode types from the annotation legend: `(stN` ischemic, `(rtstN` heart-rate-related; axis-shift marks counted separately; false-alarm time excludes every labelled ST episode +/- 30 min; the heart-rate rest proxy (rolling 5th percentile over 10 min, 60 s mean heart rate) is an assumed stand-in for a motion channel.",
    "LTSTDB heart rate comes from the database's manually corrected `.atr` beats, RR within 0.3-2.0 s; learning 2^13 beats for the per-beat detector variants.",
    "EDB overlap: ten LTSTDB headers name EDB records; the same-subject EDB records come from the EDB description; EDB positive class = ST-change episodes (it does not label ischemic origin).",
    "PTB-XL: MI = any diagnostic SCP code in the MI superclass; NORM = all diagnostic codes NORM (9069 records, fewer than the 9514 normal ECGs in the dataset summary because mixed-label records are dropped); ST level is measured at R+110 ms relative to the PR segment (R-80..-40 ms), a stand-in for J+60 ms; 100 Hz records resampled to 250 Hz.",
    "PPG-DaLiA: pulse lost = pulse size below 15% of the person's own sitting median (checked at 10% and 25%); chest moving = above 5x the sitting median; wrist still = wrist accelerometer variation at most X times the sitting median; ECG veto = a Verilog-detector beat at 30-180 bpm in the last 3 s.",
    "Round-1 tune/test split for DaLiA (S1-S8 / S9-S15) was replaced by the seeded split in `splits/dalia_split.json`; S5 and S8 (the people with all the false arms) were examined in round 1 and fall in the test group now, so B3's pre-specified variants are not an independent test.",
    "B4 learns on the first 1024 beats (LOG2N = 10, about 13 min) of each stream and injects steps on rest beats after 60% of the rest stream.",
    "B5 variant: floor = 10th percentile tracker, k = KN/8, updated only while the wrist pulse is present; the end-to-end testbench's patient and noise models are our own; scenario subsets S1, S3, S5 at each noise level, the full 35 checks only at 350 ug.",
    "B6: the LSM6DSOX datasheet could not be opened; no value from it is used.",
    "Downloads: PhysioNet databases fetched with `py/download_physionet.py`. LTSTDB: only `.hea`, `.atr`, `.stc`, `.cnt` are complete for all 86 records; the raw ECG (`.dat`), `.16a`, `.sta/.stb/.stf/.ari` were NOT downloaded in full (too slow; skipped by decision), so the A1 ST hint was not run. PTB-XL: the 100 Hz records are complete; the 500 Hz records were not needed. Licences: Open Data Commons Attribution v1.0 (PhysioNet sets), CC BY 4.0 (PTB-XL, PPG-DaLiA).",
    "Git: frozen configs and split files were committed locally only (no push), as the user confirmed.",
]
T["<<ASSUMPTIONS>>"] = "\n".join(f"{i+1}. {a}" for i, a in enumerate(A))
# ---- regression
reg = [l.strip() for l in open(f"{R}/round2_regression_run.txt", errors="ignore").read().replace("\r", "").splitlines() if "passed" in l]
T["<<REGRESSION>>"] = "`run_vivado.bat` re-run at the end of round 2 (Vivado xsim 2025.2), the baseline files unchanged:\n\n```\n" + "\n".join(reg) + "\n```\n\nExpected: 22/22, 20/20, 35/35, mutation A fails 16 of 35, mutation B fails 1 of 35 (matches)."
tmpl = open("py/report2_template.md", encoding="utf-8").read()
NL = chr(10)
m = re.search("### 1.2 Must not say" + NL + NL + "(.*?)" + NL + NL + "## 2[.]", tmpl, re.S)
head = "# Poster wording from round 2 (copy only accepted lines; full context in REAL_DATA_REPORT_2.md)" + NL + NL + "## May say" + NL + NL
open("../docs/reports/POSTER_EVIDENCE_ROUND2.md", "w", encoding="utf-8").write(head + T["<<POSTERMAY>>"] + NL + NL + "## Must not say" + NL + NL + (m.group(1) if m else "") + NL)
rep = tmpl
for k, v in T.items(): rep = rep.replace(k, v)
open("../docs/reports/REAL_DATA_REPORT_2.md", "w", encoding="utf-8").write(rep); print("wrote docs/reports/REAL_DATA_REPORT_2.md", len(rep), "chars;", "unfilled markers:", re.findall(r"<<[A-Z0-9]+>>", rep))
