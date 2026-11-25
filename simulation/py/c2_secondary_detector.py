"""C2.7: frozen fold-0 M2 (seed 0), R0, R1 on fold-0 test records using beats found by py/beat_model.py (Python port of our detector) instead of annotations.
Replayed end to end through the Python port of our detector (not bit-exact RTL).  -> results/c2_secondary_detector.csv"""
import os, sys, json, pickle
import numpy as np, pandas as pd, wfdb, torch
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E, c1_lib as C, real_lib as L, beat_model as B
SPLIT = json.load(open("splits/c1_edb_split.json")); SUB = C.subjects()
RECS = [r for r in C.records() if SUB[r] in SPLIT["folds"][0]]


def one(rec):
    h = wfdb.rdheader(f"{C.EDB}/{rec}"); r = wfdb.rdrecord(f"{C.EDB}/{rec}", channels=[0]); import pandas as pd
    x = r.p_signal[:, 0]
    if np.isnan(x).any(): r.p_signal[:, 0] = pd.Series(x).ffill().bfill().values
    codes = L.to_codes_250(r, h.fs); det = np.array(B.detect(codes), dtype=int)
    R = np.array([int(max(d - 15, 0) + np.argmax(np.abs(codes[max(d - 15, 0): d + 16]))) for d in det])
    _, _, st, tw = C.annotations(rec); rows = []; hist_t = []; hist_s = []; prev = None; prev2 = None
    for i in range(1, len(R)):
        rr = (R[i] - R[i - 1]) / C.FS
        if not (0.4 <= rr <= 1.5) or R[i] - 50 < 0 or R[i] + 100 > len(codes): continue
        t = R[i] / C.FS; rr2 = (R[i - 1] - R[i - 2]) / C.FS if i >= 2 else np.nan
        seg = codes[R[i] - 50: R[i] + 100]; f, stl = C.hand_features(seg, rr, rr2); w = C.make_window(seg)
        lo = np.searchsorted(hist_t, t - 600.0); hh = hist_s[lo:]
        r1 = abs(stl - float(np.median(hh))) if len(hh) >= 30 else np.nan
        hist_t.append(t); hist_s.append(stl)
        rows.append((rec, t, C.beat_label(t, st, tw), abs(stl), r1, w))
    return rows, len(det)

if __name__ == "__main__":
    from multiprocessing import Pool
    torch.set_num_threads(4)
    with Pool(min(len(RECS), 14)) as p: res = p.map(one, RECS)
    rows = [r for rr, _ in res for r in rr]; ndet = sum(n for _, n in res)
    df = pd.DataFrame([r[:5] for r in rows], columns=["rec", "t", "label", "R0", "R1"]); win = np.stack([r[5] for r in rows])
    ck = torch.load("data/edge/models/m2_f0_s0.pt"); net = E.BeatNet(); net.load_state_dict(ck["state"]); net.eval()
    with torch.no_grad(): df["M2"] = torch.cat([net.score(E.to_input(win[i:i + 8192])) for i in range(0, len(win), 8192)]).numpy()
    thr = json.load(open("results/c2_deployed_thresholds.json"))
    # val-fold thresholds are those stored for fold 0 (derived from annotated beats of the validation fold; unchanged)
    ok = (df.t >= 60) & df.R1.notna() & (df.label >= 0); d = df[ok]
    S0 = np.load("data/edge/c2_scores_fold0.npz"); ma = S0["ok"] & (S0["label"] >= 0)
    out = []
    for m, key in (("R0", "R0"), ("R1", "R1"), ("M2_s0", "M2")):
        y = d.label.values; s = d[key].values; sens, _ = E.sens_at_fpr(s[y == 1], s[y == 0]); t = thr[m]["0"]
        sa = S0[m][ma]; ya = (S0["label"][ma] == 1); sensa, _ = E.sens_at_fpr(sa[ya], sa[~ya])
        out.append(dict(method=m, beats_python_detector=len(d), beats_annotated=int(ma.sum()), detections_total=ndet, sens_1pctFPR_detected_beats=sens, sens_1pctFPR_annotated_beats=sensa,
                        change=sens - sensa, AUROC_detected=E.auroc(y, s), AUROC_annotated=E.auroc(ya.astype(int), sa), deployed_sens_detected=float((s[y == 1] > t).mean()), deployed_FPR_detected=float((s[y == 0] > t).mean())))
    pd.DataFrame(out).to_csv("results/c2_secondary_detector.csv", index=False); print(pd.DataFrame(out).round(3).to_string())
