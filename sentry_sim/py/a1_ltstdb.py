"""A1 (round 2): heart-rate drift check-ins against labelled ST episodes in the Long-Term ST Database (ltstdb, ECG only, 86 records, 80 subjects).
Heart rate per beat = the database's own manually corrected beat annotations (.atr), so the beat detector is NOT in the loop.
ANNOTATION CRITERION: the .stc set (ST deviation >= 100 uV for >= 60 s).  Episode types from the annotation codes:
   '(stN ... stN)'      ischemic ST episode        <- the only positive class
   '(rtstN ... rtstN)'  heart-rate-related ST episode (reported separately, not counted as ischemia)
   'sstN' / 'ccst'      ST axis shift / conduction change marks (reported by count; excluded from the false-alarm time like the other labelled episodes)
Variants of the drift check-in:  rtl (K = 3.0/3.8/4.5, learning on the first 2^13 beats), avg60 / avg120 (causal moving average first),
   rest_proxy (ASSUMED PROXY, NO MOTION CHANNEL): heart rate (60 s mean) more than X % above the rolling 5th percentile of the previous 10 min for T minutes.
Metrics (per set of patients): ischemic-episode sensitivity (a check-in between 30 min before onset and the episode end), lead time (positive = before onset),
   false check-ins per 24 h counted only outside every labelled ST episode +-30 min, fraction of records with >= 1 false check-in.
Most ischemic episodes in this database follow heart-rate rises, which flatters a heart-rate-based detector.
Stages (rule 3):  prep -> writes data/a1/*, splits/a1_split.json | tune -> grid on TUNE patients, writes configs/a1_frozen.json | test -> once, on TEST patients | hint -> ST hint (.16a)
   python py/a1_ltstdb.py prep | tune | test | hint"""
import argparse, csv, datetime, glob, hashlib, json, os, random, re, sys
import numpy as np, pandas as pd, wfdb
sys.path.insert(0, os.path.dirname(__file__))
import drift_model as M
import drift_eval as DE

ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["prep", "tune", "test", "testgrid", "hint"]); a = ap.parse_args()
DB = "real_data/ltstdb"; OUT = "data/a1"; BEAT = set("NLRBAaJSVFejnE/fQ"); LOG2N = 13
KS = {"3.0": 144, "3.8": 230, "4.5": 324}


def prep():
    os.makedirs(OUT, exist_ok=True); meta = {}
    for f in sorted(glob.glob(f"{DB}/s*.hea")):
        rec = os.path.basename(f)[:-4]
        if not (os.path.exists(f"{DB}/{rec}.atr") and os.path.exists(f"{DB}/{rec}.stc")): continue
        h = wfdb.rdheader(f"{DB}/{rec}"); at = wfdb.rdann(f"{DB}/{rec}", "atr")
        t = np.array([s / 250.0 for s, sy in zip(at.sample, at.symbol) if sy in BEAT])
        rr = np.diff(t); ok = (rr > 0.3) & (rr < 2.0)
        np.savez(f"{OUT}/{rec}.npz", t=t[1:][ok], q=np.round(60.0 / rr[ok] * 16).astype(np.int64))
        st = wfdb.rdann(f"{DB}/{rec}", "stc"); open_ = {}; isch = []; rate = []; shifts = 0
        for s, aux in zip(st.sample, st.aux_note):
            aux = (aux or "").strip("\x00"); tt = s / 250.0
            m = re.match(r"^\((rt)?st(\d)", aux)
            if m: open_[(m[1] or "", m[2])] = tt; continue
            m = re.match(r"^(rt)?st(\d)[+-]?\d*\)", aux)
            if m:
                k = (m[1] or "", m[2])
                if k in open_: (rate if m[1] else isch).append([open_.pop(k), tt])
                continue
            if re.match(r"^s(cc)?st\d", aux): shifts += 1
        meta[rec] = dict(patient=rec[2:5], leads=int(rec[1]), dur_s=h.sig_len / 250.0, ischemic=merge(isch), rate_related=merge(rate), shift_marks=shifts, n_beats=int(len(t)))
    json.dump(meta, open(f"{OUT}/meta.json", "w"), indent=1)
    pats = sorted({v["patient"] for v in meta.values()}); has = {p: any(v["ischemic"] for v in meta.values() if v["patient"] == p) for p in pats}
    rng = random.Random(20261109); sp = dict(tune=[], test=[])
    for pos in (True, False):
        ids = [p for p in pats if has[p] == pos]; rng.shuffle(ids); h2 = (len(ids) + 1) // 2 if rng.random() < 0.5 else len(ids) // 2
        sp["tune"] += ids[:h2]; sp["test"] += ids[h2:]
    out = dict(dataset="LTSTDB", rule="seeded 50/50 by SUBJECT (record name digits 2-4), stratified by whether the subject has any ischemic episode", seed=20261109,
               written=datetime.datetime.now().isoformat(timespec="seconds"), note="Written before any A1 experiment (annotation parsing only).",
               tune=sorted(sp["tune"]), test=sorted(sp["test"]))
    json.dump(out, open("splits/a1_split.json", "w"), indent=2)
    print(len(meta), "records,", len(pats), "subjects; ischemic episodes", sum(len(v["ischemic"]) for v in meta.values()),
          "rate-related", sum(len(v["rate_related"]) for v in meta.values()), "| tune", len(out["tune"]), "test", len(out["test"]))


def checkins(rec, cfg):
    d = np.load(f"{OUT}/{rec}.npz"); return DE.checkins_tq(d["t"], d["q"], cfg)


cfg_name = DE.cfg_name; metrics = DE.metrics; merge = DE.merge


GRID = [("rtl", k) for k in KS] + [(v, k) for v in ("avg60", "avg120") for k in KS] + [("rest", x, t) for x in (15, 20, 25, 30) for t in (2, 5, 10)]

if a.stage == "prep": prep()
else:
    SPLIT = json.load(open("splits/a1_split.json")); meta = json.load(open(f"{OUT}/meta.json"))
    sel = lambda g: [r for r, v in meta.items() if v["patient"] in set(SPLIT[g])]
    if a.stage == "tune":
        recs = sel("tune"); rows = []
        for cfg in GRID:
            ci = {r: checkins(r, cfg) for r in recs}; m = metrics(recs, meta, ci, None)
            rows.append(dict(config=cfg_name(cfg), cfg=list(cfg), **m)); print(rows[-1]["config"], m["ischemic_sens"], m["false_per_24h"], flush=True)
        pd.DataFrame([{k: v for k, v in r.items() if k != "cfg"} for r in rows]).to_csv("results/a1_tune_grid.csv", index=False)
        ok = [r for r in rows if r["false_per_24h"] != "" and r["false_per_24h"] <= 1.0]
        best = max(ok, key=lambda r: (r["ischemic_sens"] or 0, -r["false_per_24h"])) if ok else min(rows, key=lambda r: (r["false_per_24h"], -(r["ischemic_sens"] or 0)))
        cfg = dict(experiment="A1 LTSTDB drift", chosen_on=f"TUNE subjects ({len(SPLIT['tune'])}): {len(recs)} records", selected=best["cfg"], selected_name=best["config"],
                   any_config_met_1_per_24h=bool(ok), selection_rule="<=1 false check-in per 24 h on tune, then highest ischemic-episode sensitivity; else lowest false rate",
                   tune_row={k: v for k, v in best.items() if k != "cfg"}, baseline=["rtl", "3.8"], annotation_set=".stc (100 uV, 60 s)", log2n=LOG2N,
                   frozen_at=datetime.datetime.now().isoformat(timespec="seconds"), split_file_sha256=hashlib.sha256(open("splits/a1_split.json", "rb").read()).hexdigest())
        json.dump(cfg, open("configs/a1_frozen.json", "w"), indent=2); print(json.dumps(cfg, indent=2))
    elif a.stage == "test":
        cfg = json.load(open("configs/a1_frozen.json")); assert cfg["split_file_sha256"] == hashlib.sha256(open("splits/a1_split.json", "rb").read()).hexdigest()
        recs = sel("test"); rows = []
        for name, c in (("baseline rtl K=3.8 (untuned)", tuple(cfg["baseline"])), ("FROZEN " + cfg["selected_name"], tuple(cfg["selected"]))):
            ci = {r: checkins(r, c) for r in recs}; rows.append(dict(config=name, **metrics(recs, meta, ci, None))); print(rows[-1])
        pd.DataFrame(rows).to_csv("results/a1_test.csv", index=False)
    elif a.stage == "testgrid":
        # DESCRIPTIVE ONLY: every pre-defined setting on the TEST subjects, for the sensitivity-vs-false-rate figure; no selection is made from it (the choice is frozen)
        recs = sel("test"); rows = []
        for cfgx in GRID:
            ci = {r: checkins(r, cfgx) for r in recs}; rows.append(dict(config=cfg_name(cfgx), **metrics(recs, meta, ci, None))); print(rows[-1]["config"], rows[-1]["ischemic_sens"], rows[-1]["false_per_24h"], flush=True)
        pd.DataFrame(rows).to_csv("results/a1_test_grid_descriptive.csv", index=False)
    else:
        print("hint stage runs after the .16a files are downloaded (py/a1_hint.py)")
