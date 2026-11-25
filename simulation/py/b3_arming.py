"""B3 (round 2): arming conditions on PPG-DaLiA.  Counts FALSE ARMS (runs of at least H seconds in which the arming condition holds for a
LIVING person) per person-hour, with dispatch delay as the cost.
Condition per second:  wrist pulse lost (pulse size < loss_frac x own sitting median)  AND chest not moving (<= 5x own sitting median)
   [AND wrist still: wrist-accelerometer variation <= X x own sitting median]
   [AND no ECG veto: veto = at least one beat of the Verilog beat detector at 30-180 bpm in the last 3 s]
The ECG veto would also suppress PEA (electrical activity, no pulse); DaLiA cannot test that.
Stages (rule 3):   python py/b3_arming.py --stage tune     -> grid on the TUNE people, writes configs/b3_frozen.json
                   (freeze/commit the config)               python py/b3_arming.py --stage test     -> frozen config + baseline on the TEST people, once
Split: splits/dalia_split.json.   Needs data/b3/S*.npz, data/b3/det_S*.txt (py/b3_features.py, py/b3_ecg_rtl.py)."""
import argparse, csv, datetime, hashlib, itertools, json, os
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("--stage", choices=["tune", "test"], required=True); a = ap.parse_args()
SPLIT = json.load(open("splits/dalia_split.json"))
ACT = {0: "transient", 1: "sitting", 2: "stairs", 3: "table soccer", 4: "cycling", 5: "driving", 6: "lunch", 7: "walking", 8: "working"}
HOLDS = (3, 5, 10); WRIST_X = (None, 3, 5, 10); ECG = (False, True); DEFAULT_LOSS = 0.15


def load(sub):
    s = int(sub[1:]); f = np.load(f"data/b3/S{s}.npz"); n = int(f["n"])
    det = np.loadtxt(f"data/b3/det_S{s}.txt", dtype=int, ndmin=2)
    t = det[:, 0] / 250.0 if det.size else np.array([]); hr = det[:, 1] / 16.0 if det.size else np.array([])
    ok = (hr >= 30) & (hr <= 180); t = t[ok]
    cnt = np.zeros(n + 3, int)
    sec = np.floor(t).astype(int); sec = sec[sec < n]; np.add.at(cnt, sec, 1)
    present = np.array([cnt[max(0, i - 2): i + 1].sum() > 0 for i in range(n)])      # a valid beat in seconds i-2..i
    return dict(label=f["label"], pp=f["pp_rel"], wr=f["wrist_rel"], ch=f["chest_rel"], veto=present, n=n)


def runs(cond, hold):
    out = []; i = 0
    while i < len(cond):
        if cond[i]:
            j = i
            while j < len(cond) and cond[j]: j += 1
            if j - i >= hold: out.append(i)
            i = j
        else: i += 1
    return out


def count(D, loss, wx, ecg, hold):
    c = (D["pp"] < loss) & (D["ch"] <= 5.0)
    if wx is not None: c &= (D["wr"] <= wx)
    if ecg: c &= ~D["veto"]
    return runs(c, hold)


def evaluate(subs, data, loss, wx, ecg, hold):
    per = {s: count(data[s], loss, wx, ecg, hold) for s in subs}
    hours = sum(data[s]["n"] for s in subs) / 3600.0
    tot = sum(len(v) for v in per.values())
    byact = {}
    for s, v in per.items():
        for i in v: byact[ACT[int(data[s]["label"][i])]] = byact.get(ACT[int(data[s]["label"][i])], 0) + 1
    return dict(false_arms=tot, person_hours=round(hours, 1), per_person_hour=round(tot / hours, 3), people_affected=sum(1 for v in per.values() if v),
                worst_person=max(per, key=lambda k: len(per[k])), worst_person_arms=max(len(v) for v in per.values()), by_activity=byact)


def key(r):
    return (r["per_person_hour"], r["hold_s"], (r["wrist_still_x"] is not None) + r["ecg_veto"])


if a.stage == "tune":
    data = {s: load(s) for s in SPLIT["tune"]}
    rows = []
    for hold, wx, ecg in itertools.product(HOLDS, WRIST_X, ECG):
        r = evaluate(SPLIT["tune"], data, DEFAULT_LOSS, wx, ecg, hold)
        rows.append(dict(hold_s=hold, wrist_still_x=wx, ecg_veto=ecg, added_dispatch_delay_s=hold - 3, **{k: v for k, v in r.items() if k != "by_activity"}))
    with open("results/b3_tune_grid.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    best = min(rows, key=key)
    cfg = dict(experiment="B3 arming conditions", chosen_on="TUNE people only: " + ",".join(SPLIT["tune"]), loss_frac=DEFAULT_LOSS, chest_moving_x=5.0,
               hold_s=best["hold_s"], wrist_still_x=best["wrist_still_x"], ecg_veto=best["ecg_veto"], ecg_veto_rule="a Verilog-detector beat at 30-180 bpm in the last 3 s",
               tune_result=dict(false_arms=best["false_arms"], per_person_hour=best["per_person_hour"]),
               baseline_tune=[dict(false_arms=r["false_arms"], per_person_hour=r["per_person_hour"]) for r in rows if (r["hold_s"], r["wrist_still_x"], r["ecg_veto"]) == (3, None, False)][0],
               frozen_at=datetime.datetime.now().isoformat(timespec="seconds"), split_file_sha256=hashlib.sha256(open("splits/dalia_split.json", "rb").read()).hexdigest())
    json.dump(cfg, open("configs/b3_frozen.json", "w"), indent=2)
    print(json.dumps(cfg, indent=2))
else:
    cfg = json.load(open("configs/b3_frozen.json"))
    assert cfg["split_file_sha256"] == hashlib.sha256(open("splits/dalia_split.json", "rb").read()).hexdigest(), "split changed after freezing"
    data = {s: load(s) for s in SPLIT["test"]}
    rows = []; acts = []
    # The tune people had NO false arms at baseline, so tuning could not choose anything and the frozen config is the plain baseline.
    # The variants below are a PRE-SPECIFIED grid taken from round 1 (not selected on test).  Round 1 had already seen the two people who
    # produce the false arms (S5, S8), so this grid is NOT an independent test of the fix.
    GRID = [("PRE-SPECIFIED: hold 5 s", (5, None, False)), ("PRE-SPECIFIED: hold 10 s", (10, None, False)),
            ("PRE-SPECIFIED: wrist still 5x", (3, 5, False)), ("PRE-SPECIFIED: ECG veto", (3, None, True)),
            ("PRE-SPECIFIED: ECG veto + wrist still 5x", (3, 5, True))]
    for name, (hold, wx, ecg) in [("baseline (round-1 definition)", (3, None, False)), ("FROZEN variant", (cfg["hold_s"], cfg["wrist_still_x"], cfg["ecg_veto"]))] + GRID:
        for loss in (0.10, 0.15, 0.25):
            r = evaluate(SPLIT["test"], data, loss, wx, ecg, hold)
            rows.append(dict(config=name, loss_frac=loss, hold_s=hold, wrist_still_x=wx, ecg_veto=ecg, added_dispatch_delay_s=hold - 3,
                             **{k: v for k, v in r.items() if k != "by_activity"}))
            if loss == 0.15:
                for k, v in r["by_activity"].items(): acts.append(dict(config=name, activity=k, false_arms=v))
    with open("results/b3_test.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open("results/b3_test_per_activity.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["config", "activity", "false_arms"]); w.writeheader(); w.writerows(acts)
    for r in rows: print(r)
