"""A3 (round 2): how much does ST alone carry for telling a real heart attack (MI) from a normal ECG?   PTB-XL, Python only (not RTL).
10-second RESTING DIAGNOSTIC 12-lead ECGs: this is NOT early warning, NOT a wearable, NOT a sternal lead.
Labels: diagnostic superclass from scp_statements.csv (MI vs NORM; a record is MI if any diagnostic SCP code belongs to MI, NORM if all belong to NORM).
Folds: the dataset's own, train 1-8, validate 9, test 10.   Records at 100 Hz, resampled to 250 Hz, 0.5 Hz zero-phase high-pass.
Beats from the Python port of rtl/ecg_beat_detector.sv (py/beat_model.py); R peak = largest |sample| within +-60 ms of the detection.
Per lead (I, II, V2, V5) features from the median beat (robust):  ST level (R+110 ms, an ASSUMED stand-in for J+60 ms, relative to the PR-segment level R-80..-40 ms),
ST slope (R+80 to R+140 ms), T amplitude (largest deviation R+150..+350 ms), Q depth (R-60..R), heart rate.
Models: logistic regression (standardised), C chosen on fold 9 by AUC; threshold = Youden point on fold 9.  Sets: ST only (level+slope) | all five | heart rate only.
   python py/a3_ptbxl.py features | tune | test         Output: results/a3_*.csv, configs/a3_frozen.json"""
import argparse, ast, csv, datetime, hashlib, json, os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))

LEADS = {"I": 0, "II": 1, "V2": 7, "V5": 10}
SETS = {"ST only": ["st_level", "st_slope"], "all five": ["st_level", "st_slope", "t_amp", "q_depth", "hr"], "heart rate only": ["hr"]}
CS = (0.01, 0.1, 1.0, 10.0)
ROOT = "real_data/ptbxl"


def labels():
    db = pd.read_csv(f"{ROOT}/ptbxl_database.csv", index_col="ecg_id"); sc = pd.read_csv(f"{ROOT}/scp_statements.csv", index_col=0)
    sc = sc[sc.diagnostic == 1]
    sup = db.scp_codes.apply(lambda s: {sc.loc[k, "diagnostic_class"] for k in ast.literal_eval(s) if k in sc.index})
    db["label"] = np.where(sup.apply(lambda x: "MI" in x), 1, np.where(sup.apply(lambda x: x == {"NORM"}), 0, -1))
    return db[db.label >= 0]


def one(args):
    ecg_id, fn = args
    import wfdb
    from scipy.signal import resample_poly, butter, sosfiltfilt
    import beat_model as B
    rec = wfdb.rdrecord(f"{ROOT}/{fn}"); out = []
    sos = butter(2, 0.5, "highpass", fs=250.0, output="sos")
    for name, k in LEADS.items():
        x = rec.p_signal[:, k]
        if np.isnan(x).any(): out.append(dict(ecg_id=ecg_id, lead=name)); continue
        y = sosfiltfilt(sos, resample_poly(x, 5, 2)) * 1000.0                      # uV at 250 Hz
        det = B.detect(np.clip(np.round(y * 16.0), -32768, 32767).astype(np.int64))
        r = [int(d - 15 + np.argmax(np.abs(y[max(d - 15, 0): d + 15]))) for d in det if 40 < d < len(y) - 100]
        if len(r) < 3: out.append(dict(ecg_id=ecg_id, lead=name)); continue
        f = {"st_level": [], "st_slope": [], "t_amp": [], "q_depth": []}
        for i in r:
            if i + 90 >= len(y) or i - 25 < 0: continue
            iso = np.median(y[i - 20: i - 10]); s = lambda ms: y[i + int(round(ms * 0.25))] - iso
            f["st_level"].append(s(110)); f["st_slope"].append((s(140) - s(80)) / 60.0)
            seg = y[i + 38: i + 88] - iso; f["t_amp"].append(seg[np.argmax(np.abs(seg))])
            f["q_depth"].append(max(0.0, iso - y[i - 15: i + 1].min()))
        if not f["st_level"]: out.append(dict(ecg_id=ecg_id, lead=name)); continue
        d = {kk: float(np.median(v)) for kk, v in f.items()}; d["hr"] = float(60.0 / (np.median(np.diff(r)) / 250.0)) if len(r) > 2 else np.nan
        out.append(dict(ecg_id=ecg_id, lead=name, **d))
    return out


def auc_ci(y, p, n=1000, seed=7):
    from sklearn.metrics import roc_auc_score
    rng = np.random.default_rng(seed); base = roc_auc_score(y, p); bs = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].min() != y[i].max(): bs.append(roc_auc_score(y[i], p[i]))
    return base, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def wilson(k, n):
    z = 1.96; p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - m) / d, (c + m) / d


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["features", "tune", "test"]); a = ap.parse_args()
    if a.stage == "features":
        from multiprocessing import Pool
        db = labels(); os.makedirs("data/a3", exist_ok=True)
        with Pool(4) as p: res = p.map(one, list(zip(db.index, db.filename_lr)), chunksize=50)
        df = pd.DataFrame([r for rr in res for r in rr]).merge(db[["label", "strat_fold"]], left_on="ecg_id", right_index=True)
        df.to_csv("data/a3/features.csv", index=False); print(len(db), "records;", df.dropna(subset=["st_level"]).shape[0], "lead-rows with features;", int(db.label.sum()), "MI,", int((db.label == 0).sum()), "NORM")
    else:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        from sklearn.metrics import roc_auc_score
        df = pd.read_csv("data/a3/features.csv")

        def XY(lead, cols, folds):
            d = df[(df.lead == lead) & df.strat_fold.isin(folds)]
            return d[cols].copy(), d.label.values
        def fit(lead, cols, C):
            Xtr, ytr = XY(lead, cols, range(1, 9)); med = Xtr.median()
            m = make_pipeline(StandardScaler(), LogisticRegression(C=C, class_weight="balanced", max_iter=1000)).fit(Xtr.fillna(med), ytr)
            return m, med
        if a.stage == "tune":
            cfg = dict(experiment="A3 PTB-XL MI vs NORM", chosen_on="fold 9 (validation); trained on folds 1-8", models={}, frozen_at=datetime.datetime.now().isoformat(timespec="seconds"))
            rows = []
            for lead in LEADS:
                for sname, cols in SETS.items():
                    best = None
                    for C in CS:
                        m, med = fit(lead, cols, C); Xv, yv = XY(lead, cols, [9]); pv = m.predict_proba(Xv.fillna(med))[:, 1]
                        auc = roc_auc_score(yv, pv)
                        if best is None or auc > best[0]: best = (auc, C, pv, yv)
                    auc, C, pv, yv = best
                    from sklearn.metrics import roc_curve
                    fpr, tpr, thr = roc_curve(yv, pv); t = float(thr[np.argmax(tpr - fpr)])
                    cfg["models"][f"{lead}|{sname}"] = dict(C=C, threshold=t, val_auc=round(auc, 4))
                    rows.append(dict(lead=lead, features=sname, C=C, threshold=round(t, 4), val_auc_fold9=round(auc, 4)))
            json.dump(cfg, open("configs/a3_frozen.json", "w"), indent=2)
            pd.DataFrame(rows).to_csv("results/a3_tune_fold9.csv", index=False); print(pd.DataFrame(rows).to_string(index=False))
        else:
            cfg = json.load(open("configs/a3_frozen.json")); rows = []
            for key, m_ in cfg["models"].items():
                lead, sname = key.split("|"); cols = SETS[sname]
                m, med = fit(lead, cols, m_["C"]); Xt, yt = XY(lead, cols, [10]); pt = m.predict_proba(Xt.fillna(med))[:, 1]
                auc, lo, hi = auc_ci(yt, pt); pred = pt >= m_["threshold"]
                tp = int(((pred == 1) & (yt == 1)).sum()); fn = int(((pred == 0) & (yt == 1)).sum()); tn = int(((pred == 0) & (yt == 0)).sum()); fp = int(((pred == 1) & (yt == 0)).sum())
                sl = wilson(tp, tp + fn); sp = wilson(tn, tn + fp)
                rows.append(dict(lead=lead, features=sname, test_records=len(yt), MI=int(yt.sum()), AUC=round(auc, 3), AUC_95CI=f"{lo:.3f}-{hi:.3f}", sensitivity=round(tp / (tp + fn), 3),
                                 sens_95CI=f"{sl[0]:.3f}-{sl[1]:.3f}", specificity=round(tn / (tn + fp), 3), spec_95CI=f"{sp[0]:.3f}-{sp[1]:.3f}"))
            pd.DataFrame(rows).to_csv("results/a3_test_fold10.csv", index=False); print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
