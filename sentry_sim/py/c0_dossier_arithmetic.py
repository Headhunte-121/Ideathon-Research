"""C0: arithmetic behind the dossier's Q6.4 'Stage 2' network vs our beatnet-tiny. Calculated, ideal lower bound. -> results/c0_dossier_arithmetic.csv"""
import pandas as pd
def net(layers, fc):
    macs = sum(ci * co * k * L for ci, co, k, L in layers) + fc[0] * fc[1]
    w = sum(ci * co * k for ci, co, k, L in layers) + fc[0] * fc[1]; b = sum(co for _, co, _, _ in layers) + fc[1]
    return macs, w, b
def row(name, macs, w, b, quoted_ms=None, quoted_kb=None):
    cyc = macs / 2; ms = cyc / 128e6 * 1e3
    return dict(network=name, macs=macs, weights=w, biases=b, parameters=w + b, int8_weight_bytes=w, ideal_cycles_2mac=cyc, ideal_ms_128MHz=round(ms, 3),
                dossier_quoted_ms=quoted_ms, dossier_quoted_KB=quoted_kb, label="Calculated, ideal lower bound; real firmware is slower")
# Q6.4: 3->16 k3 L6000, 16->32 k3, 32->32 k3 (stride 1, same length), final 32->2
m, w, b = net([(3, 16, 3, 6000), (16, 32, 3, 6000), (32, 32, 3, 6000)], (32, 2))
rows = [row("dossier Q6.4 stage 2 (60 s x 100 Hz)", m, w, b, "1.8 (230,400 cycles); Q6.1: 0.74", "410")]
# ours: conv1 1->8 k7 L75; conv2 8->16 k5 L38; conv3 16->16 k3 L19; fc 16->2
m2, w2, b2 = net([(1, 8, 7, 75), (8, 16, 5, 38), (16, 16, 3, 19)], (16, 2))
rows.append(row("beatnet-tiny (ours, per heartbeat)", m2, w2, b2))
df = pd.DataFrame(rows); df.to_csv("results/c0_dossier_arithmetic.csv", index=False); print(df.T)
print("ratio MACs", m / m2, " quoted cycles 230400 vs ideal", m / 2 / 230400)
