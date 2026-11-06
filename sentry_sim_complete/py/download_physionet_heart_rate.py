"""Download a PhysioNet MIT-BIH Normal Sinus Rhythm recording and write one heart-rate value per beat
(bpm * 16, hex) for tb_drift_false_alarms.sv.   Usage:  python py/download_physionet_heart_rate.py 16265
Needs:  pip install wfdb numpy   and internet access. Record ids: 16265 16272 16273 16420 16483 16539 ..."""
import sys, numpy as np, wfdb
rec = sys.argv[1] if len(sys.argv) > 1 else "16265"
ann = wfdb.rdann(rec, "atr", pn_dir="nsrdb")
fs = wfdb.rdheader(rec, pn_dir="nsrdb").fs
beats = np.array([s for s, sym in zip(ann.sample, ann.symbol) if sym in "NLRBAaJSVFejnE/fQ"])
rr = np.diff(beats) / fs                       # seconds between beats
ok = (rr > 0.3) & (rr < 2.0)                   # drop artefacts
hr = 60.0 / rr[ok]
q4 = np.clip(np.round(hr * 16), 0, 65535).astype(int)
import os; os.makedirs("data", exist_ok=True)
path = f"data/hr_{rec}.hex"
open(path, "w").write("\n".join(f"{v:04x}" for v in q4) + "\n")
print(f"{path}: {len(q4)} beats, mean {hr.mean():.1f} bpm, about {rr[ok].sum()/3600:.1f} h")
print(f"run:  +HRFILE={path} +NBEATS={len(q4)}")
