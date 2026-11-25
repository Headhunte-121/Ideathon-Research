"""Tweak 1, step 2: which extra condition / longer hold stops living people from starting the 30 s countdown?
Reads data/dalia_feats/S*.npz (py/tweak1_features.py).  Tune on S1-S8, test on S9-S15 (split fixed before looking at any result).
A "false start" = a run of at least H consecutive seconds in which ALL of these hold for a LIVING person:
   wrist pulse lost  AND  chest not moving  [AND wrist not moving (wrist_rel <= X)]  [AND no chest-ECG beat for >= 3 s]
Cost of each rule for a real arrest (all conditions true from t=0): dispatch is delayed to H seconds (baseline H = 3 s).
Selection is made on the TUNE people only (lowest false starts per person-hour, then shortest hold, then fewest conditions);
the same rule is then reported on the TEST people.   Output: results/tweak1_false_starts.csv, results/tweak1_selection.txt"""
import csv, glob, itertools, os
import numpy as np

TUNE = list(range(1, 9)); TEST = list(range(9, 16))
HOLDS = (3, 5, 10); WRIST_X = (None, 3, 5, 10); ECG = (False, True)
F = {s: np.load(f"data/dalia_feats/S{s}.npz") for s in TUNE + TEST}


def episodes(cond, hold):
    n = 0; run = 0; longest = 0
    for v in cond:
        if v: run += 1
        else:
            if run >= hold: n += 1
            longest = max(longest, run); run = 0
    if run >= hold: n += 1
    longest = max(longest, run)
    return n, longest


def cond_for(f, wx, ecg):
    c = f["lost"] & ~f["chest_moving"]
    if wx is not None: c = c & (f["wrist_rel"] <= wx)
    if ecg: c = c & (f["ecg_age"] >= 3.0)
    return c


rows = []
for H, wx, ecg in itertools.product(HOLDS, WRIST_X, ECG):
    for group, subs in (("tune S1-S8", TUNE), ("test S9-S15", TEST)):
        per = {s: episodes(cond_for(F[s], wx, ecg), H)[0] for s in subs}
        hours = sum(len(F[s]["label"]) for s in subs) / 3600.0
        tot = sum(per.values())
        rows.append(dict(group=group, hold_s=H, wrist_still_x=("-" if wx is None else wx), ecg_no_beat_3s=("yes" if ecg else "no"),
                         false_starts=tot, person_hours=round(hours, 1), per_person_hour=round(tot / hours, 3),
                         people_affected=sum(1 for v in per.values() if v > 0), worst_person_starts=max(per.values()),
                         worst_person=max(per, key=per.get), added_delay_s=H - 3))
with open("results/tweak1_false_starts.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

tune = [r for r in rows if r["group"].startswith("tune")]
def key(r):
    nconds = (r["wrist_still_x"] != "-") + (r["ecg_no_beat_3s"] == "yes")
    return (r["per_person_hour"], r["hold_s"], nconds)
best = min(tune, key=key)
sel = [r for r in rows if (r["hold_s"], r["wrist_still_x"], r["ecg_no_beat_3s"]) == (best["hold_s"], best["wrist_still_x"], best["ecg_no_beat_3s"])]
base = [r for r in rows if (r["hold_s"], r["wrist_still_x"], r["ecg_no_beat_3s"]) == (3, "-", "no")]
lines = ["BEFORE (as tested in E5: pulse lost AND chest not moving, hold 3 s):"] + [f"  {r['group']}: {r['false_starts']} false starts in {r['person_hours']} person-h = {r['per_person_hour']}/h, people affected {r['people_affected']}, worst person S{r['worst_person']} ({r['worst_person_starts']})" for r in base]
lines += ["", f"SELECTED ON THE TUNE PEOPLE ONLY: hold {best['hold_s']} s, wrist-still x={best['wrist_still_x']}, ECG no-beat 3 s = {best['ecg_no_beat_3s']} (added dispatch delay {best['added_delay_s']} s)"]
lines += [f"  {r['group']}: {r['false_starts']} false starts in {r['person_hours']} person-h = {r['per_person_hour']}/h, people affected {r['people_affected']}, worst person S{r['worst_person']} ({r['worst_person_starts']})" for r in sel]
open("results/tweak1_selection.txt", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
