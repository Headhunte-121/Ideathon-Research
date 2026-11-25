"""A4: what does the ECG side of the Pod's "no valid heartbeat" logic do in REAL arrests?  SDDB (VF onsets, Holter) + CUDB (VT/VF excerpts).
Beat times: Verilog detector on onset windows / CUDB records (data/a4/det_*.txt, SIMULATOR) and the Python port on whole SDDB records (data/a4/beats_py_*.npy).
Flags evaluated each second:
  POD      : seconds since the last detector beat >= 6   (pod_node.sv: nobeat_s >= NOBEAT_S = 6; the Pod only uses it when the wrist band is silent)
  RATE     : beats in the last 5 s imply a rate above 180 bpm (>= 16 beats) or below 30 bpm (<= 2 beats)        [proposal]
  IRR      : coefficient of variation (std/mean) of the last 8 RR intervals > c, c chosen on the TUNE records       [proposal]
  PROPOSAL : RATE or IRR
Selection rule (fixed before looking at test): among c in {0.2,0.3,0.4,0.5,0.7} with at most 1 false flag episode per hour on the TUNE records' pre-onset
sinus time, take the c with the most TUNE onsets flagged within 60 s; if none qualifies take the lowest false rate.
   python py/a4_analysis.py --stage tune | --stage test            splits/a4_split.json, configs/a4_episodes.json"""
import argparse, csv, datetime, hashlib, json, os
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("--stage", choices=["tune", "test"], required=True); a = ap.parse_args()
SPLIT = json.load(open("splits/a4_split.json")); EPS = json.load(open("configs/a4_episodes.json")); META = json.load(open("data/a4/win_meta.json"))
CS = (0.4, 0.7, 1.0, 1.2, 1.5, 2.0); LOWS = ("5s<=2", "10s<=4", "off")


def beats_window(key):
    db, rec = key.split("/")
    det = np.loadtxt(f"data/a4/det_{db}_{rec}.txt", dtype=int, ndmin=2)
    t = det[:, 0] / 250.0 + META[key]["offset_s"] if det.size else np.array([])
    return t


def beats_full(key):
    db, rec = key.split("/"); return np.load(f"data/a4/beats_py_{db}_{rec}.npy")


def flags(beats, ticks, c, low="5s<=2"):
    """boolean arrays POD, RATE, IRR at the given tick times (seconds)"""
    idx = np.searchsorted(beats, ticks, side="right") - 1
    last = np.where(idx >= 0, beats[np.maximum(idx, 0)], -1e9)
    pod = (ticks - last) >= 6.0
    n5 = np.searchsorted(beats, ticks, side="right") - np.searchsorted(beats, ticks - 5.0, side="right")
    n10 = np.searchsorted(beats, ticks, side="right") - np.searchsorted(beats, ticks - 10.0, side="right")
    lowrule = (n5 <= 2) if low == "5s<=2" else ((n10 <= 4) if low == "10s<=4" else np.zeros(len(ticks), bool))
    rate = (n5 >= 16) | lowrule
    rr = np.diff(beats)
    if len(rr) >= 8:
        cs = np.concatenate([[0], np.cumsum(rr)]); cs2 = np.concatenate([[0], np.cumsum(rr ** 2)])
        m = (cs[8:] - cs[:-8]) / 8.0; v = (cs2[8:] - cs2[:-8]) / 8.0 - m ** 2
        cv = np.sqrt(np.maximum(v, 0)) / m                       # CV at beat index k+8 (uses rr[k:k+8])
        cvb = np.full(len(beats), np.nan); cvb[8:8 + len(cv)] = cv
        irr = np.where(idx >= 0, np.nan_to_num(cvb[np.maximum(idx, 0)], nan=0.0), 0.0) > c
    else:
        irr = np.zeros(len(ticks), bool)
    return pod, rate, irr


def first_true(mask, ticks, t0):
    sel = np.where(mask & (ticks >= t0))[0]; return float(ticks[sel[0]] - t0) if len(sel) else None


def episode_rows(keys, c, low="5s<=2"):
    rows = []
    for key in keys:
        v = EPS[key]
        for e in v["episodes"]:
            t0 = e["start_s"]
            if key.startswith("sddb"):
                t1 = min(t0 + 300.0, v["dur_s"]); beats = beats_window(key)
            else:
                t1 = e["end_s"]; beats = beats_window(key)
            ticks = np.arange(t0 - 30.0, t1, 1.0)
            pod, rate, irr = flags(beats, ticks, c, low)
            during = (ticks >= t0)
            b = beats[(beats >= t0) & (beats < t1)]
            rows.append(dict(record=key, kind=e["kind"], onset_s=round(t0, 1), analysed_s=round(t1 - t0, 1), beats_in_episode=len(b),
                             beats_per_min=round(len(b) / max((t1 - t0) / 60.0, 1e-9), 1), median_bpm=round(float(np.median(60.0 / np.diff(b))), 1) if len(b) > 2 else "",
                             pct_seconds_with_beat_in_last_6s=round(100 * float(np.mean(~pod[during])), 1),
                             t_to_POD_s=first_true(pod, ticks, t0), t_to_RATE_s=first_true(rate, ticks, t0), t_to_IRR_s=first_true(irr, ticks, t0),
                             t_to_PROPOSAL_s=first_true(rate | irr, ticks, t0), flagged_before_onset_PROPOSAL=bool((rate | irr)[ticks < t0].any())))
    return rows


def false_rows(keys, c, low="5s<=2"):
    rows = []
    for key in keys:
        if not key.startswith("sddb"): continue
        v = EPS[key]; beats = beats_full(key)
        lo = 600.0; hi = (v["episodes"][0]["start_s"] - 600.0) if v["episodes"] else v["dur_s"]
        if hi - lo < 1800: continue
        ticks = np.arange(lo, hi, 1.0); pod, rate, irr = flags(beats, ticks, c, low)
        edges = lambda m: int(((m[1:] & ~m[:-1]).sum()) + (1 if m[0] else 0))
        hrs = (hi - lo) / 3600.0
        rows.append(dict(record=key, has_vf_onset=bool(v["episodes"]), hours=round(hrs, 2), POD_flags=edges(pod), RATE_flags=edges(rate), IRR_flags=edges(irr),
                         PROPOSAL_flags=edges(rate | irr), POD_per_h=round(edges(pod) / hrs, 2), PROPOSAL_per_h=round(edges(rate | irr) / hrs, 2)))
    return rows


def agg(rows, col): return sum(r[col] for r in rows) / sum(r["hours"] for r in rows)


if a.stage == "tune":
    keys = SPLIT["tune"]; res = []
    for low, c in [(l, c_) for l in LOWS for c_ in CS]:
        ep = [r for r in episode_rows([k for k in keys if k.startswith("sddb")], c, low) if r["kind"] == "VF"]
        fl = false_rows(keys, c, low)
        det60 = sum(1 for r in ep if r["t_to_IRR_s"] is not None and r["t_to_IRR_s"] <= 60 or (r["t_to_RATE_s"] is not None and r["t_to_RATE_s"] <= 60))
        res.append(dict(low_rate_rule=low, c=c, tune_onsets=len(ep), onsets_flagged_within_60s_RATE_or_IRR=det60, false_RATE_or_IRR_per_h=round(agg(fl, "PROPOSAL_flags"), 2),
                        false_POD_per_h=round(agg(fl, "POD_flags"), 2)))
    with open("results/a4_tune_grid.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys())); w.writeheader(); w.writerows(res)
    ok = [r for r in res if r["false_RATE_or_IRR_per_h"] <= 1.0]
    best = max(ok, key=lambda r: (r["onsets_flagged_within_60s_RATE_or_IRR"], -r["false_RATE_or_IRR_per_h"])) if ok else min(res, key=lambda r: (r["false_RATE_or_IRR_per_h"], -r["onsets_flagged_within_60s_RATE_or_IRR"]))
    cfg = dict(experiment="A4 arrest ECG logic", chosen_on="TUNE records only (" + str(len([k for k in keys if k.startswith('sddb')])) + " SDDB + " + str(len([k for k in keys if k.startswith('cudb')])) + " CUDB)",
               irregularity_cv_threshold=best["c"], low_rate_rule=best["low_rate_rule"], any_setting_met_1_per_hour=bool(ok), rate_limits_bpm=[30, 180], rate_window_s=5, irr_window_beats=8, pod_nobeat_s=6,
               selection_rule="<=1 false flag/h on tune pre-onset sinus time, then most tune onsets flagged within 60 s", tune_row=best,
               frozen_at=datetime.datetime.now().isoformat(timespec="seconds"), split_file_sha256=hashlib.sha256(open("splits/a4_split.json", "rb").read()).hexdigest())
    json.dump(cfg, open("configs/a4_frozen.json", "w"), indent=2); print(json.dumps(cfg, indent=2)); [print(r) for r in res]
else:
    cfg = json.load(open("configs/a4_frozen.json")); c = cfg["irregularity_cv_threshold"]; low = cfg["low_rate_rule"]
    assert cfg["split_file_sha256"] == hashlib.sha256(open("splits/a4_split.json", "rb").read()).hexdigest()
    keys = SPLIT["test"]
    ep = episode_rows(keys, c, low); fl = false_rows(keys, c, low)
    for name, rows in (("a4_test_episodes.csv", ep), ("a4_test_false_flags.csv", fl)):
        with open("results/" + name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("episodes", len(ep)); [print(r) for r in ep]; print("false", [(r["record"], r["hours"], r["POD_per_h"], r["PROPOSAL_per_h"]) for r in fl])
