"""Round 3 shared helpers: EDB subjects, episodes, beat eligibility, beat window / hand features.  Label for everything built on it: Replayed (public recording)."""
import os, re, sys, collections
import numpy as np, wfdb
sys.path.insert(0, os.path.dirname(__file__))
import real_lib as L

EDB = "real_data/edb"
FS = 250
WIN_L, WIN_R = 50, 100            # samples R-50 .. R+99 at 250 Hz (0.6 s)
NPAIR = 75


def records():
    return [l.strip() for l in open(f"{EDB}/RECORDS") if l.strip()]


def subjects():
    """record -> subject id.  Records sharing identical age+sex+diagnosis header comments are one subject (assumption A-subj; gives 79 subjects)."""
    g = collections.OrderedDict()
    for r in records():
        h = wfdb.rdheader(f"{EDB}/{r}")
        key = tuple(x.strip() for x in h.comments if not x.startswith("Recorder") and not x.startswith("Medications"))
        g.setdefault(key, []).append(r)
    return {r: f"s{i:02d}" for i, rs in enumerate(g.values()) for r in rs}


def merge(iv):
    iv = sorted(iv); out = []
    for s, e in iv:
        if out and s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)
        else: out.append([s, e])
    return out


def annotations(rec):
    """-> beat sample idx, beat symbols, ST episodes [(on,off,sign_hint,'ST1+')...] in seconds, T episodes."""
    at = wfdb.rdann(f"{EDB}/{rec}", "atr")
    bi = np.array([s for s, sy in zip(at.sample, at.symbol) if sy in L.BEAT_SYMS]); bs = np.array([sy for sy in at.symbol if sy in L.BEAT_SYMS])
    op = {}; st = []; tw = []
    for s, aux in zip(at.sample, at.aux_note):
        aux = (aux or "").strip("\x00"); x = s / FS
        m = re.match(r"^\((ST|T)(\d)([+-]*)", aux)
        if m: op[(m[1], m[2])] = (x, m[3]); continue
        m = re.match(r"^(ST|T)(\d)[+-]*\)", aux)
        if m and (m[1], m[2]) in op:
            on, sg = op.pop((m[1], m[2])); (st if m[1] == "ST" else tw).append((on, x, sg))
    return bi, bs, st, tw


def eligible(bi, bs):
    """N beat whose previous beat is also N and RR 0.4-1.5 s.  Returns boolean mask, rr (s) and previous rr."""
    n = len(bi); ok = np.zeros(n, bool); rr = np.full(n, np.nan); rr2 = np.full(n, np.nan)
    for i in range(1, n):
        rr[i] = (bi[i] - bi[i - 1]) / FS
        ok[i] = bs[i] == "N" and bs[i - 1] == "N" and 0.4 <= rr[i] <= 1.5
    rr2[2:] = rr[1:-1]
    return ok, rr, rr2


def beat_label(t, st, tw):
    """1 inside an ST episode; 0 if >=30 min from every ST/T episode; -1 otherwise (T-only or near an episode)."""
    if any(s <= t <= e for s, e, _ in st): return 1
    if any(s - 1800 <= t <= e + 1800 for s, e, _ in st + tw): return -1
    return 0


def make_window(seg):
    """seg = 150 int codes (250 Hz, R at index 50).  Firmware-style int8 window (75 samples @125 Hz, R at index 25), 1 LSB = 16 uV (shift 8).
    Uses ONLY samples R-50..R+99."""
    seg = np.asarray(seg, dtype=np.int64); assert len(seg) == WIN_L + WIN_R
    pair = (seg[0::2] + seg[1::2]) >> 1
    base = int(seg[50 - 18: 50 - 10].sum()) >> 3
    return np.clip((pair - base) >> 8, -128, 127).astype(np.int8)


def hand_features(seg, rr, rr2):
    """Six features in uV / bpm from the 150-sample 250 Hz segment (R at 50).  ST level at R+100..120 ms, slope R+80..140 ms, T amp R+150..350 ms, Q depth R-60..R."""
    x = np.asarray(seg, dtype=np.float64) / 16.0
    b = x[50 - 18: 50 - 10].mean()
    st = x[50 + 25: 50 + 31].mean() - b
    slope = (x[50 + 33: 50 + 37].mean() - x[50 + 19: 50 + 23].mean()) / 60.0       # uV per ms between ~R+85 and ~R+140
    seg_t = x[50 + 37: 50 + 88] - b; tamp = seg_t[np.argmax(np.abs(seg_t))]
    q = max(0.0, b - x[50 - 15: 51].min())
    hr = 60.0 / rr; ratio = rr / rr2 if np.isfinite(rr2) else 1.0
    return np.array([st, slope, tamp, q, hr, ratio], dtype=np.float32), float(st)
