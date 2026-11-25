"""A4 helper: run the Python port of the beat detector over WHOLE long records (SDDB, 20+ h) in 30-minute chunks.
   python py/a4_beats_py.py sddb 30 31 ...      Output: data/a4/beats_py_<db>_<rec>.npy  (beat times in seconds)
Same front end as everywhere else: 250 Hz, 16 codes/uV, 0.5 Hz AC coupling (state carried across chunks), channel 0."""
import os, sys, time
import numpy as np, wfdb
from scipy.signal import butter, sosfilt, sosfilt_zi
sys.path.insert(0, os.path.dirname(__file__))
import beat_model as B

def ffill(x):
    """invalid ADC samples are NaN in some PhysioNet records; one NaN would poison the high-pass filter for the rest of the record"""
    bad = np.isnan(x); n = int(bad.sum())
    if n == 0: return x, 0
    idx = np.where(~bad, np.arange(len(x)), 0); np.maximum.accumulate(idx, out=idx)
    y = x[idx]; y[np.isnan(y)] = 0.0
    return y, n

db = sys.argv[1]; os.makedirs("data/a4", exist_ok=True)
sos = butter(1, 0.5, "highpass", fs=250.0, output="sos")
for rec in sys.argv[2:]:
    out = f"data/a4/beats_py_{db}_{rec}.npy"
    if os.path.exists(out): continue
    p = f"real_data/{db}/{rec}"; h = wfdb.rdheader(p); fs = int(h.fs); n = h.sig_len; step = 30 * 60 * fs
    det = B.StreamDetector(FS=250); zi = None; beats = []; rail = 0; tot = 0; t0 = time.time(); nan = 0; last = 0.0
    for s0 in range(0, n, step):
        x = wfdb.rdrecord(p, sampfrom=s0, sampto=min(n, s0 + step), channels=[0]).p_signal[:, 0]
        x, k = ffill(x); nan += k
        if fs != 250: from scipy.signal import resample_poly; x = resample_poly(x, 250, fs)
        if zi is None: zi = sosfilt_zi(sos) * x[0]
        y, zi = sosfilt(sos, x, zi=zi)
        c = np.round(y * 16000.0); rail += int((np.abs(c) > 32767).sum()); tot += len(c)
        beats += det.feed(np.clip(c, -32768, 32767).astype(np.int64))
    np.save(out, np.array(beats) / 250.0)
    print(f"{db}/{rec}: {len(beats)} beats in {n/fs/3600:.1f} h, {100*rail/tot:.3f}% on the rail, {nan} NaN samples filled, {time.time()-t0:.0f} s", flush=True)
