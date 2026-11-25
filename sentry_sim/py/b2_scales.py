"""B2 (round 2, supersedes tweak 3): scales 16/8/4/2 codes/uV, MIN_THR scaled and unscaled.  (Original tweak 3 text follows.)
Tweak 3: how much of the loud-noise loss in E1 was never the detector's fault (my 16 codes/uV scale clipping the signal)?
Replays the NSTDB records at several ECG scales through the UNCHANGED rtl/ecg_beat_detector.sv.  The detector's MIN_THR floor is
set per scale so that it stays the same number of microvolts as in E1 (1500 codes at 16 codes/uV = 93.75 uV), plus one run where it is NOT
rescaled, to show that effect separately.   Needs settings64.bat in the same window.
    python py/tweak3_scale.py
Output: results/b2_scales_nstdb.csv  (original E1 results in results/real_ecg_nstdb.csv are untouched)"""
import csv, os, subprocess, sys
from fractions import Fraction
import numpy as np, wfdb
from scipy.signal import resample_poly, butter, sosfilt, sosfilt_zi
sys.path.insert(0, os.path.dirname(__file__))
import real_lib as L

RECS = ["118e24", "118e18", "118e12", "118e06", "118e00", "118e_6", "119e24", "119e18", "119e12", "119e06", "119e00", "119e_6"]
# (label, codes per uV, MIN_THR)
VARIANTS = [("scale16_thr1500 (E1 as before)", 16, 1500), ("scale8_thr750 (scaled)", 8, 750), ("scale8_thr1500 (unscaled)", 8, 1500),
            ("scale4_thr375 (scaled)", 4, 375), ("scale4_thr1500 (unscaled)", 4, 1500), ("scale2_thr187 (scaled)", 2, 187), ("scale2_thr1500 (unscaled)", 2, 1500)]
WORK = "xsim_work"; DATA = "data/b2"
os.makedirs(DATA, exist_ok=True); os.makedirs(WORK, exist_ok=True)


def run(cmd):
    return subprocess.run(cmd, cwd=WORK, capture_output=True, text=True, shell=(os.name == "nt"))


def codes(rec, scale):
    r, ann, fs, s0 = L.load_wfdb(rec, "real_data/nstdb", 0.0, None, 0)
    mv = r.p_signal[:, 0]
    fr = Fraction(250, int(round(fs))).limit_denominator(2000)
    x = resample_poly(mv, fr.numerator, fr.denominator)
    sos = butter(1, 0.5, "highpass", fs=250.0, output="sos")
    x = sosfilt(sos, x, zi=sosfilt_zi(sos) * x[0])[0]
    c = np.round(x * 1000.0 * scale)
    clip = float(np.mean(np.abs(c) > 32767) * 100)
    idx = np.array([s for s, sym in zip(ann.sample, ann.symbol) if sym in L.BEAT_SYMS])
    ref = np.round(idx[(idx >= s0)] * 250.0 / fs).astype(int)
    return np.clip(c, -32768, 32767).astype(np.int64), ref, clip


def main():
    src = open("rtl_variants/tb_real_ecg_beats_scaled.sv", encoding="utf-8").read()
    THRS = sorted({t for _, _, t in VARIANTS})
    for thr in THRS:
        # one testbench per threshold (xelab -generic_top does not survive the xelab.bat launcher): module name and default changed
        t = src.replace("module tb_real_ecg_beats_scaled #(parameter MIN_THR_TB = 1500)", f"module tb_scaled_{thr} #(parameter MIN_THR_TB = {thr})")
        open(f"{DATA}/tb_scaled_{thr}.sv", "w", encoding="utf-8").write(t)
    files = [os.path.abspath("rtl/ecg_beat_detector.sv")] + [os.path.abspath(f"{DATA}/tb_scaled_{thr}.sv") for thr in THRS]
    b = run(["xvlog", "-sv"] + files)
    if b.returncode: sys.exit(b.stdout + b.stderr)
    for thr in THRS:
        e = run(["xelab", f"work.tb_scaled_{thr}", "-s", f"s{thr}", "--timescale", "1ns/1ps", "-debug", "off"])
        if e.returncode: sys.exit(e.stdout + e.stderr)
    rows = []
    for label, scale, thr in VARIANTS:
        d = f"{DATA}/s{scale}_t{thr}"; os.makedirs(d, exist_ok=True)
        for rec in RECS:
            c, ref, clip = codes(rec, scale)
            open(f"{d}/ecg_{rec}.hex", "w").write("\n".join(f"{int(v) & 0xFFFF:04x}" for v in c) + "\n")
            np.savetxt(f"{d}/ref_{rec}.txt", ref, fmt="%d")
            ab = os.path.abspath(d).replace("\\", "/")
            o = run(["xsim", f"s{thr}", "-runall", "-testplusarg", f'"ECGFILE={ab}/ecg_{rec}.hex"', "-testplusarg", f'"NSAMP={len(c)}"',
                     "-testplusarg", f'"OUT={ab}/det_{rec}.txt"']).stdout
            if "replay done" not in o: sys.exit(f"sim failed {label} {rec}\n{o[-500:]}")
            sc = L.score_beats(rec, d, True)
            for seg in ("noisy", "clean"):
                v = sc[seg]
                rows.append(dict(variant=label, record=rec[:3], snr_db=(-6 if rec.endswith("e_6") else int(rec[4:])), segment=seg,
                                 pct_samples_clipped=round(clip, 2), sens=round(v["sens"], 2), ppv=round(v["ppv"], 2),
                                 tp=v["tp"], fn=v["fn"], fp=v["fp"]))
            print(label, rec, "clip %.1f%%" % clip, "noisy sens %.1f ppv %.1f" % (sc["noisy"]["sens"], sc["noisy"]["ppv"]), flush=True)
    with open("results/b2_scales_nstdb.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("saved results/b2_scales_nstdb.csv")


main()
