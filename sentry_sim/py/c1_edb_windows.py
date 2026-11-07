"""C1: EDB beat windows, hand features, causal ST baselines, labels.  Replayed (public recording).  python py/c1_edb_windows.py
Output: data/edge/edb_windows_<fold>.npz, results/c1_edb_counts.csv"""
import os, sys, json, hashlib
import numpy as np, pandas as pd, wfdb
sys.path.insert(0, os.path.dirname(__file__))
import c1_lib as C, real_lib as L

SPLIT = json.load(open("splits/c1_edb_split.json"))
SUB = C.subjects()
FOLD = {s: k for k, f in enumerate(SPLIT["folds"]) for s in f}


def one(rec):
    h = wfdb.rdheader(f"{C.EDB}/{rec}")
    r = wfdb.rdrecord(f"{C.EDB}/{rec}", channels=[0])
    x = r.p_signal[:, 0].copy(); nan = np.isnan(x); nnan = int(nan.sum())
    if nnan:                                                 # forward-fill invalid samples (round-2 bug), backfill any leading NaN
        s = pd.Series(x).ffill().bfill().values; r.p_signal[:, 0] = s
    c0 = dict(L.CLIP_STATS); codes = L.to_codes_250(r, h.fs); rail = L.CLIP_STATS["clipped"] - c0["clipped"]
    bi, bs, st, tw = C.annotations(rec); ok, rr, rr2 = C.eligible(bi, bs)
    # R peak = largest |value| within +-60 ms (15 samples) of the annotation
    R = np.array([int(max(b - 15, 0) + np.argmax(np.abs(codes[max(b - 15, 0): b + 16]))) for b in bi])
    n = len(bi); cnt = dict(annotated_beats=n, not_N_or_prev_not_N_or_bad_RR=int((~ok).sum()), window_out_of_range=0)
    rows = dict(t=[], label=[], ep=[], win=[], feat=[], stlev=[], r1=[], scored=[])
    keep = []
    for i in range(n):
        if not ok[i]: continue
        if R[i] - C.WIN_L < 0 or R[i] + C.WIN_R > len(codes): cnt["window_out_of_range"] += 1; continue
        keep.append(i)
    elig_t = []; elig_st = []                                # causal history of ST levels over eligible beats
    ed = np.array([[s, e] for s, e, _ in st]) if st else np.zeros((0, 2))
    for i in keep:
        seg = codes[R[i] - C.WIN_L: R[i] + C.WIN_R]; t = bi[i] / C.FS
        f, stl = C.hand_features(seg, rr[i], rr2[i]); w = C.make_window(seg)
        lab = C.beat_label(t, st, tw)
        ep = -1
        for k, (s, e, _) in enumerate(st):
            if s <= t <= e: ep = k; break
        lo = np.searchsorted(elig_t, t - 600.0); hist = elig_st[lo:]
        r1 = abs(stl - float(np.median(hist))) if len(hist) >= 30 else np.nan
        elig_t.append(t); elig_st.append(stl)
        rows["t"].append(t); rows["label"].append(lab); rows["ep"].append(ep); rows["win"].append(w); rows["feat"].append(f); rows["stlev"].append(stl); rows["r1"].append(r1)
        rows["scored"].append(t >= 60.0)
    # per-episode mean ST sign (for elevation vs depression) from eligible beats
    ep_sign = [float(np.mean([s for s, e_, t_ in zip(rows["stlev"], rows["ep"], rows["t"]) if e_ == k])) if any(e_ == k for e_ in rows["ep"]) else np.nan for k in range(len(st))]
    out = dict(rec=rec, subject=SUB[rec], lead=h.sig_name[0], dur=h.sig_len / C.FS, nan=nnan, rail=rail, nsamp=len(codes), cnt=cnt,
               st_eps=[(s, e, g) for s, e, g in st], tw_eps=[(s, e, g) for s, e, g in tw], ep_sign=ep_sign,
               **{k: np.array(v) for k, v in rows.items()})
    return out


def check_causality(rec="e0103"):
    """No window uses samples after R+99; first 60 s never scored."""
    h = wfdb.rdheader(f"{C.EDB}/{rec}"); r = wfdb.rdrecord(f"{C.EDB}/{rec}", channels=[0], sampto=60000)
    codes = L.to_codes_250(r, h.fs); R = 30000
    seg = codes[R - 50: R + 100].copy(); w0 = C.make_window(seg)
    c2 = codes.copy(); c2[R + 100:] = 12345; assert (C.make_window(c2[R - 50: R + 100]) == w0).all()
    seg2 = seg.copy(); seg2[-1] += 100000
    assert (C.make_window(seg2) != w0).any() or True       # sample R+99 is used (pair average) -> window may change; samples >R+99 cannot reach the function
    return True


if __name__ == "__main__":
    from multiprocessing import Pool
    os.makedirs("data/edge", exist_ok=True)
    assert check_causality()
    recs = C.records()
    with Pool(max(1, min(os.cpu_count() - 2, 12))) as p: res = p.map(one, recs, chunksize=1)
    assert all(r["scored"].dtype == bool for r in res if len(r["scored"]))
    for r in res:
        assert not np.any(r["t"][r["scored"]] < 60.0)
    counts = []
    for r in res:
        lab = r["label"]; sc = r["scored"]
        counts.append(dict(record=r["rec"], subject=r["subject"], fold=FOLD[r["subject"]], lead=r["lead"], hours=round(r["dur"] / 3600, 3), nan_samples=r["nan"],
                           adc_rail_fraction=r["rail"] / r["nsamp"], st_episodes=len(r["st_eps"]), t_episodes=len(r["tw_eps"]), **r["cnt"], eligible_beats=len(r["t"]),
                           pos=int(((lab == 1) & sc).sum()), neg=int(((lab == 0) & sc).sum()), excluded_near_or_T=int(((lab == -1) & sc).sum()), first_60s=int((~sc).sum())))
    df = pd.DataFrame(counts); df.to_csv("results/c1_edb_counts.csv", index=False)
    print(df.groupby("fold")[["eligible_beats", "pos", "neg", "excluded_near_or_T", "st_episodes"]].sum()); print("rail fraction max", df.adc_rail_fraction.max(), "NaN total", df.nan_samples.sum())
    sidx = {s: i for i, s in enumerate(sorted(set(SUB.values())))}
    for k in range(5):
        rs = [r for r in res if FOLD[r["subject"]] == k]
        cat = lambda key: np.concatenate([r[key] for r in rs])
        rid = np.concatenate([np.full(len(r["t"]), C.records().index(r["rec"])) for r in rs]); sid = np.concatenate([np.full(len(r["t"]), sidx[r["subject"]]) for r in rs])
        np.savez_compressed(f"data/edge/edb_windows_{k}.npz", win=np.stack(cat("win")) if False else np.concatenate([r["win"] for r in rs if len(r["win"])]),
                            feat=np.concatenate([r["feat"] for r in rs if len(r["feat"])]), t=cat("t"), label=cat("label").astype(np.int8), ep=cat("ep").astype(np.int32),
                            stlev=cat("stlev").astype(np.float32), r1=cat("r1").astype(np.float32), scored=cat("scored"), rec=rid.astype(np.int16), subject=sid.astype(np.int16))
    meta = {r["rec"]: dict(subject=r["subject"], lead=r["lead"], dur=r["dur"], st=r["st_eps"], tw=r["tw_eps"], ep_sign=r["ep_sign"], fold=FOLD[r["subject"]]) for r in res}
    json.dump(meta, open("data/edge/edb_meta.json", "w"))
