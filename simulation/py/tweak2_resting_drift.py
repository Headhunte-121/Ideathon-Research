"""Tweak 2: heart-rate drift warning on RESTING heart rate only (PPG-DaLiA, 15 people).  Heart rate per beat = dataset R-peaks.
Two setups are reported side by side:
  POOLED  : rest = chest not moving AND activity label sitting or working.  Learn on the first 10 rest-minutes, test on the rest.
            (What the device could do if "resting" = "chest still"; it cannot tell sitting from working.)
  WORKING : rest = chest not moving AND label working only; learn on the first 5 rest-minutes.  UPPER BOUND ONLY: it uses an activity
            label the device does not have, to show what a separate baseline per context would give.
Rules:   PLAIN: 60 s mean resting HR > (1+T) x own baseline for 5 minutes in a row, T = 10/15/20 %     SIGMA: the Verilog detector's logic
(py/drift_model.py) on the rest-only beats.   Injected step (SIMULATED, on real recordings): +10/+15/+25 % over the last 10 (POOLED) or 8 (WORKING)
rest-minutes.  False alarms counted without injection.  Detection counted only among people NOT already alarming just before the step.
Tune on S1-S8, test on S9-S15 (fixed in advance).   python -I py/tweak2_resting_drift.py --dir real_data/ppg_dalia/PPG_FieldStudy
Output: results/tweak2_resting_drift.csv, results/tweak2_selection.txt, results/tweak2_context_hr.csv"""
import argparse, csv, os, pickle, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import drift_model as M

ap = argparse.ArgumentParser(); ap.add_argument("--dir", required=True); a = ap.parse_args()
TUNE = list(range(1, 9)); TEST = list(range(9, 16)); HOLD = 300
THRS = (0.10, 0.15, 0.20); STEPS = (10, 15, 25)
SETUPS = {"POOLED": dict(labels=(1, 8), learn=600, inj=600), "WORKING (labels used: upper bound)": dict(labels=(8,), learn=300, inj=480)}


def beats(s):
    with open(os.path.join(a.dir, f"S{s}", f"S{s}.pkl"), "rb") as fh: d = pickle.load(fh, encoding="latin1")
    rp = np.asarray(d["rpeaks"]).ravel() / 700.0
    rr = np.diff(rp); ok = (rr > 0.3) & (rr < 2.0)
    return rp[1:][ok], 60.0 / rr[ok]


def rest_series(s, labels, t, hr):
    f = np.load(f"data/dalia_feats/S{s}.npz")
    rest = np.isin(f["label"], labels) & ~f["chest_moving"]; n = len(rest)
    sec = np.floor(t).astype(int); keep = sec < n
    sec, h = sec[keep], hr[keep]
    cum = np.cumsum(rest) - rest
    m = rest[sec]
    return h[m], cum[sec[m]], int(rest.sum())


def per_rest_second(h, rs, nrest):
    out = np.full(nrest, np.nan)
    sums = np.bincount(rs, weights=h, minlength=nrest)[:nrest]; cnt = np.bincount(rs, minlength=nrest)[:nrest]
    out[cnt > 0] = sums[cnt > 0] / cnt[cnt > 0]
    last = np.nan
    for i in range(nrest):
        if np.isnan(out[i]): out[i] = last
        else: last = out[i]
    out[np.isnan(out)] = out[~np.isnan(out)][0]
    return out


def plain(hs, thr, step, learn, injlen):
    x = hs.copy(); n = len(x); inj = n - injlen
    if step: x[inj:] *= 1 + step / 100.0
    base = x[:learn].mean()
    c = np.convolve(x, np.ones(60) / 60, mode="full")[:n]
    over = c > (1 + thr) * base
    run = 0; alarms = 0; first = -1; eligible = True
    for i in range(learn, n):
        if i == inj: eligible = (run == 0)
        run = run + 1 if over[i] else 0
        if run == HOLD:
            alarms += 1
            if step and i >= inj and first < 0: first = i - inj
    return alarms, first, eligible


def sigma(h, rs, step, learn, injlen, k2=230):
    nl = int(np.searchsorted(rs, learn)); log2n = max(int(np.floor(np.log2(max(nl, 64)))), 6)
    q = np.round(h * 16).astype(np.int64)
    inj = int(np.searchsorted(rs, rs.max() - injlen)) if len(rs) else 0
    if step: q = q.copy(); q[inj:] = q[inj:] + (q[inj:] * step) // 100
    e, first = M.run_rtl_replica(q, k2, LOG2N=log2n, first_after=inj if step else None)
    _, _, flag = M.run_rtl_replica(q[:inj] if step else q, k2, LOG2N=log2n, return_state=True)
    return e, first, ((not flag) if step else True)


B = {s: beats(s) for s in TUNE + TEST}
ctx = []
rows = []; excluded = {}
for setup, cfg in SETUPS.items():
    data = {}
    for s in TUNE + TEST:
        h, rs, nrest = rest_series(s, cfg["labels"], *B[s])
        if nrest < cfg["learn"] + 600 + (300 if len(cfg["labels"]) > 1 else 0):
            excluded.setdefault(setup, []).append((s, nrest)); continue
        data[s] = (h, rs, nrest, per_rest_second(h, rs, nrest))
    for group, subs in (("tune", TUNE), ("test", TEST)):
        subs = [s for s in subs if s in data]
        rest_hours = sum(data[s][2] - cfg["learn"] for s in subs) / 3600.0
        for rule, param in [("PLAIN", t) for t in THRS] + [("SIGMA", 3.8)]:
            r = dict(setup=setup, group=group, people=len(subs), rule=rule,
                     param=(f"+{int(param*100)}% for 5 min" if rule == "PLAIN" else "K=3.8 (RTL logic)"), test_rest_hours=round(rest_hours, 2))
            fa = 0; pfa = 0
            for s in subs:
                h, rs, nrest, hs = data[s]
                e = (plain(hs, param, 0, cfg["learn"], cfg["inj"]) if rule == "PLAIN" else sigma(h, rs, 0, cfg["learn"], cfg["inj"]))[0]
                fa += e; pfa += e > 0
            r["false_alarms"] = fa; r["false_alarms_per_rest_hour"] = round(fa / rest_hours, 2); r["people_with_false_alarm"] = pfa
            for st in STEPS:
                det = 0; el = 0; delays = []
                for s in subs:
                    h, rs, nrest, hs = data[s]
                    al, first, ok = (plain(hs, param, st, cfg["learn"], cfg["inj"]) if rule == "PLAIN" else sigma(h, rs, st, cfg["learn"], cfg["inj"]))
                    if not ok: continue
                    el += 1
                    if first >= 0:
                        det += 1; delays.append(first / 60.0 if rule == "PLAIN" else first / max(len(h), 1) * rs.max() / 60.0)
                r[f"detected_step_{st}pct"] = f"{det}/{el}"
                r[f"median_delay_min_{st}pct"] = round(float(np.median(delays)), 1) if delays else ""
            rows.append(r); print(r, flush=True)
with open("results/tweak2_resting_drift.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

lines = [f"Excluded (too little rest time): {excluded}"]
for setup in SETUPS:
    tune = [r for r in rows if r["setup"] == setup and r["group"] == "tune"]
    ok = [r for r in tune if r["false_alarms"] == 0] or tune
    def score(r): return sum(int(r[f"detected_step_{s}pct"].split("/")[0]) / max(int(r[f"detected_step_{s}pct"].split("/")[1]), 1) for s in STEPS)
    best = max(ok, key=lambda r: (-r["false_alarms"], score(r)))
    lines.append(f"[{setup}] selected on the TUNE people only (fewest false alarms, then most steps detected): {best['rule']} {best['param']}")
    for r in rows:
        if r["setup"] == setup and (r["rule"], r["param"]) == (best["rule"], best["param"]):
            lines.append(f"    {r['group']} ({r['people']} people, {r['test_rest_hours']} rest-h): false alarms {r['false_alarms']} ({r['false_alarms_per_rest_hour']}/rest-h), "
                         f"detected +10%: {r['detected_step_10pct']}, +15%: {r['detected_step_15pct']}, +25%: {r['detected_step_25pct']}")
open("results/tweak2_selection.txt", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))

# context difference in resting heart rate (chest still): why a single baseline fails
for s in TUNE + TEST:
    t, hr = B[s]; f = np.load(f"data/dalia_feats/S{s}.npz"); sec = np.floor(t).astype(int); k = sec < len(f["label"])
    sec, h = sec[k], hr[k]
    def m(lbl):
        sel = (f["label"][sec] == lbl) & ~f["chest_moving"][sec]
        return float(h[sel].mean()) if sel.sum() > 50 else float("nan")
    ctx.append(dict(subject=s, hr_sitting_still=round(m(1), 1), hr_working_still=round(m(8), 1)))
with open("results/tweak2_context_hr.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(ctx[0].keys())); w.writeheader(); w.writerows(ctx)
