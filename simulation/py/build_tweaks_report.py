"""Fill py/tweaks_template.md from the tweak CSVs -> ../docs/reports/TWEAKS_REPORT.md.   python py/build_tweaks_report.py"""
import pandas as pd

def md(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)

# T1
d = pd.read_csv("results/tweak1_false_starts.csv")
t = d.pivot_table(index=["hold_s", "wrist_still_x", "ecg_no_beat_3s", "added_delay_s"], columns="group",
                  values=["false_starts", "per_person_hour"], aggfunc="first").reset_index()
t.columns = [" ".join(str(x) for x in c).strip() for c in t.columns.values]
t1 = pd.DataFrame({"Hold (s)": t["hold_s"], "Wrist still (x sitting)": t["wrist_still_x"], "No ECG beat 3 s": t["ecg_no_beat_3s"],
                   "Added delay (s)": t["added_delay_s"],
                   "Tune S1-S8: starts (per person-h)": [f"{int(a)} ({b})" for a, b in zip(t["false_starts tune S1-S8"], t["per_person_hour tune S1-S8"])],
                   "Test S9-S15: starts (per person-h)": [f"{int(a)} ({b})" for a, b in zip(t["false_starts test S9-S15"], t["per_person_hour test S9-S15"])]})
t1["Hold (s)"] = t1["Hold (s)"].astype(str)
t1.loc[(t1["Hold (s)"] == "3") & (t1["Wrist still (x sitting)"].astype(str) == "-") & (t1["No ECG beat 3 s"] == "no"), "Hold (s)"] = "3 (BEFORE)"
# T2
d2 = pd.read_csv("results/tweak2_resting_drift.csv")
t2 = d2[["setup", "group", "rule", "param", "false_alarms", "false_alarms_per_rest_hour", "people_with_false_alarm",
         "detected_step_10pct", "detected_step_15pct", "detected_step_25pct"]].copy()
t2.columns = ["Setup", "Group", "Rule", "Parameter", "False alarms", "per rest-hour", "People with a false alarm", "Caught +10%", "Caught +15%", "Caught +25%"]
t2["Setup"] = t2["Setup"].str.replace(" (labels used: upper bound)", " (upper bound)", regex=False)
# T3
d3 = pd.read_csv("results/tweak3_scale_nstdb.csv"); d3 = d3[(d3.segment == "noisy") & (d3.snr_db.isin([12, 6, 0, -6]))]
g = d3.groupby(["variant", "snr_db"]).agg(clip=("pct_samples_clipped", "mean"), sens=("sens", "mean"), ppv=("ppv", "mean")).reset_index()
g = g.sort_values(["variant", "snr_db"], ascending=[True, False])
t3 = pd.DataFrame({"Variant": g.variant, "Noise SNR (dB)": g.snr_db, "Samples at the rail %": g["clip"].round(1), "Sensitivity %": g["sens"].round(1), "PPV %": g.ppv.round(1)})
# T4
d4 = pd.read_csv("results/tweak4_adaptive_still.csv")
t4 = pd.DataFrame({"Sensor noise (ug RMS)": d4.sensor_noise_ug_rms,
                   "Living called still, fixed %": d4.living_seconds_called_still_fixed_pct, "Living called still, adaptive % (worst person)":
                   [f"{a} ({b})" for a, b in zip(d4.living_seconds_called_still_adaptive_pct, d4.living_worst_person_adaptive_pct)],
                   "No-heartbeat chest recognised, fixed %": d4.no_heartbeat_called_still_fixed_pct, "No-heartbeat chest recognised, adaptive %": d4.no_heartbeat_called_still_adaptive_pct})
# T5
d5 = pd.read_csv("results/tweak5_early_beat.csv")
def m(v, st, ds, col):
    r = d5[(d5.variant == v) & (d5.set.isin(st)) & (d5.dataset == ds)][col]; return round(r.mean(), 2)
rows = []
for v in ["none", "0.5/2", "0.6/2", "0.7/3"]:
    rows.append({"Variant (fraction / slope multiple)": v,
                 "Tune 118 noisy: sens / PPV": f"{m(v,['tune'],'NSTDB noisy','sens')} / {m(v,['tune'],'NSTDB noisy','ppv')}",
                 "Test 119 noisy: sens / PPV": f"{m(v,['test'],'NSTDB noisy','sens')} / {m(v,['test'],'NSTDB noisy','ppv')}",
                 "18 clean NSRDB: sens / PPV": f"{m(v,['test'],'NSRDB clean','sens')} / {m(v,['test'],'NSRDB clean','ppv')}"})
t5 = pd.DataFrame(rows)
rep = open("py/tweaks_template.md", encoding="utf-8").read()
for k, v in {"<<T1>>": md(t1), "<<T2>>": md(t2), "<<T3>>": md(t3), "<<T4>>": md(t4), "<<T5>>": md(t5)}.items():
    rep = rep.replace(k, v)
open("../docs/reports/TWEAKS_REPORT.md", "w", encoding="utf-8").write(rep); print("wrote docs/reports/TWEAKS_REPORT.md", len(rep), "chars")
