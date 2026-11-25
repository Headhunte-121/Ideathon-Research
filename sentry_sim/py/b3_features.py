"""B3/B4 step 1 (round 2): per-second features for each PPG-DaLiA person + the chest ECG exported as 250 Hz codes for the Verilog beat detector.
  python -I py/b3_features.py --dir real_data/ppg_dalia/PPG_FieldStudy --subjects 1 2 ... 15
Writes data/b3/S<k>.npz  (label, pp_rel = wrist pulse size / own sitting median, wrist_rel, chest_rel = motion std / own sitting median)
and data/b3/ecg_S<k>.hex (chest ECG, 700 Hz -> 250 Hz, 16 codes/uV, same 0.5 Hz AC coupling as real_lib.to_codes_250), plus the fraction of
samples on the ADC rail (rule 8).  Pickles are only loaded from the dataset you downloaded yourself."""
import argparse, os, pickle
import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfilt, sosfilt_zi, resample_poly

ap = argparse.ArgumentParser(); ap.add_argument("--dir", required=True); ap.add_argument("--subjects", type=int, nargs="+", required=True)
a = ap.parse_args(); os.makedirs("data/b3", exist_ok=True)


def per_second(x, fs):
    n = int(len(x) // fs); return x[: int(n * fs)].reshape(n, int(fs)), n


for s in a.subjects:
    with open(os.path.join(a.dir, f"S{s}", f"S{s}.pkl"), "rb") as f: d = pickle.load(f, encoding="latin1")
    sig = d["signal"]
    bvp = np.asarray(sig["wrist"]["BVP"]).ravel().astype(float)
    cacc = np.asarray(sig["chest"]["ACC"]).astype(float); wacc = np.asarray(sig["wrist"]["ACC"]).astype(float)
    ecg = np.asarray(sig["chest"]["ECG"]).ravel().astype(float)
    lab = np.asarray(d["activity"]).ravel().astype(int)
    bf = sosfiltfilt(butter(3, [0.5, 4.0], "bandpass", fs=64.0, output="sos"), bvp)
    B1, nb = per_second(bf, 64); pp = B1.max(axis=1) - B1.min(axis=1)
    M, nm = per_second(np.sqrt((cacc ** 2).sum(axis=1)), 700); mv = M.std(axis=1)
    W, nw = per_second(np.sqrt((wacc ** 2).sum(axis=1)), 32); wv = W.std(axis=1)
    n = min(nb, nm, nw, len(lab) // 4, len(ecg) // 700)
    pp, mv, wv = pp[:n], mv[:n], wv[:n]
    L = np.array([np.bincount(lab[i * 4:(i + 1) * 4]).argmax() for i in range(n)])
    sit = L == 1; ok = sit.sum() > 30
    ref = lambda x: np.median(x[sit]) if ok else np.median(x)
    np.savez(f"data/b3/S{s}.npz", label=L, pp_rel=pp / ref(pp), wrist_rel=wv / ref(wv), chest_rel=mv / ref(mv), n=n)
    e250 = resample_poly(ecg[: n * 700], 5, 14)
    sos = butter(1, 0.5, "highpass", fs=250.0, output="sos")
    e250 = sosfilt(sos, e250, zi=sosfilt_zi(sos) * e250[0])[0]
    c = np.round(e250 * 1000.0 * 16.0); rail = float(np.mean(np.abs(c) > 32767) * 100)
    c = np.clip(c, -32768, 32767).astype(np.int64)
    open(f"data/b3/ecg_S{s}.hex", "w").write("\n".join(f"{int(v) & 0xFFFF:04x}" for v in c) + "\n")
    print(f"S{s}: {n} s, {len(c)} ECG samples at 250 Hz, {rail:.3f}% on the ADC rail", flush=True)
