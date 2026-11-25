"""C2 train stage: M1 (per fold) and M2 (per fold x seed) trained on 3 training folds; epoch / C / thresholds chosen on the inner-validation fold ONLY.  No outer-test scoring here.
   python py/c2_train.py        -> data/edge/models/*, results/c2_train_log.csv"""
import os, sys, json, time, pickle, hashlib
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
CFG = json.load(open("configs/c2_frozen.json"))
assert hashlib.sha256(open("splits/c1_edb_split.json", "rb").read()).hexdigest() == CFG["split_sha256"]


def gather(folds):
    import edge_nets as E
    ds = [E.load_fold(k) for k in folds]; out = {}
    for key in ("win", "feat", "label", "stlev", "r1", "t", "ok", "scored"):
        out[key] = np.concatenate([d[key] for d in ds])
    m = out["scored"] & (out["label"] >= 0)
    return {k: v[m] for k, v in out.items()}


def job(a):
    kind, k, seed = a
    import torch, edge_nets as E
    torch.set_num_threads(1)
    val = (k + 1) % 5; trf = [f for f in range(5) if f not in (k, val)]
    tr, va = gather(trf), gather([val]); t0 = time.time()
    if kind == "M1":
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        best = None
        for C in CFG["M1"]["C_grid"]:
            m = make_pipeline(StandardScaler(), LogisticRegression(C=C, class_weight="balanced", max_iter=2000)).fit(tr["feat"], tr["label"])
            s = m.decision_function(va["feat"]); ap = E.auprc(va["label"], s)
            if best is None or ap > best[0]: best = (ap, C, m, s)
        ap, C, m, s = best
        thr = E.thr_at_fpr(s[va["label"] == 0]); pickle.dump(dict(model=m, thr=thr, C=C), open(f"data/edge/models/m1_f{k}.pkl", "wb"))
        return dict(kind=kind, fold=k, seed=-1, val_auprc=ap, thr=thr, note=f"C={C}", epochs=0, sec=time.time() - t0)
    rs = 1000 * k + seed; rng = np.random.default_rng(rs); torch.manual_seed(rs)
    net = E.BeatNet(); opt = torch.optim.Adam(net.parameters(), lr=CFG["optimiser"]["lr"], weight_decay=CFG["optimiser"]["weight_decay"])
    pos = np.where(tr["label"] == 1)[0]; neg = np.where(tr["label"] == 0)[0]
    xv = E.to_input(va["win"]); best = (-1, None, 0); bad = 0; hist = []
    for ep in range(CFG["optimiser"]["max_epochs"]):
        net.train(); idx = np.concatenate([pos, rng.choice(neg, size=len(pos), replace=len(neg) < len(pos))]); rng.shuffle(idx)
        for i in range(0, len(idx), CFG["optimiser"]["batch"]):
            b = idx[i:i + CFG["optimiser"]["batch"]]
            x = E.to_input(tr["win"][b]); y = torch.from_numpy(tr["label"][b].astype(np.int64))
            loss = torch.nn.functional.cross_entropy(net(x), y); opt.zero_grad(); loss.backward(); opt.step()
        net.eval()
        with torch.no_grad(): sv = torch.cat([net.score(xv[i:i + 8192]) for i in range(0, len(xv), 8192)]).numpy()
        ap = E.auprc(va["label"], sv); hist.append(ap)
        if ap > best[0]: best = (ap, {k_: v.clone() for k_, v in net.state_dict().items()}, ep, sv.copy()); bad = 0
        else:
            bad += 1
            if bad >= CFG["early_stopping"]["patience"]: break
    net.load_state_dict(best[1]); thr = E.thr_at_fpr(best[3][va["label"] == 0])
    torch.save(dict(state=best[1], thr=thr, epoch=best[2], hist=hist), f"data/edge/models/m2_f{k}_s{seed}.pt")
    return dict(kind=kind, fold=k, seed=seed, val_auprc=best[0], thr=thr, note=f"best_epoch={best[2]}", epochs=len(hist), sec=time.time() - t0)


if __name__ == "__main__":
    from multiprocessing import Pool
    os.makedirs("data/edge/models", exist_ok=True)
    jobs = [("M2", k, s) for k in range(5) for s in range(3)] + [("M1", k, -1) for k in range(5)]
    with Pool(min(os.cpu_count() - 2, 14)) as p: res = p.map(job, jobs, chunksize=1)
    df = pd.DataFrame(res); df.to_csv("results/c2_train_log.csv", index=False); print(df)
