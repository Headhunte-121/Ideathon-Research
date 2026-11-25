"""A4: run SDDB onset windows (10 min before to 5 min after the VF onset) and whole CUDB records through the UNCHANGED
rtl/ecg_beat_detector.sv with tb/tb_real_ecg_beats.sv (own xsim folder).  Needs settings64.bat in the same window.
   python py/a4_windows_rtl.py            Output: data/a4/det_<db>_<rec>.txt (idx at 250 Hz within the window, hr bpm*16), data/a4/win_meta.json, rail %
Channel 0, 250 Hz, 16 codes/uV, 0.5 Hz AC coupling (same as every other ECG run)."""
import json, os, sys
import numpy as np, wfdb
from scipy.signal import butter, sosfilt, sosfilt_zi
sys.path.insert(0, os.path.dirname(__file__))
import real_lib as L

def ffill(x):
    bad = np.isnan(x); n = int(bad.sum())
    if n == 0: return x, 0
    idx = np.where(~bad, np.arange(len(x)), 0); np.maximum.accumulate(idx, out=idx)
    y = x[idx]; y[np.isnan(y)] = 0.0
    return y, n


eps = json.load(open("configs/a4_episodes.json")); os.makedirs("data/a4", exist_ok=True)
sos = butter(1, 0.5, "highpass", fs=250.0, output="sos")
sim = L.Sim("xsim", work="xsim_work_a4"); sim.build(["rtl/ecg_beat_detector.sv", "tb/tb_real_ecg_beats.sv"], "tb_real_ecg_beats", "a4")
meta = {}
for key, v in eps.items():
    db, rec = key.split("/")
    if db == "sddb":
        if not v["episodes"]: continue
        t0 = v["episodes"][0]["start_s"]; a, b = max(0.0, t0 - 600), min(v["dur_s"], t0 + 300)
    else:
        a, b = 0.0, v["dur_s"]
    r = wfdb.rdrecord(f"real_data/{db}/{rec}", sampfrom=int(a * 250), sampto=int(b * 250), channels=[0]); x, nnan = ffill(r.p_signal[:, 0])
    y = sosfilt(sos, x, zi=sosfilt_zi(sos) * x[0])[0]; c = np.round(y * 16000.0)
    rail = float(np.mean(np.abs(c) > 32767) * 100); c = np.clip(c, -32768, 32767).astype(np.int64)
    open(f"data/a4/ecg_{db}_{rec}.hex", "w").write("\n".join(f"{int(q) & 0xFFFF:04x}" for q in c) + "\n")
    o = sim.run("a4", [f"ECGFILE=../data/a4/ecg_{db}_{rec}.hex", f"NSAMP={len(c)}", f"OUT=../data/a4/det_{db}_{rec}.txt"])
    if "replay done" not in o: sys.exit(f"sim failed {key}\n{o[-500:]}")
    meta[key] = dict(offset_s=a, length_s=b - a, rail_pct=round(rail, 3), nan_filled=nnan); print(key, meta[key], flush=True)
json.dump(meta, open("data/a4/win_meta.json", "w"), indent=1)
