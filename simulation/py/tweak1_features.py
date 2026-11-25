"""Tweak 1, step 1: per-second features for every PPG-DaLiA person, cached in data/dalia_feats/S<k>.npz.
  python -I py/tweak1_features.py --dir real_data/ppg_dalia/PPG_FieldStudy --subjects 1 2 ... 15
Per second: activity label; wrist pulse lost (same definition as E5); chest moving (same as E5); wrist moving (NEW: std of wrist
accelerometer magnitude, relative to that person's own sitting median); seconds since the last chest-ECG beat found by the
detector port (py/beat_model.py, chest ECG resampled to 250 Hz at 16 codes/uV with the same 0.5 Hz AC coupling as E1/E2).
Only load pickles you downloaded yourself from the dataset page."""
import argparse, os, pickle, sys
from fractions import Fraction
import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfilt, sosfilt_zi, resample_poly
sys.path.insert(0, os.path.dirname(__file__))
import beat_model as B

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True); ap.add_argument("--subjects", type=int, nargs="+", required=True)
ap.add_argument("--loss-frac", type=float, default=0.15); ap.add_argument("--move-x", type=float, default=5.0)
a = ap.parse_args()
os.makedirs("data/dalia_feats", exist_ok=True)


def per_second(x, fs):
    n = int(len(x) // fs); return x[: int(n * fs)].reshape(n, int(fs)), n


for s in a.subjects:
    p = os.path.join(a.dir, f"S{s}", f"S{s}.pkl")
    with open(p, "rb") as f: d = pickle.load(f, encoding="latin1")
    sig = d["signal"]
    bvp = np.asarray(sig["wrist"]["BVP"]).ravel().astype(float)
    cacc = np.asarray(sig["chest"]["ACC"]).astype(float)
    wacc = np.asarray(sig["wrist"]["ACC"]).astype(float)
    ecg = np.asarray(sig["chest"]["ECG"]).ravel().astype(float)            # mV, 700 Hz
    lab = np.asarray(d["activity"]).ravel().astype(int)
    bf = sosfiltfilt(butter(3, [0.5, 4.0], "bandpass", fs=64.0, output="sos"), bvp)
    B1, nb = per_second(bf, 64); pp = B1.max(axis=1) - B1.min(axis=1)
    M, nm = per_second(np.sqrt((cacc ** 2).sum(axis=1)), 700); mv = M.std(axis=1)
    W, nw = per_second(np.sqrt((wacc ** 2).sum(axis=1)), 32); wv = W.std(axis=1)
    n = min(nb, nm, nw, len(lab) // 4, len(ecg) // 700)
    pp, mv, wv = pp[:n], mv[:n], wv[:n]
    L = np.array([np.bincount(lab[i * 4:(i + 1) * 4]).argmax() for i in range(n)])
    sit = L == 1
    ok = sit.sum() > 30
    pp0 = np.median(pp[sit]) if ok else np.median(pp)
    mv0 = np.median(mv[sit]) if ok else np.median(mv)
    wv0 = np.median(wv[sit]) if ok else np.median(wv)
    lost = pp < a.loss_frac * pp0
    chest_moving = mv > a.move_x * mv0
    # chest ECG -> 250 Hz codes, AC coupled, detector port
    e250 = resample_poly(ecg, 5, 14)
    sos = butter(1, 0.5, "highpass", fs=250.0, output="sos")
    e250 = sosfilt(sos, e250, zi=sosfilt_zi(sos) * e250[0])[0]
    codes = np.clip(np.round(e250 * 1000.0 * 16.0), -32768, 32767).astype(np.int64)
    clip = float(np.mean(np.abs(e250 * 16000) > 32767) * 100)
    beats = B.detect(codes) / 250.0                                         # seconds
    ends = np.arange(1, n + 1, dtype=float)
    j = np.searchsorted(beats, ends, side="right") - 1
    age = np.where(j >= 0, ends - beats[np.maximum(j, 0)], 1e6)
    np.savez(f"data/dalia_feats/S{s}.npz", label=L, lost=lost, chest_moving=chest_moving, wrist_rel=wv / wv0, chest_rel=mv / mv0,
             ecg_age=age, n_beats=len(beats), ecg_clip_pct=clip, sitting_wrist_std=wv0, sitting_chest_std=mv0)
    rp = np.asarray(d["rpeaks"]).ravel() / 700.0
    print(f"S{s}: {n} s, {len(beats)} chest-ECG beats found (dataset R-peaks: {len(rp)}), ECG at rail {clip:.2f}%, "
          f"sitting wrist std {wv0:.4f} g, sitting chest std {mv0:.4f} g", flush=True)
