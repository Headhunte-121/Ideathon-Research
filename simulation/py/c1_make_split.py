"""C1 step 1: write splits/c1_edb_split.json (5 folds of SUBJECTS) from annotations only, before any experiment.
Rule: subjects with >=1 ST episode sorted by positive-beat count (desc, seeded tie shuffle) and greedily given to the fold with the fewest positive beats
(then fewest subjects); subjects without ST episodes dealt to the fold with the fewest subjects.  Seed 20261107."""
import json, hashlib, datetime, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import c1_lib as C

SEED = 20261107
if __name__ == "__main__":
    sub = C.subjects(); info = {}
    for r in C.records():
        bi, bs, st, tw = C.annotations(r); ok, rr, _ = C.eligible(bi, bs)
        t = bi / C.FS; pos = int(sum(any(s <= x <= e for s, e, _ in st) for x in t[ok]))
        d = info.setdefault(sub[r], dict(records=[], st_eps=0, pos=0)); d["records"].append(r); d["st_eps"] += len(st); d["pos"] += pos
    rng = np.random.default_rng(SEED)
    ids = sorted(info); rng.shuffle(ids)
    withst = sorted([s for s in ids if info[s]["st_eps"] > 0], key=lambda s: -info[s]["pos"])
    nost = [s for s in ids if info[s]["st_eps"] == 0]
    folds = [dict(subjects=[], pos=0) for _ in range(5)]
    for s in withst:
        f = min(folds, key=lambda f: (f["pos"], len(f["subjects"]))); f["subjects"].append(s); f["pos"] += info[s]["pos"]
    for s in nost:
        f = min(folds, key=lambda f: len(f["subjects"])); f["subjects"].append(s)
    out = dict(name="c1_edb_split", seed=SEED, created=datetime.datetime.now().isoformat(timespec="seconds"),
               rule=__doc__.split("\n", 1)[1], subject_rule="records with identical header comments (age, sex, diagnosis; Recorder/Medications ignored) = one subject",
               folds=[sorted(f["subjects"]) for f in folds], fold_positive_beats=[f["pos"] for f in folds],
               subject_records={s: info[s]["records"] for s in sorted(info)}, subject_st_episodes={s: info[s]["st_eps"] for s in sorted(info)})
    os.makedirs("splits", exist_ok=True); json.dump(out, open("splits/c1_edb_split.json", "w"), indent=1)
    print([len(f) for f in out["folds"]], out["fold_positive_beats"], hashlib.sha256(open("splits/c1_edb_split.json", "rb").read()).hexdigest())
