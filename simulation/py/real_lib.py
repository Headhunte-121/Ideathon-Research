"""Shared helpers for the real-data experiments."""
import os, subprocess, re
from fractions import Fraction
import numpy as np, wfdb
from scipy.signal import resample_poly, butter, sosfilt, sosfilt_zi

BEAT_SYMS = set("NLRBAaJSVFejnE/fQ")
CLIP_STATS = {"samples": 0, "clipped": 0}      # how many ECG codes hit the 16-bit rail (reported by real_batch)

def load_wfdb(rec, folder, start_min=0.0, minutes=None, lead=0):
    path = os.path.join(folder, rec)
    hdr = wfdb.rdheader(path); fs = hdr.fs
    s0 = int(start_min * 60 * fs)
    s1 = None if minutes is None else int((start_min + minutes) * 60 * fs)
    r = wfdb.rdrecord(path, sampfrom=s0, sampto=s1, channels=[lead])
    ann = wfdb.rdann(path, "atr")
    return r, ann, fs, s0

def to_codes_250(rec, fs):
    """ECG record -> 250 Hz int codes at 16 codes/uV (ADS1292R-like), any source rate."""
    sig = rec.p_signal[:, 0]
    unit = (rec.units[0] or "mV").lower()
    mv = sig * {"mv": 1.0, "uv": 0.001, "v": 1000.0}.get(unit, 1.0)
    fr = Fraction(250, int(round(fs))).limit_denominator(2000)
    x = resample_poly(mv, fr.numerator, fr.denominator)
    # Real recordings carry a DC offset (NSTDB sits near -6 mV) that a real ECG front end removes by AC coupling.
    # Emulate that with a causal 0.5 Hz high-pass (initial state = first sample, so no start-up step).
    sos = butter(1, 0.5, "highpass", fs=250.0, output="sos")
    x = sosfilt(sos, x, zi=sosfilt_zi(sos) * x[0])[0]
    codes = np.round(x * 1000.0 * 16.0)
    CLIP_STATS["samples"] += len(codes); CLIP_STATS["clipped"] += int((np.abs(codes) > 32767).sum())
    return np.clip(codes, -32768, 32767).astype(np.int64)

def prepare_ecg(rec, folder, outdir="data", start_min=0.0, minutes=None, lead=0):
    os.makedirs(outdir, exist_ok=True)
    r, ann, fs, s0 = load_wfdb(rec, folder, start_min, minutes, lead)
    codes = to_codes_250(r, fs)
    open(f"{outdir}/ecg_{rec}.hex", "w").write("\n".join(f"{int(v) & 0xFFFF:04x}" for v in codes) + "\n")
    idx = np.array([s for s, sym in zip(ann.sample, ann.symbol) if sym in BEAT_SYMS])
    s1 = s0 + r.p_signal.shape[0]
    inwin = idx[(idx >= s0) & (idx < s1)] - s0
    ref = np.round(inwin * 250.0 / fs).astype(int)
    open(f"{outdir}/ref_{rec}.txt", "w").write("\n".join(str(v) for v in ref) + "\n")
    return len(codes), len(ref)

def hr_file(rec, folder, outdir="data"):
    """Whole-record heart rate per beat (bpm*16) from the database's own annotations."""
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(folder, rec)
    ann = wfdb.rdann(path, "atr"); fs = wfdb.rdheader(path).fs
    b = np.array([s for s, sym in zip(ann.sample, ann.symbol) if sym in BEAT_SYMS])
    rr = np.diff(b) / fs; ok = (rr > 0.3) & (rr < 2.0)
    hr = 60.0 / rr[ok]
    q4 = np.clip(np.round(hr * 16), 0, 65535).astype(int)
    open(f"{outdir}/hr_{rec}.hex", "w").write("\n".join(f"{v:04x}" for v in q4) + "\n")
    return len(q4), float(rr[ok].sum() / 3600.0)

def score_beats(rec, outdir="data", noisy_pattern=False, tol_s=0.150):
    ref = np.loadtxt(f"{outdir}/ref_{rec}.txt", dtype=int, ndmin=1)
    det = np.loadtxt(f"{outdir}/det_{rec}.txt", dtype=int, ndmin=2)
    didx = det[:, 0] if det.size else np.array([], dtype=int)
    tol = int(tol_s * 250)
    used = np.zeros(len(ref), bool); matched = np.zeros(len(didx), bool)
    for k, d in enumerate(didx):
        j = np.searchsorted(ref, d)
        c = [c for c in (j - 1, j) if 0 <= c < len(ref) and not used[c] and abs(ref[c] - d) <= tol]
        if c:
            c = min(c, key=lambda c: abs(ref[c] - d)); used[c] = True; matched[k] = True
    def noisy(i):                                   # NSTDB: noise in minutes [5+4k, 7+4k)
        m = i / 250.0 / 60.0
        return m >= 5 and ((m - 5) % 4) < 2
    out = {}
    groups = {"all": (np.ones(len(ref), bool), np.ones(len(didx), bool))}
    if noisy_pattern:
        rn = np.array([noisy(i) for i in ref]); dn = np.array([noisy(i) for i in didx])
        groups["noisy"] = (rn, dn); groups["clean"] = (~rn, ~dn)
    first_ref = 0                                    # detector cannot report the very first beat
    for g, (rm, dm) in groups.items():
        tp = int((matched & dm).sum()); fp = int((~matched & dm).sum())
        fn = int((~used & rm).sum()) - (1 if rm[first_ref] and not used[first_ref] else 0)
        fn = max(fn, 0)
        out[g] = dict(tp=tp, fn=fn, fp=fp, sens=100.0 * tp / max(tp + fn, 1), ppv=100.0 * tp / max(tp + fp, 1))
    return out

class Sim:
    """Runs the Verilog testbenches with Vivado xsim (default) or Icarus (vvp)."""
    def __init__(self, kind="xsim", work="xsim_work"):
        self.kind, self.work = kind, work
        os.makedirs(work, exist_ok=True)
    def build(self, files, top, snap):
        files = [os.path.abspath(f) for f in files]
        if self.kind == "xsim":
            subprocess.run(["xvlog", "-sv"] + files, cwd=self.work, check=True, capture_output=True, shell=(os.name == "nt"))
            subprocess.run(["xelab", f"work.{top}", "-s", snap, "--timescale", "1ns/1ps", "-debug", "off"],
                           cwd=self.work, check=True, capture_output=True, shell=(os.name == "nt"))
        else:
            subprocess.run(["iverilog", "-g2012", "-s", top, "-o", os.path.join(self.work, snap + ".vvp")] + files, check=True)
    def run(self, snap, plusargs):
        if self.kind == "xsim":
            # xsim is a .bat file: cmd splits unquoted NAME=value at '=', so every plusarg must be quoted.
            cmd = ["xsim", snap, "-runall"] + sum([["-testplusarg", f'"{p}"'] for p in plusargs], [])
            return subprocess.run(cmd, cwd=self.work, capture_output=True, text=True, shell=(os.name == "nt")).stdout
        cmd = ["vvp", os.path.join(self.work, snap + ".vvp")] + ["+" + p for p in plusargs]
        return subprocess.run(cmd, capture_output=True, text=True).stdout
