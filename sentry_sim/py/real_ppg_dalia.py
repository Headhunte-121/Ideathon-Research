"""PPG-DaLiA real daily-life check of the "pulse lost" and "motion" signals, per activity.
For each subject pickle (S1.pkl ... S15.pkl) and each activity it reports how often, in a LIVING person,
  - the wrist pulse is lost (per-second wrist pulse size below LOSS_FRAC of that subject's own sitting median), and
  - the chest is moving (chest accelerometer variation above MOVE_X times that subject's sitting median), and
  - pulse lost while the chest is NOT moving (the case the Pod could mistake for arrest if the chest-heartbeat check failed).
  python py/real_ppg_dalia.py --dir real_data/ppg_dalia --subjects 1 2 3 ... 15
Pickles are loaded with encoding='latin1'. Only load files you downloaded yourself from the dataset page."""
import argparse, csv, os, pickle
import numpy as np
from scipy.signal import butter, sosfiltfilt

ACT = {0: "transient", 1: "sitting", 2: "stairs", 3: "table soccer", 4: "cycling", 5: "driving", 6: "lunch", 7: "walking", 8: "working"}
ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True); ap.add_argument("--subjects", type=int, nargs="+", required=True)
ap.add_argument("--loss-frac", type=float, default=0.15); ap.add_argument("--move-x", type=float, default=5.0)
a = ap.parse_args()

def per_second(x, fs):
    n = int(len(x) // fs); return x[: int(n * fs)].reshape(n, int(fs)), n

rows = []; allsec = {}; SEC = []
for s in a.subjects:
    p = os.path.join(a.dir, f"S{s}", f"S{s}.pkl")
    if not os.path.exists(p): p = os.path.join(a.dir, f"S{s}.pkl")
    with open(p, "rb") as f: d = pickle.load(f, encoding="latin1")
    sig = d["signal"]; bvp = np.asarray(sig["wrist"]["BVP"]).ravel().astype(float)
    acc = np.asarray(sig["chest"]["ACC"]).astype(float)
    lab = np.asarray(d["activity"]).ravel().astype(int)           # 4 Hz activity label
    sos = butter(3, [0.5, 4.0], "bandpass", fs=64.0, output="sos"); bf = sosfiltfilt(sos, bvp)
    B, nb = per_second(bf, 64); pp = B.max(axis=1) - B.min(axis=1)
    mag = np.sqrt((acc ** 2).sum(axis=1)); M, nm = per_second(mag, 700); mv = M.std(axis=1)
    n = min(nb, nm, len(lab) // 4)
    pp, mv = pp[:n], mv[:n]; L = np.array([np.bincount(lab[i * 4:(i + 1) * 4]).argmax() for i in range(n)])
    sit = L == 1
    pp0 = np.median(pp[sit]) if sit.sum() > 30 else np.median(pp); mv0 = np.median(mv[sit]) if sit.sum() > 30 else np.median(mv)
    lost = pp < a.loss_frac * pp0; moving = mv > a.move_x * mv0
    SEC.append(np.column_stack([np.full(n, s), np.arange(n), L, lost, moving]))   # per-second flags, for run-length analysis
    for k, name in ACT.items():
        m = L == k
        if k == 0 or m.sum() < 30: continue
        rows.append(dict(subject=s, activity=name, seconds=int(m.sum()), pct_pulse_lost=round(100 * lost[m].mean(), 1),
                         pct_moving=round(100 * moving[m].mean(), 1), pct_lost_and_still=round(100 * (lost & ~moving)[m].mean(), 1)))
        allsec.setdefault(name, []).append((int(m.sum()), lost[m].sum(), moving[m].sum(), (lost & ~moving)[m].sum()))
    print(f"S{s}: {n} s, sitting median pulse size {pp0:.2f}, sitting motion {mv0:.4f} g")
os.makedirs("results", exist_ok=True)
np.savetxt("results/real_ppg_dalia_seconds.csv", np.vstack(SEC), fmt="%d", delimiter=",", header="subject,second,activity,pulse_lost,moving", comments="")
with open("results/real_ppg_dalia.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("\nall subjects pooled (percent of seconds, living people):")
print(f"{'activity':14s} {'seconds':>8s} {'pulse lost':>11s} {'moving':>8s} {'lost & still':>13s}")
for name, v in allsec.items():
    t = np.array(v).sum(axis=0)
    print(f"{name:14s} {int(t[0]):8d} {100*t[1]/t[0]:10.1f}% {100*t[2]/t[0]:7.1f}% {100*t[3]/t[0]:12.1f}%")
