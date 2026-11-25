"""Diagnosis + proposal for the drift detector, using the bit-exact Python replica (py/drift_model.py).
 1. 'rtl'  : the detector exactly as built (per-beat feature).
 2. 'avgN' : PROPOSAL, Python only: same detector, but its input is the mean heart rate of the last N beats.
For every person (NSRDB, ~20 h each): false check-ins per 24 h (no injection) and detection of a +10/15/25 % step
injected over the last quarter of the recording.  Nothing is tuned to hit a target: K and window settings stay as in the RTL.
Output: results/drift_variants.csv"""
import csv, glob, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import drift_model as M

K = {"3.0": 144, "3.8": 230, "4.5": 324}
VARIANTS = [("rtl", 1), ("avg30", 30), ("avg60", 60), ("avg120", 120)]
SHIFTS = [10, 15, 25]
rows = []
for f in sorted(glob.glob("data/hr_?????.hex")):
    rec = os.path.basename(f)[3:-4]
    hr = np.array([int(l, 16) for l in open(f)], dtype=np.int64)
    hours = float(np.sum(60.0 / (hr / 16.0)) / 3600.0)           # real elapsed time = sum of RR intervals
    min_per_beat = hours * 60.0 / len(hr)
    for name, n in VARIANTS:
        feat = hr if n == 1 else M.smooth_feature(hr, n)
        for kn, k2 in K.items():
            fa = M.run_rtl_replica(feat, k2)[0]
            row = dict(record=rec, hours=round(hours, 1), variant=name, K=kn, false_checkins=fa,
                       per24h=round(fa * 24.0 / hours, 2))
            for pct in SHIFTS:
                if n == 1:
                    h2, at = M.inject(hr, pct)
                else:
                    h2, at = M.inject(hr, pct); h2 = M.smooth_feature(h2, n)
                first = M.run_rtl_replica(h2, k2, first_after=at)[1]
                row[f"delay_min_{pct}pct"] = round(first * min_per_beat, 1) if first >= 0 else "missed"
            rows.append(row)
    print(rec, "done", flush=True)
os.makedirs("results", exist_ok=True)
with open("results/drift_variants.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

import pandas as pd
d = pd.DataFrame(rows)
print("\nvariant  K    mean false/24h  max false/24h  people with >=1 false |  detected of 18 at +10% / +15% / +25%  (median delay min of those detected)")
for (v, k), g in d.groupby(["variant", "K"], sort=False):
    s = []
    for pct in SHIFTS:
        col = pd.to_numeric(g[f"delay_min_{pct}pct"], errors="coerce")
        s.append(f"{col.notna().sum()}/18 ({col.median():.0f})" if col.notna().any() else f"0/18 (-)")
    print(f"{v:7s} {k}  {g.per24h.mean():10.2f} {g.per24h.max():14.2f} {int((g.false_checkins > 0).sum()):12d}/18 | " + "  ".join(s))
