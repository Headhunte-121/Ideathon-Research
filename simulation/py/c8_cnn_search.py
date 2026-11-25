"""C8 GPU CNN random search.  python py/c8_cnn_search.py <n_configs> [start_id]   Appends to results/c8_cnn_log.csv.  Uses the CUDA torch in .torch_cuda."""
import os, sys, json, time, csv
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".torch_cuda"))   # optional local CUDA build of PyTorch
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
sys.path.insert(0, os.path.dirname(__file__))
import c8_search as S8
from sklearn.metrics import roc_auc_score, average_precision_score
DEV = torch.device("cuda"); MM = S8.MM
ARCH = [[4, 8, 8], [8, 16, 16], [16, 32, 32], [8, 16, 32], [16, 16]]; KERN = [[7, 5, 3], [5, 5, 3], [9, 5, 3], [7, 3, 3]]; STR = [[1, 2, 2], [2, 2, 2], [1, 1, 2]]


def sample(i):
    r = np.random.default_rng(9000 + i); ch = ARCH[int(r.integers(len(ARCH)))]; n = len(ch)
    return dict(id=i, inp=str(r.choice(["W", "WR300", "WR600", "WR1800", "W+WR600"])), ch=ch, k=KERN[int(r.integers(len(KERN)))][:n], s=STR[int(r.integers(len(STR)))][:n], lr=float(r.choice([3e-4, 1e-3, 3e-3])),
                wd=float(r.choice([0, 1e-4, 1e-3])), drop=float(r.choice([0, .2])), batch=int(r.choice([512, 2048])), per_class=int(r.choice([20000, 60000])), aug=str(r.choice(["none", "amp+shift"])), smooth=int(r.choice([1, 5, 15, 30])))


class Net(nn.Module):
    def __init__(self, c):
        super().__init__(); cin = 2 if c["inp"] == "W+WR600" else 1; self.convs = nn.ModuleList(); self.pads = []
        L = 75
        for co, k, s in zip(c["ch"], c["k"], c["s"]):
            out = -(-L // s); tot = max((out - 1) * s + k - L, 0); self.pads.append((tot // 2, tot - tot // 2)); self.convs.append(nn.Conv1d(cin, co, k, stride=s)); cin = co; L = out
        self.drop = nn.Dropout(c["drop"]); self.fc = nn.Linear(cin, 2)

    def forward(self, x):
        for cv, p in zip(self.convs, self.pads): x = F.relu(cv(F.pad(x, p)))
        return self.fc(self.drop(x.mean(2)))


_D = {}
def data(k, key):
    if (k, key) not in _D: _D[(k, key)] = torch.from_numpy(np.load(f"{MM}/{k}_{key}.npy")).to(DEV)
    return _D[(k, key)]


_IN = {}
def inputs(k, c, idx=None):
    key = (k, c["inp"])
    if key not in _IN:
        _IN[key] = _inputs(k, c).half(); _D.pop((k, "win"), None); [_D.pop((k, f"wmed{x}"), None) for x in (300, 600, 1800)]
    return _IN[key] if idx is None else _IN[key][idx]


def _inputs(k, c, idx=None):
    w = data(k, "win").float() / 16.0; i = c["inp"]
    if i == "W": x = w[:, None, :]
    elif i.startswith("WR") and "+" not in i: x = ((w * 16 - torch.nan_to_num(data(k, f"wmed{i[2:]}").float())) / 16.0)[:, None, :]
    else: x = torch.stack([w, (w * 16 - torch.nan_to_num(data(k, "wmed600").float())) / 16.0], 1)
    return x if idx is None else x[idx]


def smooth_t(score, start, n):
    if n <= 1: return score
    cs = torch.cat([torch.zeros(1, device=DEV, dtype=torch.float64), torch.cumsum(score.double(), 0)]); i = torch.arange(len(score), device=DEV); lo = torch.maximum(i - n + 1, start)
    return ((cs[i + 1] - cs[lo]) / (i + 1 - lo)).float()


@torch.no_grad()
def predict(net, x):
    net.eval(); return torch.cat([(lambda o: o[:, 1] - o[:, 0])(net(x[i:i + 16384].float())) for i in range(0, len(x), 16384)])


def gpu_auc(k, s):
    ok = data(k, "ok").bool(); lab = data(k, "label"); m = ok & (lab >= 0); y = (lab[m] == 1); sc = s[m]; r = torch.empty(len(sc), device=DEV); o = torch.argsort(sc); r[o] = torch.arange(1, len(sc) + 1, device=DEV, dtype=torch.float32)
    npos = y.sum().item(); nneg = len(y) - npos; return ((r[y].sum().item() - npos * (npos + 1) / 2) / (npos * nneg))


def metrics(k, s, thr=None):
    ok = data(k, "ok").bool(); lab = data(k, "label"); m = ok & (lab >= 0); yy = (lab[m] == 1).cpu().numpy().astype(int); ss = s[m].cpu().numpy(); t_own = np.quantile(ss[yy == 0], .99)
    r = dict(auroc=roc_auc_score(yy, ss), auprc=average_precision_score(yy, ss), sens1=float((ss[yy == 1] > t_own).mean()), thr=t_own)
    if thr is not None: r.update(dep_sens=float((ss[yy == 1] > thr).mean()), dep_fpr=float((ss[yy == 0] > thr).mean()))
    return r


def job(c, k):
    t0 = time.time(); val = (k + 1) % 5; trf = [f for f in range(5) if f not in (k, val)]; seed = 9000 + c["id"] + 100 * k; torch.manual_seed(seed); g = np.random.default_rng(seed)
    X = torch.cat([inputs(f, c) for f in trf]); lab = torch.cat([data(f, "label") for f in trf]); ok = torch.cat([data(f, "ok") for f in trf]).bool(); m = ok & (lab >= 0)
    pos = torch.where(m & (lab == 1))[0]; neg = torch.where(m & (lab == 0))[0]; net = Net(c).to(DEV); opt = torch.optim.Adam(net.parameters(), lr=c["lr"], weight_decay=c["wd"])
    Xv, Xt = inputs(val, c), inputs(k, c); sv_start, st_start = data(val, "start"), data(k, "start"); best = (-1, None)
    for ep in range(12):
        net.train(); n = min(c["per_class"], len(pos), len(neg)); idx = torch.cat([pos[torch.randperm(len(pos), device=DEV)[:n]], neg[torch.randperm(len(neg), device=DEV)[:n]]]); idx = idx[torch.randperm(len(idx), device=DEV)]
        for i in range(0, len(idx), c["batch"]):
            b = idx[i:i + c["batch"]]; x = X[b].float(); y = (lab[b] == 1).long()
            if c["aug"] == "amp+shift":
                x = x * (0.8 + 0.4 * torch.rand(len(b), 1, 1, device=DEV)); sh = int(torch.randint(-2, 3, (1,))); x = torch.roll(x, sh, dims=2)
            loss = F.cross_entropy(net(x), y); opt.zero_grad(); loss.backward(); opt.step()
        sv = smooth_t(predict(net, Xv), sv_start, c["smooth"]); a = gpu_auc(val, sv)
        if a > best[0]: best = (a, {n_: v.clone() for n_, v in net.state_dict().items()})
    net.load_state_dict(best[1]); sv = smooth_t(predict(net, Xv), sv_start, c["smooth"]); mv = metrics(val, sv); st = smooth_t(predict(net, Xt), st_start, c["smooth"]); mt = metrics(k, st, mv["thr"])
    return dict(cfg=c["id"], fold=k, val_auroc=mv["auroc"], val_auprc=mv["auprc"], val_sens1=mv["sens1"], test_auroc=mt["auroc"], test_auprc=mt["auprc"], test_sens1=mt["sens1"], test_dep_sens=mt["dep_sens"], test_dep_fpr=mt["dep_fpr"], sec=time.time() - t0), st.cpu().numpy()


if __name__ == "__main__":
    S8.make_cache()
    if sys.argv[1].endswith(".json"):
        cfgs = [sample(i) for i in json.load(open(sys.argv[1]))]; s0, step = 0, 1
    else:
        n = int(sys.argv[1]); s0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0; step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        cfgs = [sample(i) for i in range(n)]; json.dump(cfgs, open("results/c8_cnn_configs.json", "w"))
    for f in range(5): data(f, "start")
    fields = ["cfg", "fold", "val_auroc", "val_auprc", "val_sens1", "test_auroc", "test_auprc", "test_sens1", "test_dep_sens", "test_dep_fpr", "sec"]
    path = "results/c8_cnn_log%s.csv" % (sys.argv[4] if len(sys.argv) > 4 else ""); new = not os.path.exists(path)
    with open(path, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        if new: w.writeheader()
        for c in cfgs[s0::step]:
            for k in range(5):
                o, _ = job(c, k); w.writerow({a: o[a] for a in fields}); fh.flush()
            print("cfg", c["id"], "done", flush=True)
