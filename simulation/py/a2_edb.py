"""A2 (round 2): CONFIRMATION of the frozen A1 configuration on the European ST-T Database (edb: 90 two-hour excerpts, 79 subjects, ECG only).
The frozen config (configs/a1_frozen.json) is run UNCHANGED, plus the untuned baseline (rtl K=3.8), on EDB records that do not overlap LTSTDB.
Overlap (from the LTSTDB headers: 'An excerpt of this recording is included in the European ST-T Database (record eXXXX)') and same-subject records
(EDB description) are excluded:  e0103 e0104 e0105 e0113 e0123 e0124 e0125 e0126 e0127 e0129 e0133 e0162 e0163 e0603 e0604   (15 records).
EDB episodes: '(STn+/-' .. 'STn+/-)' = ST-segment change (positive class here), '(Tn..' = T-wave change (reported separately); EDB does not label ischemic origin.
Beat times = the database's own annotations.  Two-hour records: a detector that needs 2^13 beats of learning (about 2 h) has almost nothing left to test; that is reported, not fixed.
   python py/a2_edb.py       Output: results/a2_edb_test.csv, results/a2_edb_records.csv"""
import json, os, re, sys
import numpy as np, pandas as pd, wfdb
sys.path.insert(0, os.path.dirname(__file__))
import drift_eval as DE

EXCL = {"e0103", "e0104", "e0105", "e0113", "e0123", "e0124", "e0125", "e0126", "e0127", "e0129", "e0133", "e0162", "e0163", "e0603", "e0604"}
BEAT = set("NLRBAaJSVFejnE/fQ"); cfg = json.load(open("configs/a1_frozen.json"))
meta = {}; ci = {}; ci_base = {}; rows = []
for rec in [l.strip() for l in open("real_data/edb/RECORDS") if l.strip()]:
    if rec in EXCL: continue
    at = wfdb.rdann(f"real_data/edb/{rec}", "atr"); h = wfdb.rdheader(f"real_data/edb/{rec}")
    t = np.array([s / 250.0 for s, sy in zip(at.sample, at.symbol) if sy in BEAT]); rr = np.diff(t); ok = (rr > 0.3) & (rr < 2.0)
    tt, q = t[1:][ok], np.round(60.0 / rr[ok] * 16).astype(np.int64)
    op = {}; st = []; tw = []
    for s, aux in zip(at.sample, at.aux_note):
        aux = (aux or "").strip("\x00"); x = s / 250.0
        m = re.match(r"^\((ST|T)(\d)", aux)
        if m: op[(m[1], m[2])] = x; continue
        m = re.match(r"^(ST|T)(\d)[+-]*\)", aux)
        if m and (m[1], m[2]) in op: (st if m[1] == "ST" else tw).append([op.pop((m[1], m[2])), x])
    meta[rec] = dict(patient=rec, dur_s=h.sig_len / 250.0, ischemic=DE.merge(st), rate_related=DE.merge(tw))
    ci[rec] = DE.checkins_tq(tt, q, tuple(cfg["selected"])); ci_base[rec] = DE.checkins_tq(tt, q, tuple(cfg["baseline"]))
    rows.append(dict(record=rec, beats=len(tt), hours=round(h.sig_len / 250 / 3600, 2), ST_episodes=len(meta[rec]["ischemic"]), T_episodes=len(meta[rec]["rate_related"]),
                     frozen_checkins=len(ci[rec]), baseline_checkins=len(ci_base[rec])))
recs = list(meta)
out = []
for name, c in (("baseline rtl K=3.8 (untuned)", ci_base), ("FROZEN " + cfg["selected_name"], ci)):
    m = DE.metrics(recs, meta, c, None)
    m = {k.replace("ischemic", "ST_change").replace("rate_related", "T_wave").replace("rate_", "T_wave_"): v for k, v in m.items()}
    out.append(dict(config=name, **m)); print(out[-1])
pd.DataFrame(out).to_csv("results/a2_edb_test.csv", index=False); pd.DataFrame(rows).to_csv("results/a2_edb_records.csv", index=False)
print("records used:", len(recs), "excluded:", len(EXCL))
