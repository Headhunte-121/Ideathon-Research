"""A1 step 4 (round 2): a simple ST HINT on LTSTDB, reported separately from the heart-rate check-in (it is a hint, not the trigger).
ST level at J+60 ms per beat per lead = the 5th value of the database's own .16a ST measurements ("ee" in the annotation legend); the .16a values are
AUTOMATIC measurements that were manually corrected by the database authors, so this is NOT a measurement made by our detector.
Hint: deviation of the ST level from that lead's rolling baseline (median of the per-minute medians of the previous 30 min) larger than 100 uV in magnitude for
60 s in a row (any lead) -> one check-in at the 60 s mark.  Fixed rule, nothing tuned (the thresholds are the .stc annotation criteria themselves, so the
hint partly re-derives the annotators' criterion: its sensitivity is expected to be high; its false rate is the informative number).
Metrics as in A1 (py/drift_eval.py).   python py/a1_hint.py        Output: results/a1_hint.csv"""
import json, os, re, sys
import numpy as np, pandas as pd, wfdb
sys.path.insert(0, os.path.dirname(__file__))
import drift_eval as DE

meta = json.load(open("data/a1/meta.json")); split = json.load(open("splits/a1_split.json"))
ci = {}; used = []
for rec in meta:
    p = f"real_data/ltstdb/{rec}"
    if not os.path.exists(p + ".16a"): continue
    a = wfdb.rdann(p, "16a"); per = {}
    for s, aux in zip(a.sample, a.aux_note):
        m = re.match(r"^ST(\d)([+-]?\d+),([+-]?\d+),([+-]?\d+),([+-]?\d+),([+-]?\d+)", (aux or "").strip("\x00"))
        if m: per.setdefault(m[1], []).append((s / 250.0, float(m[6])))
    out = []
    for lead, v in per.items():
        v = np.array(v); t, st = v[:, 0], v[:, 1]
        mins = (t // 60).astype(int); n = mins.max() + 1
        med = pd.Series(st).groupby(mins).median().reindex(range(n)); base = med.shift(1).rolling(30, min_periods=10).median()
        dev = st - base.values[mins]; bad = np.abs(dev) > 100
        start = None
        for i in range(len(t)):
            if bad[i] and not np.isnan(dev[i]):
                if start is None: start = t[i]
                if t[i] - start >= 60.0 and (not out or out[-1][0] != lead or t[i] - out[-1][1] > 60 or True):
                    out.append((lead, start + 60.0)); start = None; skip = True
                    while i + 1 < len(t) and bad[i + 1]: i += 1; break
            else: start = None
    ci[rec] = sorted({round(x[1], 1) for x in out}); used.append(rec)
rows = []
for g in ("tune", "test"):
    recs = [r for r in used if meta[r]["patient"] in set(split[g])]
    m = DE.metrics(recs, meta, ci, None); rows.append(dict(set=g, config="ST hint (.16a J+60, 100 uV, 60 s)", **m)); print(rows[-1])
pd.DataFrame(rows).to_csv("results/a1_hint.csv", index=False)
