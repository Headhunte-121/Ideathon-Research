"""C2 evaluation on the stored outer-test scores (no re-scoring).  Replayed.   python py/c2_eval.py
Outputs results/c2_beat_metrics.csv, c2_bootstrap.csv, c2_episode_metrics.csv, c2_failure_analysis.csv, figures."""
import os, sys, json, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E, drift_eval as DE, c1_lib as C
import torch

CFG = json.load(open("configs/c2_frozen.json"))
META = json.load(open("data/edge/edb_meta.json")); RECS = C.records()
METHODS = ["R0", "R1", "M1", "M2_s0", "M2_s1", "M2_s2"]
S = [dict(np.load(f"data/edge/c2_scores_fold{k}.npz")) for k in range(5)]


def thresholds():
    thr = {m: {} for m in METHODS}
    for k in range(5):
        v = S[(k + 1) % 5]; mk = v["ok"] & (v["label"] == 0)
        thr["R0"][k] = E.thr_at_fpr(v["R0"][mk]); thr["R1"][k] = E.thr_at_fpr(v["R1"][mk])
        thr["M1"][k] = pickle.load(open(f"data/edge/models/m1_f{k}.pkl", "rb"))["thr"]
        for s in range(3): thr[f"M2_s{s}"][k] = torch.load(f"data/edge/models/m2_f{k}_s{s}.pt")["thr"]
    return thr


def beat_sets(k):
    d = S[k]; m = d["ok"] & (d["label"] >= 0); return m, (d["label"][m] == 1).astype(int)


def beat_metrics(thr):
    rows = []
    pooled = {m: [[], []] for m in METHODS}
    for m in METHODS:
        tp_c = tn_c = fp_c = pos_c = neg_c = tpc_c = 0
        for k in range(5):
            mk, y = beat_sets(k); s = S[k][m][mk]; pos, neg = s[y == 1], s[y == 0]
            sens, t1 = E.sens_at_fpr(pos, neg, 0.01); dep = thr[m][k]
            rows.append(dict(method=m, fold=k, n_pos=len(pos), n_neg=len(neg), prevalence=round(len(pos) / len(y), 4), AUROC=E.auroc(y, s), AUPRC=E.auprc(y, s),
                             sens_at_1pct_FPR_curve=sens, deployed_sens=float((pos > dep).mean()), deployed_FPR=float((neg > dep).mean())))
            tpc_c += (pos > t1).sum(); tp_c += (pos > dep).sum(); fp_c += (neg > dep).sum(); pos_c += len(pos); neg_c += len(neg)
            pooled[m][0].append(s); pooled[m][1].append(y)
        s = np.concatenate(pooled[m][0]); y = np.concatenate(pooled[m][1])
        rows.append(dict(method=m, fold="pooled", n_pos=pos_c, n_neg=neg_c, prevalence=round(pos_c / (pos_c + neg_c), 4), AUROC=E.auroc(y, s), AUPRC=E.auprc(y, s),
                         sens_at_1pct_FPR_curve=tpc_c / pos_c, deployed_sens=tp_c / pos_c, deployed_FPR=fp_c / neg_c))
    # clinical-style R0 point |ST| >= 100 uV
    tp = fp = p = n = 0
    for k in range(5):
        mk, y = beat_sets(k); s = S[k]["R0"][mk]; tp += (s[y == 1] >= 100).sum(); fp += (s[y == 0] >= 100).sum(); p += (y == 1).sum(); n += (y == 0).sum()
    rows.append(dict(method="R0 at |ST|>=100uV", fold="pooled", n_pos=p, n_neg=n, deployed_sens=tp / p, deployed_FPR=fp / n))
    return pd.DataFrame(rows)


def bootstrap(nb=2000, seed=7):
    rng = np.random.default_rng(seed)
    subs = sorted(set(np.concatenate([S[k]["subject"][S[k]["ok"] & (S[k]["label"] >= 0)] for k in range(5)]).tolist())); sidx = {s: i for i, s in enumerate(subs)}
    prep = {}
    for k in range(5):
        mk, y = beat_sets(k); sid = np.array([sidx[s] for s in S[k]["subject"][mk]])
        for m in METHODS:
            sc = S[k][m][mk]; pn = np.where(y == 0)[0]; pp = np.where(y == 1)[0]
            on = np.argsort(sc[pn]); op = np.argsort(sc[pp])
            prep[(k, m)] = (sc[pn][on], sid[pn][on], sc[pp][op], sid[pp][op])
    nsub = len(subs); res = {m: np.zeros(nb) for m in METHODS}; tot = {}
    for b in range(nb):
        w = np.bincount(rng.integers(0, nsub, nsub), minlength=nsub).astype(np.float64)
        for m in METHODS:
            tp = pos = 0.0
            for k in range(5):
                sn, idn, sp, idp = prep[(k, m)]; wn = w[idn]; cw = np.cumsum(wn)
                if cw[-1] == 0: continue
                j = np.searchsorted(cw, 0.99 * cw[-1]); thr = sn[min(j, len(sn) - 1)]
                wp = w[idp]; pos += wp.sum(); tp += wp[sp > thr].sum()
            res[m][b] = tp / pos if pos else np.nan
    pt = beat_metrics_point = {}
    for m in METHODS:
        tp = pos = 0
        for k in range(5):
            sn, idn, sp, idp = prep[(k, m)]; thr = np.quantile(sn, 0.99); tp += (sp > thr).sum(); pos += len(sp)
        pt[m] = tp / pos
    m2 = np.mean([res[f"M2_s{s}"] for s in range(3)], axis=0); m2pt = np.mean([pt[f"M2_s{s}"] for s in range(3)])
    best = "R0" if pt["R0"] >= pt["R1"] else "R1"
    rows = []
    def ci(x): return tuple(np.nanpercentile(x, [2.5, 97.5]))
    for m in ["R0", "R1", "M1"]:
        rows.append(dict(quantity=f"{m} sens@1%FPR (curve)", point=pt[m], lo=ci(res[m])[0], hi=ci(res[m])[1]))
    rows.append(dict(quantity="M2 (mean of 3 seeds) sens@1%FPR (curve)", point=m2pt, lo=ci(m2)[0], hi=ci(m2)[1]))
    for s in range(3): rows.append(dict(quantity=f"M2 seed {s} sens@1%FPR (curve)", point=pt[f"M2_s{s}"], lo=ci(res[f"M2_s{s}"])[0], hi=ci(res[f"M2_s{s}"])[1]))
    for name, ref, rp in (("better rule (" + best + ")", res[best], pt[best]), ("R0", res["R0"], pt["R0"]), ("R1", res["R1"], pt["R1"]), ("M1", res["M1"], pt["M1"])):
        d = m2 - ref; rows.append(dict(quantity=f"M2 - {name}", point=m2pt - rp, lo=ci(d)[0], hi=ci(d)[1]))
    df = pd.DataFrame(rows); df["note"] = f"subject bootstrap {nb} resamples, per-fold 1% FPR thresholds from resampled negatives, pooled over 5 folds"
    return df, best


def persistence_alerts(rec_mask_scores, t, thr, win, need):
    return E.alerts(t, rec_mask_scores > thr, win, need)


def episode_metrics(thr, win=30, need=24, methods=METHODS):
    out = {}
    for m in methods:
        n_ep = caught = 0; leads = []; false = 0; hours = 0.0; recs_f = 0; nrec = 0; per_ep = []
        for k in range(5):
            d = S[k]
            for ri in np.unique(d["rec"]):
                rec = RECS[ri]; mt = META[rec]; sel = (d["rec"] == ri) & d["ok"]; t = d["t"][sel]
                al = E.alerts(t, d[m][sel] > thr[m][k], win, need) if m in thr else E.alerts(t, d[m][sel] > 100, win, need)
                st, tw = mt["st"], mt["tw"]; nrec += 1
                for ei, (s, e, g) in enumerate(st):
                    hit = al[(al >= s) & (al <= e)]; n_ep += 1; caught += len(hit) > 0
                    if len(hit): leads.append((s - hit[0]) / 60.0)
                    per_ep.append(dict(method=m, rec=rec, subject=mt["subject"], lead=mt["lead"], ep=ei, onset=s, end=e, dur_min=(e - s) / 60, sign=mt["ep_sign"][ei], caught=int(len(hit) > 0)))
                ex = C.merge([[max(0, s - 1800), e + 1800] for s, e, _ in st + tw])
                ok = np.ones(len(al), bool)
                for s, e in ex: ok &= ~((al >= s) & (al <= e))
                false += int(ok.sum()); recs_f += int(ok.sum() > 0)
                hours += (mt["dur"] - 60.0 - sum(min(e, mt["dur"]) - max(s, 60.0) for s, e in ex if min(e, mt["dur"]) > max(s, 60.0))) / 3600.0
        out[m] = dict(method=m, window=f"{need}/{win}", episodes=n_ep, caught=caught, sensitivity=caught / n_ep, median_lead_min=float(np.median(leads)) if leads else np.nan,
                      false_alerts=false, episode_free_hours=round(hours, 1), false_per_24h=false * 24.0 / hours, records_with_false=recs_f, records=nrec, per_ep=per_ep)
    return out


def drift_rows():
    cfg = json.load(open("configs/a1_frozen.json")); rows = []
    meta = {}; ci = {r: {} for r in ("rtl", "rest")}
    for rec in RECS:
        bi, bs, st, tw = C.annotations(rec); t = bi / C.FS; rr = np.diff(t); ok = (rr > 0.3) & (rr < 2.0)
        tt, q = t[1:][ok], np.round(60.0 / rr[ok] * 16).astype(np.int64)
        meta[rec] = dict(dur_s=META[rec]["dur"], ischemic=DE.merge([[s, e] for s, e, _ in st]), rate_related=DE.merge([[s, e] for s, e, _ in tw]))
        ci["rtl"][rec] = DE.checkins_tq(tt, q, ("rtl", "3.8")); ci["rest"][rec] = DE.checkins_tq(tt, q, tuple(cfg["selected"]))
    for name, key in (("drift: rtl K=3.8", "rtl"), ("drift: A1 frozen " + cfg["selected_name"], "rest")):
        m = DE.metrics(RECS, meta, ci[key], None); rows.append(dict(method=name, episodes=m["ischemic_episodes"], caught=m["ischemic_caught"], sensitivity=m["ischemic_sens"],
                                                                   median_lead_min=m["median_lead_min"], false_alerts=m["false_checkins"], episode_free_hours=m["nonepisode_hours"],
                                                                   false_per_24h=m["false_per_24h"], records_with_false=m["records_with_false"], records=m["records"], window="(heart-rate drift)"))
    return rows


def failure(thr, eps):
    d_rows = []
    for m in ("R0", "M2_s0"):
        for lab, sel_fn in (("hr<60", lambda f: f[:, 4] < 60), ("hr 60-80", lambda f: (f[:, 4] >= 60) & (f[:, 4] < 80)), ("hr 80-100", lambda f: (f[:, 4] >= 80) & (f[:, 4] < 100)), ("hr>=100", lambda f: f[:, 4] >= 100)):
            tp = n = 0
            for k in range(5):
                mk, y = beat_sets(k); f = S[k]["feat"][mk]; s = S[k][m][mk]; c = sel_fn(f) & (y == 1); n += c.sum(); tp += (s[c] > thr[m][k]).sum()
            d_rows.append(dict(method=m, group="heart-rate band", value=lab, positive_beats=int(n), beat_sensitivity=tp / n if n else np.nan))
        leads = {}; subj = {}
        for k in range(5):
            mk, y = beat_sets(k); s = S[k][m][mk]; r = S[k]["rec"][mk]; sb = S[k]["subject"][mk]
            for ri in np.unique(r[y == 1]):
                c = (r == ri) & (y == 1); h = (s[c] > thr[m][k]); ld = META[RECS[ri]]["lead"]; a = leads.setdefault(ld, [0, 0]); a[0] += h.sum(); a[1] += len(h)
                a = subj.setdefault(META[RECS[ri]]["subject"], [0, 0]); a[0] += h.sum(); a[1] += len(h)
        for ld, (a, b) in sorted(leads.items()): d_rows.append(dict(method=m, group="lead (channel 0)", value=ld, positive_beats=b, beat_sensitivity=a / b))
        low = sorted(subj.items(), key=lambda kv: kv[1][0] / kv[1][1])[:5]
        for sname, (a, b) in low: d_rows.append(dict(method=m, group="5 lowest-sensitivity subjects", value=sname, positive_beats=b, beat_sensitivity=a / b))
        pe = pd.DataFrame(eps[m]["per_ep"])
        pe["sgn"] = np.where(pe.sign > 0, "ST elevation (mean ST>0)", "ST depression (mean ST<0)")
        for g, df in pe.groupby("sgn"): d_rows.append(dict(method=m, group="episode ST sign", value=g, positive_beats=len(df), beat_sensitivity=df.caught.mean(), note="episode-level"))
        q1, q2 = pe.dur_min.quantile([1 / 3, 2 / 3])
        for g, df in (("shortest third", pe[pe.dur_min <= q1]), ("middle third", pe[(pe.dur_min > q1) & (pe.dur_min <= q2)]), ("longest third", pe[pe.dur_min > q2])):
            d_rows.append(dict(method=m, group="episode duration", value=f"{g} ({df.dur_min.min():.1f}-{df.dur_min.max():.1f} min)", positive_beats=len(df), beat_sensitivity=df.caught.mean(), note="episode-level"))
    return pd.DataFrame(d_rows)


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    thr = thresholds(); bm = beat_metrics(thr); bm.to_csv("results/c2_beat_metrics.csv", index=False); print(bm[bm.fold == "pooled"].round(3).to_string())
    bt, best = bootstrap(); bt.to_csv("results/c2_bootstrap.csv", index=False); print(bt.round(3).to_string()); print("better rule:", best)
    eps = episode_metrics(thr); eps["R0 at 100uV"] = episode_metrics({**thr, "R0": {k: 100.0 for k in range(5)}}, methods=["R0"])["R0"]; eps["R0 at 100uV"]["method"] = "R0 at |ST|>=100uV"
    rows = [{k: v for k, v in e.items() if k != "per_ep"} for e in eps.values()]
    # persistence sensitivity rows (same 80% rule): 15 beats (need 12), 60 beats (need 48)
    for win, need in ((15, 12), (60, 48)):
        for m, e in episode_metrics(thr, win, need).items(): rows.append({k: v for k, v in e.items() if k != "per_ep"})
    rows += drift_rows()
    ep = pd.DataFrame(rows); ep.to_csv("results/c2_episode_metrics.csv", index=False); print(ep.round(3).to_string())
    fa = failure(thr, eps); fa.to_csv("results/c2_failure_analysis.csv", index=False); print(fa.round(3).to_string())
    json.dump({m: {str(k): v for k, v in t.items()} for m, t in thr.items()}, open("results/c2_deployed_thresholds.json", "w"), indent=1)
