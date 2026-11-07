"""beatnet-tiny (Appendix A).  Float (torch) definition + data/metric helpers shared by C2/C3/C5.
Padding convention ('same', TF style, fixed for float, integer numpy and Verilog):
  conv1 k7 s1 L75->75 pad (3,3);  conv2 k5 s2 L75->38 pad (2,2);  conv3 k3 s2 L38->19 pad (0,1).
Float input = int8_window / 16 (fixed input scale 1/16).  Float GAP = mean over 19 positions; integer GAP keeps the SUM (1/19 folded into the fc scale)."""
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

IN_SCALE = 1.0 / 16.0
SPEC = [  # name, cin, cout, k, stride, pad(l,r), Lout
    ("conv1", 1, 8, 7, 1, (3, 3), 75), ("conv2", 8, 16, 5, 2, (2, 2), 38), ("conv3", 16, 16, 3, 2, (0, 1), 19)]


class BeatNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv1d(1, 8, 7); self.c2 = nn.Conv1d(8, 16, 5, stride=2); self.c3 = nn.Conv1d(16, 16, 3, stride=2); self.fc = nn.Linear(16, 2)

    def forward(self, x):                          # x: (B,75) float already scaled
        x = x.unsqueeze(1)
        x = F.relu(self.c1(F.pad(x, (3, 3)))); x = F.relu(self.c2(F.pad(x, (2, 2)))); x = F.relu(self.c3(F.pad(x, (0, 1))))
        return self.fc(x.mean(dim=2))

    def score(self, x):
        o = self.forward(x); return o[:, 1] - o[:, 0]


def to_input(win_int8):
    return torch.from_numpy(win_int8.astype(np.float32) * IN_SCALE)


def state_numpy(net):
    return {k: v.detach().cpu().numpy().astype(np.float64) for k, v in net.state_dict().items()}


# ---------- data ----------
def load_fold(k):
    z = np.load(f"data/edge/edb_windows_{k}.npz"); d = {n: z[n] for n in z.files}
    d["ok"] = d["scored"] & ~np.isnan(d["r1"])                     # scored by every method
    return d


def trainable(d):
    m = d["scored"] & (d["label"] >= 0); return m


# ---------- metrics ----------
def thr_at_fpr(neg_scores, fpr=0.01):
    return float(np.quantile(neg_scores, 1.0 - fpr))


def sens_at_fpr(pos_scores, neg_scores, fpr=0.01):
    t = thr_at_fpr(neg_scores, fpr); return float((pos_scores > t).mean()), t


def auroc(y, s):
    from sklearn.metrics import roc_auc_score
    return float(roc_auc_score(y, s))


def auprc(y, s):
    from sklearn.metrics import average_precision_score
    return float(average_precision_score(y, s))


def alerts(t, above, win=30, need=24):
    """Rising edges of (>= need of the last win eligible beats above threshold). t sorted. Returns alert times."""
    a = above.astype(np.int32); c = np.convolve(a, np.ones(win, dtype=np.int32))[:len(a)]
    c[:win - 1] = 0                                                  # need a full window of beats
    cond = c >= need; edge = cond & ~np.concatenate([[False], cond[:-1]])
    return t[edge]
