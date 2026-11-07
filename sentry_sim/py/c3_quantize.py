"""C3: post-training INT8 of beatnet-tiny per outer fold (seed 0 model).  Replayed (integer model on public recordings).
   python py/c3_quantize.py            -> results/c3_*.csv, configs/c3_quant_frozen.json (fold 0 model), data/edge/quant/f<k>_<variant>.npz, rtl_edge/weights/*.mem (written by c4_write_weights.py)
Variants: 'first' = per-tensor weight scales (the planned scheme); 'perch' = per-output-channel conv weight scales (fallback a); 'qat' = fine-tune with STE (fallback b)."""
import os, sys, json, pickle, math
import numpy as np, pandas as pd, torch
sys.path.insert(0, os.path.dirname(__file__))
import edge_nets as E, edge_int_model as IM

META = json.load(open("data/edge/edb_meta.json")); import c1_lib as C; RECS = C.records()
LAYERS = ["conv1", "conv2", "conv3"]


def m0n(M):
    """M ~= M0 * 2^-n with M0 int in [2^30, 2^31)."""
    if M <= 0: return 0, 31
    m, e = math.frexp(M)                                           # M = m*2^e, m in [0.5,1)
    M0 = int(round(m * 2 ** 31)); n = 31 - e
    if M0 == 2 ** 31: M0 //= 2; n -= 1
    return M0, n


def float_acts(net, win):
    x = E.to_input(win).unsqueeze(1); outs = []
    import torch.nn.functional as F
    with torch.no_grad():
        x = F.relu(net.c1(F.pad(x, (3, 3)))); outs.append(x.numpy())
        x = F.relu(net.c2(F.pad(x, (2, 2)))); outs.append(x.numpy())
        x = F.relu(net.c3(F.pad(x, (0, 1)))); outs.append(x.numpy())
    return outs


def quantize(state, calib_win, per_channel=False):
    net = E.BeatNet(); net.load_state_dict({k: torch.tensor(v, dtype=torch.float32) for k, v in state.items()}); net.eval()
    acts = float_acts(net, calib_win); P = {}; s_in = E.IN_SCALE; meta = {}
    W = {"conv1": (state["c1.weight"], state["c1.bias"]), "conv2": (state["c2.weight"], state["c2.bias"]), "conv3": (state["c3.weight"], state["c3.bias"])}
    for name, a in zip(LAYERS, acts):
        w, b = W[name]
        sw = (np.abs(w).reshape(w.shape[0], -1).max(1) / 127.0) if per_channel else np.full(w.shape[0], np.abs(w).max() / 127.0)
        wq = np.clip(np.round(w / sw[:, None, None]), -127, 127).astype(np.int64)
        s_out = float(np.percentile(a, 99.9)) / 127.0
        bq = np.round(b / (s_in * sw)).astype(np.int64)
        M0, n = zip(*[m0n(s_in * s / s_out) for s in sw])
        P[f"{name}_w"], P[f"{name}_b"], P[f"{name}_M0"], P[f"{name}_n"] = wq, bq, np.array(M0, dtype=np.int64), np.array(n, dtype=np.int64)
        meta[name] = dict(s_in=s_in, s_w=[float(v) for v in sw], s_out=s_out); s_in = s_out
    wf, bf = state["fc.weight"], state["fc.bias"]; swf = np.abs(wf).max() / 127.0; sf = s_in * swf / 19.0
    P["fc_w"] = np.clip(np.round(wf / swf), -127, 127).astype(np.int64); P["fc_b"] = np.round(bf / sf).astype(np.int64)
    meta["fc"] = dict(s_w=float(swf), logit_scale=float(sf)); P["_meta"] = meta
    return P


def int_scores(win, P, chunk=4096):
    return np.concatenate([IM.forward_int_batch(win[i:i + chunk], P) for i in range(0, len(win), chunk)])


def episode_counts(S, scores, thr, win=30, need=24):
    import edge_nets as E
    caught = n = 0; false = 0
    for ri in np.unique(S["rec"]):
        rec = RECS[ri]; mt = META[rec]; sel = (S["rec"] == ri) & S["ok"]; t = S["t"][sel]; al = E.alerts(t, scores[sel] > thr, win, need)
        for s, e, g in mt["st"]: n += 1; caught += int(((al >= s) & (al <= e)).any())
    return caught, n


def evaluate_fold(k, state, thr_f, variant, per_channel, qat_P=None):
    import pickle
    rng = np.random.default_rng(100 + k)
    val = (k + 1) % 5; trf = [f for f in range(5) if f not in (k, val)]
    dtr = [E.load_fold(f) for f in trf]; wtr = np.concatenate([d["win"][d["scored"] & (d["label"] >= 0)] for d in dtr])
    calib = wtr[rng.choice(len(wtr), 4000, replace=False)]
    P = qat_P if qat_P is not None else quantize(state, calib, per_channel)
    dv, dt = E.load_fold(val), E.load_fold(k); Sv = np.load(f"data/edge/c2_scores_fold{val}.npz"); St = dict(np.load(f"data/edge/c2_scores_fold{k}.npz"))
    mv = dv["ok"] & (dv["label"] >= 0); mt_ = dt["ok"] & (dt["label"] >= 0)
    iv = int_scores(dv["win"][mv], P); fv = Sv["M2_s0"][mv]; frac = float((fv > thr_f).mean()); thr_i = float(np.quantile(iv, 1 - frac))
    ia = int_scores(dt["win"], P); fa = St["M2_s0"]                 # all eligible test beats (for persistence)
    y = (dt["label"][mt_] == 1).astype(int); si, sf = ia[mt_], fa[mt_]
    agree = float(((si > thr_i) == (sf > thr_f)).mean())
    cf, nep = episode_counts(St, fa, thr_f); ci, _ = episode_counts(St, ia, thr_i)
    thr_i2 = E.thr_at_fpr(iv[(dv["label"][mv] == 0)]); ci2, _ = episode_counts(St, ia, thr_i2)         # diagnostic only: integer model's OWN 1% FPR threshold on validation negatives
    row = dict(fold=k, variant=variant, test_beats=len(y), AUPRC_float=E.auprc(y, sf), AUPRC_int=E.auprc(y, si), AUROC_float=E.auroc(y, sf), AUROC_int=E.auroc(y, si),
               sens1pct_float=E.sens_at_fpr(sf[y == 1], sf[y == 0])[0], sens1pct_int=E.sens_at_fpr(si[y == 1], si[y == 0])[0],
               deployed_pos_frac_val=frac, decision_agreement=agree, episodes=nep, episodes_caught_float=cf, episodes_caught_int=ci, episode_sens_float=cf / nep, episode_sens_int=ci / nep,
               episode_sens_drop_pp=100 * (cf - ci) / nep, diag_own_thr_deployed_sens=float((si[y == 1] > thr_i2).mean()), diag_own_thr_deployed_FPR=float((si[y == 0] > thr_i2).mean()),
               diag_float_deployed_sens=float((sf[y == 1] > thr_f).mean()), diag_float_deployed_FPR=float((sf[y == 0] > thr_f).mean()), diag_own_thr_episodes_caught=ci2, max_abs_acc=max(P["_maxacc"].values()) if "_maxacc" in P else np.nan)
    return row, P, (sf, si, y)


def qat_state(k, state, epochs=3, lr=1e-4):
    """Fallback b: fine-tune with fake quantisation (STE), activation scales fixed from the float model's training-patient calibration."""
    import torch.nn.functional as F
    torch.set_num_threads(8); val = (k + 1) % 5; trf = [f for f in range(5) if f not in (k, val)]
    dtr = [E.load_fold(f) for f in trf]; m = lambda d: d["scored"] & (d["label"] >= 0)
    win = np.concatenate([d["win"][m(d)] for d in dtr]); lab = np.concatenate([d["label"][m(d)] for d in dtr]); dv = E.load_fold(val); wv = dv["win"][m(dv)]; lv = dv["label"][m(dv)]
    rng = np.random.default_rng(100 + k); calib = win[rng.choice(len(win), 4000, replace=False)]
    net = E.BeatNet(); net.load_state_dict({n: torch.tensor(v, dtype=torch.float32) for n, v in state.items()}); acts = float_acts(net, calib)
    so = [float(np.percentile(a, 99.9)) / 127.0 for a in acts]
    def fqw(w): sc = w.detach().abs().max() / 127.0; q = torch.clamp(torch.round(w / sc), -127, 127) * sc; return w + (q - w).detach()
    def fqa(x, sc): q = torch.clamp(torch.round(x / sc), 0, 127) * sc; return x + (q - x).detach()
    def fwd(x):
        x = x.unsqueeze(1)
        x = fqa(F.relu(F.conv1d(F.pad(x, (3, 3)), fqw(net.c1.weight), net.c1.bias)), so[0])
        x = fqa(F.relu(F.conv1d(F.pad(x, (2, 2)), fqw(net.c2.weight), net.c2.bias, stride=2)), so[1])
        x = fqa(F.relu(F.conv1d(F.pad(x, (0, 1)), fqw(net.c3.weight), net.c3.bias, stride=2)), so[2])
        return F.linear(x.mean(2), fqw(net.fc.weight), net.fc.bias)
    opt = torch.optim.Adam(net.parameters(), lr=lr, weight_decay=1e-4); pos = np.where(lab == 1)[0]; neg = np.where(lab == 0)[0]; best = (-1, None)
    for ep in range(epochs):
        idx = np.concatenate([pos, rng.choice(neg, len(pos), replace=len(neg) < len(pos))]); rng.shuffle(idx)
        for i in range(0, len(idx), 256):
            b = idx[i:i + 256]; o = fwd(E.to_input(win[b])); loss = F.cross_entropy(o, torch.from_numpy(lab[b].astype(np.int64))); opt.zero_grad(); loss.backward(); opt.step()
        with torch.no_grad(): o = torch.cat([fwd(E.to_input(wv[i:i + 8192])) for i in range(0, len(wv), 8192)]); ap = E.auprc(lv, (o[:, 1] - o[:, 0]).numpy())
        if ap > best[0]: best = (ap, {n: v.detach().numpy().astype(np.float64).copy() for n, v in net.state_dict().items()})
    return best[1]


if __name__ == "__main__":
    import torch
    os.makedirs("data/edge/quant", exist_ok=True); rows = []; scat = None
    for k in range(5):
        ck = torch.load(f"data/edge/models/m2_f{k}_s0.pt"); state = {n: v.numpy().astype(np.float64) for n, v in ck["state"].items()}; thr_f = ck["thr"]
        qs = qat_state(k, state)
        for variant, pc, st_ in (("first (per-tensor)", False, state), ("fallback a (per-channel)", True, state), ("fallback b (QAT, per-tensor)", False, qs)):
            row, P, sc = evaluate_fold(k, st_, thr_f, variant, pc); rows.append(row)
            pickle.dump(P, open(f"data/edge/quant/f{k}_{variant[:10].replace(' ', '_')}.pkl", "wb"))
            if k == 0 and variant.startswith('first'): scat = sc
            print(k, variant, round(row["decision_agreement"], 4), row["episodes_caught_float"], row["episodes_caught_int"], round(row["AUROC_float"], 3), round(row["AUROC_int"], 3))
    df = pd.DataFrame(rows); df.to_csv("results/c3_int8_vs_float.csv", index=False)
    pickle.dump(scat, open("data/edge/quant/scatter_f0.pkl", "wb"))
