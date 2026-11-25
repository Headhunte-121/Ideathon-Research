"""Tweak 5 (lowest priority): reject a beat that arrives far too soon after the last one unless it is clearly larger.  PROPOSAL, tested in the
Python port (py/beat_model.py), NOT in the RTL.   Tune on NSTDB record 118 (6 noise levels), test on record 119 and on the 18 clean NSRDB people.
Variants (fraction of the median of the last 5 RR intervals, slope multiple of the threshold):  none | (0.5, 2) | (0.6, 2) | (0.7, 3)
Selection on the tune record: highest mean PPV in the noisy minutes with sensitivity loss <= 1 point.
    python py/tweak5_early_beat.py       Output: results/tweak5_early_beat.csv"""
import csv, os, sys, shutil
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import beat_model as B, real_lib as L

VARS = [("none", None), ("0.5/2", (0.5, 2.0)), ("0.6/2", (0.6, 2.0)), ("0.7/3", (0.7, 3.0))]
TMP = "data/tweak5"; os.makedirs(TMP, exist_ok=True)


def score(rec, ecg_path, ref_path, rej, noisy):
    x = np.array([int(l, 16) for l in open(ecg_path)]); x = np.where(x > 32767, x - 65536, x)
    det = B.detect(x, reject_early=rej)
    shutil.copy(ref_path, f"{TMP}/ref_{rec}.txt")
    np.savetxt(f"{TMP}/det_{rec}.txt", np.column_stack([det, np.zeros(len(det), int)]), fmt="%d")
    return L.score_beats(rec, TMP, noisy)


rows = []
nst = [f"{p}e{s}" for p in (118, 119) for s in ("24", "18", "12", "06", "00", "_6")]
for name, rej in VARS:
    for rec in nst:
        sc = score(rec, f"data/tweak3/s16_t1500/ecg_{rec}.hex", f"data/tweak3/s16_t1500/ref_{rec}.txt", rej, True)["noisy"]
        rows.append(dict(variant=name, set=("tune" if rec.startswith("118") else "test"), dataset="NSTDB noisy", record=rec, sens=round(sc["sens"], 2), ppv=round(sc["ppv"], 2), tp=sc["tp"], fn=sc["fn"], fp=sc["fp"]))
    for rec in sorted(f[4:-4] for f in os.listdir("data") if f.startswith("ecg_") and f[4:9].isdigit() and len(f) == 13):
        sc = score(rec, f"data/ecg_{rec}.hex", f"data/ref_{rec}.txt", rej, False)["all"]
        rows.append(dict(variant=name, set="test", dataset="NSRDB clean", record=rec, sens=round(sc["sens"], 2), ppv=round(sc["ppv"], 2), tp=sc["tp"], fn=sc["fn"], fp=sc["fp"]))
    print(name, "done", flush=True)
with open("results/tweak5_early_beat.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def mean(v, st, ds, col):
    r = [x[col] for x in rows if x["variant"] == v and x["set"] in st and x["dataset"] == ds]; return sum(r) / len(r)
base_sens = mean("none", ("tune",), "NSTDB noisy", "sens")
ok = [v for v, _ in VARS if v == "none" or base_sens - mean(v, ("tune",), "NSTDB noisy", "sens") <= 1.0]
best = max(ok, key=lambda v: mean(v, ("tune",), "NSTDB noisy", "ppv"))
print("variant   tune(118 noisy) sens/ppv   test(119 noisy) sens/ppv   NSRDB clean sens/ppv")
for v, _ in VARS:
    print(f"{v:8s}  {mean(v,('tune',),'NSTDB noisy','sens'):6.2f} / {mean(v,('tune',),'NSTDB noisy','ppv'):6.2f}       {mean(v,('test',),'NSTDB noisy','sens'):6.2f} / {mean(v,('test',),'NSTDB noisy','ppv'):6.2f}      {mean(v,('test',),'NSRDB clean','sens'):6.2f} / {mean(v,('test',),'NSRDB clean','ppv'):6.2f}")
print("selected on the tune record:", best)
