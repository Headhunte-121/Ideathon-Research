"""E5 follow-up: how many EPISODES (>= HOLD consecutive seconds) of 'wrist pulse lost AND chest not moving' occur in living people?
The Pod arms its 30 s cancel window only if both hold for 3 s, so isolated seconds matter less than runs.
Reads results/real_ppg_dalia_seconds.csv; writes results/e5_episodes.csv.  python py/e5_episodes.py [--hold 3]"""
import argparse, numpy as np, pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--hold", type=int, default=3); a = ap.parse_args()
d = pd.read_csv("results/real_ppg_dalia_seconds.csv")
ACT = {1: "sitting", 2: "stairs", 3: "table soccer", 4: "cycling", 5: "driving", 6: "lunch", 7: "walking", 8: "working", 0: "transient"}
rows = []
for s, g in d.groupby("subject"):
    f = ((g.pulse_lost == 1) & (g.moving == 0)).to_numpy(); act = g.activity.to_numpy()
    i = 0
    while i < len(f):
        if f[i]:
            j = i
            while j < len(f) and f[j]: j += 1
            rows.append(dict(subject=int(s), start_s=int(g.second.iloc[i]), length_s=j - i, activity=ACT[int(act[i])]))
            i = j
        else: i += 1
e = pd.DataFrame(rows); e.to_csv("results/e5_episodes.csv", index=False)
hours = len(d) / 3600.0; arm = e[e.length_s >= a.hold]
print(f"living people: 15, {hours:.1f} person-hours; runs of pulse-lost & chest-still: {len(e)}; runs >= {a.hold} s (would ARM the 30 s cancel window): {len(arm)}")
if len(arm):
    print(arm.sort_values("length_s", ascending=False).head(10).to_string(index=False))
    print("arming episodes per person-hour: %.2f; people affected: %d of 15; longest: %d s" % (len(arm) / hours, arm.subject.nunique(), arm.length_s.max()))
    print(arm.groupby("activity").size().to_string())
else: print("no episode long enough to arm")
