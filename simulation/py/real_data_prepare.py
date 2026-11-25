"""Turn a real PhysioNet ECG record (MIT-BIH Normal Sinus Rhythm, 128 Hz) into files for the Verilog tests.

Usage (record files already downloaded into a folder, e.g. C:\\data\\nsrdb):
    python py/real_data_prepare.py 16265 --dir C:\\data\\nsrdb --start-min 60 --minutes 30
Or let wfdb download it (needs internet):
    python py/real_data_prepare.py 16265 --pn nsrdb --start-min 60 --minutes 30

Writes into ./data :
    ecg_<rec>.hex   ECG resampled to 250 Hz, one signed 16-bit value per line (hex), scaled to ADS1292R-like codes
                    (16 codes per microvolt)  -> read by tb_real_ecg_beats.sv
    ref_<rec>.txt   reference beat positions (sample index at 250 Hz) from the database's own annotations
    hr_<rec>.hex    heart rate per beat (bpm*16) for the WHOLE record -> tb_drift_false_alarms.sv +HRFILE
Needs: pip install wfdb numpy scipy"""
import argparse, os, numpy as np, wfdb
from scipy.signal import resample_poly

p = argparse.ArgumentParser()
p.add_argument("rec")
p.add_argument("--dir", default=None, help="folder holding <rec>.hea/.dat/.atr")
p.add_argument("--pn", default=None, help="PhysioNet database name to download from, e.g. nsrdb")
p.add_argument("--start-min", type=float, default=0.0)
p.add_argument("--minutes", type=float, default=30.0)
p.add_argument("--lead", type=int, default=0)
a = p.parse_args()

if a.dir:
    path = os.path.join(a.dir, a.rec)
    hdr = wfdb.rdheader(path); fs = hdr.fs
    ann = wfdb.rdann(path, "atr")
    s0, s1 = int(a.start_min * 60 * fs), int((a.start_min + a.minutes) * 60 * fs)
    rec = wfdb.rdrecord(path, sampfrom=s0, sampto=s1, channels=[a.lead])
else:
    hdr = wfdb.rdheader(a.rec, pn_dir=a.pn); fs = hdr.fs
    ann = wfdb.rdann(a.rec, "atr", pn_dir=a.pn)
    s0, s1 = int(a.start_min * 60 * fs), int((a.start_min + a.minutes) * 60 * fs)
    rec = wfdb.rdrecord(a.rec, pn_dir=a.pn, sampfrom=s0, sampto=s1, channels=[a.lead])

units = rec.units[0]
sig = rec.p_signal[:, 0]
mv = sig * (1.0 if units == "mV" else 0.001 if units == "uV" else 1.0)     # to millivolts
sig250 = resample_poly(mv, 125, 64)                                         # 128 Hz -> 250 Hz (needs fs == 128)
assert abs(fs - 128) < 1e-6, f"this script expects 128 Hz data, got {fs}"
codes = np.clip(np.round(sig250 * 1000.0 * 16.0), -32768, 32767).astype(np.int64)   # mV -> uV -> codes
os.makedirs("data", exist_ok=True)
open(f"data/ecg_{a.rec}.hex", "w").write("\n".join(f"{int(v) & 0xFFFF:04x}" for v in codes) + "\n")

good = set("NLRBAaJSVFejnE/fQ")
bidx = np.array([s for s, sym in zip(ann.sample, ann.symbol) if sym in good])
inwin = bidx[(bidx >= s0) & (bidx < s1)] - s0
ref250 = np.round(inwin * 250.0 / fs).astype(int)
open(f"data/ref_{a.rec}.txt", "w").write("\n".join(str(v) for v in ref250) + "\n")

rr = np.diff(bidx) / fs
ok = (rr > 0.3) & (rr < 2.0)
hr = 60.0 / rr[ok]
q4 = np.clip(np.round(hr * 16), 0, 65535).astype(int)
open(f"data/hr_{a.rec}.hex", "w").write("\n".join(f"{v:04x}" for v in q4) + "\n")

amp = np.percentile(np.abs(codes), 99) / 16.0
print(f"record {a.rec}: {len(codes)} samples at 250 Hz ({len(codes)/250/60:.1f} min), {len(ref250)} reference beats in window")
print(f"typical R amplitude about {amp:.0f} uV (clipped at +/-2047 uV)")
print(f"whole-record heart rate file: data/hr_{a.rec}.hex  ({len(q4)} beats, mean {hr.mean():.1f} bpm, {rr[ok].sum()/3600:.1f} h)")
print(f"next:  tb_real_ecg_beats with +ECGFILE=data/ecg_{a.rec}.hex +NSAMP={len(codes)} +OUT=data/det_{a.rec}.txt")
print(f"       python py/real_data_score.py {a.rec}")
