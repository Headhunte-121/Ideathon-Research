"""B5 follow-up: what would the adaptive 'chest still' rule (floor = running 10th percentile of per-second chest energy, k = KN/8) do to LIVING people?
The RTL variant cannot be run on CEBS (no wrist-pulse channel to gate the floor), so its floor tracker is EMULATED in Python second by second on the real
per-second chest energies of the 40 CEBS recordings (E4 data, 660 and 220 mV/g): up-step UP and down-step DOWN in units of 1/16 code per second, as in the RTL,
warmed up by repeating each 5-minute record 12 times (1 h) and scored on the last pass, which approximates the steady state of a day-long run.
   python py/b5_cebs_emulation.py     Output: results/b5_cebs_emulation.csv"""
import numpy as np, pandas as pd
rows = []
for tag, mv in (("660 mV/g", 660), ("220 mV/g", 220)):
    d = pd.concat([pd.read_csv(f"results/e4_scg_{g}_{mv}mVg_seconds.csv") for g in ("baseline", "postmusic")])
    for up, down in ((1, 9), (16, 144)):
        for kn in (4, 6, 8, 10, 12, 14):
            pct = []
            for rec, g in d.groupby("record"):
                e = g.sort_values("second").energy_codes.values
                floor = 0.0; below = 0; n = 0
                for rep in range(12):
                    for x in e:
                        if x * 16 > floor: floor += up
                        else: floor = max(floor - down, 0.0)
                        thr = max(5.0, floor / 16.0 * kn / 8.0)
                        if rep == 11: below += x < thr; n += 1
                pct.append(100.0 * below / n)
            pct = np.array(pct)
            rows.append(dict(chest_sensitivity=tag, UP=up, DOWN=down, k=kn / 8, living_seconds_called_still_pct_mean=round(float(pct.mean()), 1),
                             worst_person_pct=round(float(pct.max()), 1), people_over_5pct=int((pct > 5).sum()), people=len(pct)))
df = pd.DataFrame(rows); df.to_csv("results/b5_cebs_emulation.csv", index=False); print(df.to_string(index=False))
