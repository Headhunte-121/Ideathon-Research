"""C7 train: A3 = beatnet-tiny retrained on per-person residual windows (window - running median of previous 10 min).  Same recipe as c2_frozen.  No outer-test scoring here."""
import os, sys, json, time
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
CFG = json.load(open("configs/c2_frozen.json"))


def gather(folds):
    import edge_nets as E
    out = {"win": [], "label": []}
    for k in folds:
        d = E.load_fold(k); r = np.load(f"data/edge/edb_resid_{k}.npz"); m = d["scored"] & (d["label"] >= 0) & r["hist_ok"]
        out["win"].append(r["resid"][m]); out["label"].append(d["label"][m])
    return {k: np.concatenate(v) for k, v in out.items()}


def job(a):
    k, seed = a
    import torch, edge_nets as E
    torch.set_num_threads(1); val = (k + 1) % 5; trf = [f for f in range(5) if f not in (k, val)]
    tr, va = gather(trf), gather([val]); t0 = time.time(); rs = 1000 * k + seed + 500; rng = np.random.default_rng(rs); torch.manual_seed(rs)
    net = E.BeatNet(); opt = torch.optim.Adam(net.parameters(), lr=CFG["optimiser"]["lr"], weight_decay=CFG["optimiser"]["weight_decay"])
    pos = np.where(tr["label"] == 1)[0]; neg = np.where(tr["label"] == 0)[0]; xv = E.to_input(va["win"]); best = (-1, None, 0, None); bad = 0
    for ep in range(CFG["optimiser"]["max_epochs"]):
        net.train(); idx = np.concatenate([pos, rng.choice(neg, size=len(pos), replace=len(neg) < len(pos))]); rng.shuffle(idx)
        for i in range(0, len(idx), CFG["optimiser"]["batch"]):
            b = idx[i:i + CFG["optimiser"]["batch"]]
            loss = torch.nn.functional.cross_entropy(net(E.to_input(tr["win"][b])), torch.from_numpy(tr["label"][b].astype(np.int64))); opt.zero_grad(); loss.backward(); opt.step()
        net.eval()
        with torch.no_grad(): sv = torch.cat([net.score(xv[i:i + 8192]) for i in range(0, len(xv), 8192)]).numpy()
        ap = E.auprc(va["label"], sv)
        if ap > best[0]: best = (ap, {n: v.clone() for n, v in net.state_dict().items()}, ep, sv.copy()); bad = 0
        else:
            bad += 1
            if bad >= CFG["early_stopping"]["patience"]: break
    torch.save(dict(state=best[1], epoch=best[2]), f"data/edge/models/a3_f{k}_s{seed}.pt")
    return dict(fold=k, seed=seed, val_auprc=best[0], best_epoch=best[2], sec=time.time() - t0)


if __name__ == "__main__":
    from multiprocessing import Pool
    with Pool(min(os.cpu_count() - 2, 14)) as p: res = p.map(job, [(k, s) for k in range(5) for s in range(3)], chunksize=1)
    df = pd.DataFrame(res); df.to_csv("results/c7_train_log.csv", index=False); print(df)
