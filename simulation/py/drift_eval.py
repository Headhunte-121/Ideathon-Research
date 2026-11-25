"""Shared drift check-in evaluation for A1 (LTSTDB) and A2 (EDB).  Generated from py/a1_ltstdb.py; the metric definitions are documented there."""
import numpy as np, pandas as pd
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import drift_model as M
KS = {"3.0": 144, "3.8": 230, "4.5": 324}; LOG2N = 13


def merge(iv):
    iv = sorted(iv); out = []
    for s, e in iv:
        if out and s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)
        else: out.append([s, e])
    return out


def checkins_tq(t, q, cfg):
    if cfg[0] in ("rtl", "avg60", "avg120"):
        feat = q if cfg[0] == "rtl" else M.smooth_feature(q, 60 if cfg[0] == "avg60" else 120)
        idx = M.run_rtl_replica(feat, KS[cfg[1]], LOG2N=LOG2N, return_edges=True)
        return [float(t[i]) for i in idx]
    X, T = cfg[1], cfg[2]                                            # rest_proxy
    n = int(t[-1]) + 1; sec = t.astype(int); hr = q / 16.0
    s = np.bincount(sec, weights=hr, minlength=n); c = np.bincount(sec, minlength=n)
    h = np.where(c > 0, s / np.maximum(c, 1), np.nan); h = pd.Series(h).ffill().bfill().values
    base = pd.Series(h).shift(1).rolling(600, min_periods=300).quantile(0.05).values
    cur = pd.Series(h).rolling(60, min_periods=30).mean().values
    over = cur > (1 + X / 100.0) * base; out = []; run = 0
    for i in range(len(over)):
        run = run + 1 if over[i] else 0
        if run == T * 60: out.append(float(i))
    return out


def metrics(recs, meta, ci, bylist):
    """ci: dict rec -> list of check-in times (s)"""
    isch_n = isch_c = rate_n = rate_c = 0; leads = []; false = 0; hours = 0.0; recs_false = 0
    for rec in recs:
        m = meta[rec]; c = np.array(sorted(ci[rec])); dur = m["dur_s"]
        for key in ("ischemic", "rate_related"):
            for s, e in m[key]:
                hit = c[(c >= s - 1800) & (c <= e)]
                if key == "ischemic":
                    isch_n += 1; isch_c += len(hit) > 0
                    if len(hit): leads.append((s - hit[0]) / 60.0)
                else: rate_n += 1; rate_c += len(hit) > 0
        excl = merge([[max(0, s - 1800), e + 1800] for key in ("ischemic", "rate_related") for s, e in m[key]])
        ok = np.ones(len(c), bool)
        for s, e in excl: ok &= ~((c >= s) & (c <= e))
        f = int(ok.sum()); false += f; recs_false += f > 0
        hours += (dur - sum(min(e, dur) - max(s, 0) for s, e in excl)) / 3600.0
    return dict(records=len(recs), ischemic_episodes=isch_n, ischemic_caught=isch_c, ischemic_sens=round(isch_c / isch_n, 3) if isch_n else "",
                median_lead_min=round(float(np.median(leads)), 1) if leads else "", rate_episodes=rate_n, rate_caught=rate_c,
                false_checkins=false, nonepisode_hours=round(hours, 1), false_per_24h=round(false * 24.0 / hours, 2) if hours else "", records_with_false=recs_false,
                fraction_records_with_false=round(recs_false / len(recs), 3))


def cfg_name(c): return f"{c[0]} K={c[1]}" if c[0] in ("rtl", "avg60", "avg120") else f"rest_proxy +{c[1]}% for {c[2]} min"


