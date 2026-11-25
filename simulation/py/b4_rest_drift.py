"""B4 (round 2): does feeding the drift detector only REST beats fix its blindness?  PPG-DaLiA, heart rate per beat = output of the Verilog beat
detector on the chest ECG (data/b3/det_S*.txt, bpm*16).  Rest = chest motion <= 5x the person's own sitting median (as in E5).
Two streams through the SAME detector logic (py/drift_model.py, the checked Python copy of baseline_drift_detector.sv), same K:
   ALL   : every beat in time order
   REST  : only beats that fall in rest seconds
Learning = first 2^LOG2N beats of the stream (LOG2N = 10, about 13 min of beats).  A step of +10/+15/+25 % (Simulated) is added to every REST beat
after the time T_inj = the time of the rest beat at 60 % of the rest stream.  False check-ins: rising edges without any step (ALL: all time after
learning; REST: rest time after learning).  Detection counted only for people not already flagged at T_inj.  K in {3.0, 3.8, 4.5} chosen on the TUNE people.
Only about 2 h per person, so the learning period is short compared with the 24 h design.
   python py/b4_rest_drift.py --stage tune | --stage test         Output: results/b4_*.csv, configs/b4_frozen.json"""
import argparse, csv, datetime, hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import drift_model as M

ap = argparse.ArgumentParser(); ap.add_argument("--stage", choices=["tune", "test"], required=True); a = ap.parse_args()
SPLIT = json.load(open("splits/dalia_split.json"))
KS = {"3.0": 144, "3.8": 230, "4.5": 324}; LOG2N = 10; STEPS = (10, 15, 25)


def load(sub):
    s = int(sub[1:]); f = np.load(f"data/b3/S{s}.npz"); n = int(f["n"])
    det = np.loadtxt(f"data/b3/det_S{s}.txt", dtype=int, ndmin=2)
    t = det[:, 0] / 250.0; q = det[:, 1]
    ok = (q >= 30 * 16) & (q <= 200 * 16) & (t < n); t, q = t[ok], q[ok]
    rest = f["chest_rel"] <= 5.0
    isrest = rest[np.floor(t).astype(int)]
    return dict(t=t, q=q, rest=isrest, hours=n / 3600.0)


def run(stream_t, stream_q, k2, step, tinj):
    q = stream_q.copy()
    if step: q = np.where(stream_t >= tinj, q + (q * step) // 100, q)
    first_idx = int(np.searchsorted(stream_t, tinj)) if step else None
    e, first = M.run_rtl_replica(q, k2, LOG2N=LOG2N, first_after=first_idx)
    flag = M.run_rtl_replica(q[:first_idx], k2, LOG2N=LOG2N, return_state=True)[2] if step else False
    delay = None
    if step and first >= 0: delay = (stream_t[first_idx + first] - tinj) / 60.0
    return e, delay, (not flag)


def evaluate(subs, data, kname, with_steps=True):
    k2 = KS[kname]; out = []
    for mode in ("ALL", "REST"):
        fa = 0; hours = 0.0; pfa = 0; det = {s: [0, 0, []] for s in STEPS}; used = 0
        for sub in subs:
            d = data[sub]
            if d["rest"].sum() < (1 << LOG2N) + 600: continue                     # too little rest to learn and test
            used += 1
            tr, qr = d["t"][d["rest"]], d["q"][d["rest"]]
            tinj = tr[int(0.6 * len(tr))]
            t, q = (d["t"], d["q"]) if mode == "ALL" else (tr, qr)
            if len(t) <= (1 << LOG2N) + 100: continue
            e = run(t, q, k2, 0, tinj)[0]
            tl = t[(1 << LOG2N)]                                                   # time learning ends
            span = (t[-1] - tl) / 3600.0
            fa += e; hours += span; pfa += e > 0
            if mode == "REST": pass
            for st in STEPS:
                # the step is applied to REST beats only: build the stream with the injection on rest beats
                if mode == "ALL":
                    q2 = d["q"].copy(); m = d["rest"] & (d["t"] >= tinj); q2[m] = q2[m] + (q2[m] * st) // 100
                    idx = int(np.searchsorted(d["t"], tinj)); ee, first = M.run_rtl_replica(q2, k2, LOG2N=LOG2N, first_after=idx)
                    _, _, fl = M.run_rtl_replica(q2[:idx], k2, LOG2N=LOG2N, return_state=True)
                    ok = not fl; dl = (d["t"][idx + first] - tinj) / 60.0 if first >= 0 else None
                else:
                    _, dl, ok = run(t, q, k2, st, tinj)
                if ok:
                    det[st][1] += 1
                    if dl is not None: det[st][0] += 1; det[st][2].append(dl)
        row = dict(stream=mode, K=kname, people_used=used, false_checkins=fa, stream_hours=round(hours, 2), false_per_hour=round(fa / hours, 3) if hours else "",
                   people_with_false=pfa)
        for st in STEPS:
            row[f"caught_{st}pct"] = f"{det[st][0]}/{det[st][1]}"; row[f"median_delay_min_{st}pct"] = round(float(np.median(det[st][2])), 1) if det[st][2] else ""
        out.append(row)
    return out


if a.stage == "tune":
    data = {s: load(s) for s in SPLIT["tune"]}; rows = []
    for kn in KS: rows += evaluate(SPLIT["tune"], data, kn)
    with open("results/b4_tune.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    def score(kn):                      # same K for both streams: fewest false check-ins per hour (sum over streams), then most steps caught in REST
        rr = [r for r in rows if r["K"] == kn]
        fa = sum(float(r["false_per_hour"] or 0) for r in rr)
        rest = [r for r in rr if r["stream"] == "REST"][0]
        caught = sum(int(rest[f"caught_{s}pct"].split("/")[0]) for s in STEPS)
        return (fa, -caught)
    best = min(KS, key=score)
    cfg = dict(experiment="B4 rest-only drift", chosen_on="TUNE people only: " + ",".join(SPLIT["tune"]), K=best, K2X16=KS[best], LOG2N=LOG2N,
               rest_rule="chest motion <= 5x own sitting median", steps_tested=list(STEPS), frozen_at=datetime.datetime.now().isoformat(timespec="seconds"),
               split_file_sha256=hashlib.sha256(open("splits/dalia_split.json", "rb").read()).hexdigest())
    json.dump(cfg, open("configs/b4_frozen.json", "w"), indent=2); print(json.dumps(cfg, indent=2))
    for r in rows: print(r)
else:
    cfg = json.load(open("configs/b4_frozen.json"))
    assert cfg["split_file_sha256"] == hashlib.sha256(open("splits/dalia_split.json", "rb").read()).hexdigest()
    data = {s: load(s) for s in SPLIT["test"]}
    rows = evaluate(SPLIT["test"], data, cfg["K"])
    with open("results/b4_test.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    for r in rows: print(r)
