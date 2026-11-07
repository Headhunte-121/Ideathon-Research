"""C2 test stage: score each outer-test fold ONCE with the frozen models.  -> data/edge/c2_scores_fold<k>.npz"""
import os, sys, json, pickle
import numpy as np, torch
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E
torch.set_num_threads(4)
if __name__ == "__main__":
    for k in range(5):
        d = E.load_fold(k); out = dict(t=d["t"], label=d["label"], ep=d["ep"], rec=d["rec"], subject=d["subject"], ok=d["ok"], stlev=d["stlev"], feat=d["feat"])
        out["R0"] = np.abs(d["stlev"]); out["R1"] = np.nan_to_num(d["r1"], nan=-1.0)
        m1 = pickle.load(open(f"data/edge/models/m1_f{k}.pkl", "rb")); out["M1"] = m1["model"].decision_function(d["feat"])
        x = E.to_input(d["win"])
        for s in range(3):
            ck = torch.load(f"data/edge/models/m2_f{k}_s{s}.pt"); net = E.BeatNet(); net.load_state_dict(ck["state"]); net.eval()
            with torch.no_grad(): out[f"M2_s{s}"] = torch.cat([net.score(x[i:i + 8192]) for i in range(0, len(x), 8192)]).numpy()
        np.savez_compressed(f"data/edge/c2_scores_fold{k}.npz", **out); print(k, len(d["t"]))
