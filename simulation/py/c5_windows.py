"""C5: PTB-XL median-beat int8 windows (leads I, II, V2, V5), same window/pre-processing as C1.  Replayed.  python py/c5_windows.py -> data/edge/ptbxl_windows.npz
10-second resting diagnostic 12-lead ECGs: not early warning, not a wearable, not a sternal lead.  Causal 0.5 Hz high-pass (as C1) instead of A3's zero-phase filter (logged)."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
LEADS = {"I": 0, "II": 1, "V2": 7, "V5": 10}

def one(a):
    ecg_id, fn = a
    import wfdb; from fractions import Fraction
    from scipy.signal import resample_poly, butter, sosfilt, sosfilt_zi
    import beat_model as B, c1_lib as C
    rec = wfdb.rdrecord(f"real_data/ptbxl/{fn}"); out = np.zeros((4, 75), np.int8); valid = np.zeros(4, bool); sos = butter(1, 0.5, "highpass", fs=250.0, output="sos")
    for li, (nm, k) in enumerate(LEADS.items()):
        x = rec.p_signal[:, k]
        if np.isnan(x).any(): continue
        y = resample_poly(x * 1000.0, 5, 2); y = sosfilt(sos, y, zi=sosfilt_zi(sos) * y[0])[0]; codes = np.clip(np.round(y * 16.0), -32768, 32767).astype(np.int64)
        det = B.detect(codes); R = [int(max(d - 15, 0) + np.argmax(np.abs(codes[max(d - 15, 0): d + 16]))) for d in det]
        segs = [codes[r - 50: r + 100] for r in R if 50 <= r <= len(codes) - 100]
        if len(segs) < 3: continue
        med = np.round(np.median(np.stack(segs), axis=0)).astype(np.int64); out[li] = C.make_window(med); valid[li] = True
    return ecg_id, out, valid

if __name__ == "__main__":
    from multiprocessing import Pool
    import a3_ptbxl as A
    db = A.labels()
    with Pool(max(1, os.cpu_count() - 2)) as p: res = p.map(one, list(zip(db.index, db.filename_lr)), chunksize=50)
    ids = np.array([r[0] for r in res]); win = np.stack([r[1] for r in res]); valid = np.stack([r[2] for r in res])
    d = db.loc[ids]; np.savez_compressed("data/edge/ptbxl_windows.npz", ecg_id=ids, win=win, valid=valid, label=d.label.values.astype(np.int8), fold=d.strat_fold.values.astype(np.int8), patient=d.patient_id.values.astype(np.int64))
    print(len(ids), "records; valid per lead", valid.sum(0), "MI", int(d.label.sum()), "NORM", int((d.label == 0).sum()))
