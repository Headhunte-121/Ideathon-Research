"""Tweak 4: should the 'chest still' threshold adapt to the chest sensor's own noise floor?   (Python model; the RTL is NOT changed.)
Fixed rule (as built):   chest_still  =  per-second mean|a| < 5 codes (122 ug/LSB)         [SCG_THR = 5]
Adaptive rule (proposal): chest_still  =  per-second mean|a| < max(5, K x floor)           floor = causal 60 s median of the 40-100 Hz
                                          band mean|a| (the heartbeat has no energy there, so it measures the sensor's noise)
Sweep: extra white sensor noise of RMS sigma (ug) is added to the CEBS recordings (living, 40 x 5 min, 660 mV/g assumed) and, for the
'no heartbeat' case, a noise-only signal (SIMULATED: what a still chest with no heartbeat would read, nothing else).
Also: 1 g of gravity (DC) added to the living signal, with and without the 1 Hz high-pass the Pod would need.
    python py/tweak4_adaptive_still.py          Output: results/tweak4_adaptive_still.csv, results/tweak4_gravity.csv"""
import csv
import numpy as np, wfdb
from scipy.signal import resample_poly, butter, sosfiltfilt, sosfilt

UG = 122.0; MVG = 660.0; K = 3.0; THR0 = 5.0
rng = np.random.default_rng(20261106)
HP = butter(2, 1.0, "highpass", fs=250.0, output="sos")
BP = butter(2, [40.0, 100.0], "bandpass", fs=250.0, output="sos")


def sec_energy(y):                                   # mean |y| per second, in codes
    n = len(y) // 250
    return np.abs(y[: n * 250]).reshape(n, 250).mean(axis=1) * 1e6 / UG


def floor_series(hf):                                # causal 60 s rolling median
    return np.array([np.median(hf[max(0, i - 59): i + 1]) for i in range(len(hf))])


def judge(y):
    """y: acceleration in g at 250 Hz (DC allowed).  Returns per-second energy, adaptive threshold."""
    e = sec_energy(sosfiltfilt(HP, y))
    hf = sec_energy(sosfiltfilt(BP, y))
    return e, np.maximum(THR0, K * floor_series(hf))


recs = [f"b{i:03d}" for i in range(1, 21)] + [f"p{i:03d}" for i in range(1, 21)]
sig = {}
for r in recs:
    x = wfdb.rdrecord(f"real_data/cebs/{r}", channels=[3]).p_signal[:, 0] / MVG
    sig[r] = resample_poly(x, 1, 20)

rows = []
for sigma in (0, 150, 350, 500, 650, 800, 1000, 2000):
    a_fix = a_ad = a_n = d_fix = d_ad = d_n = 0
    worst_alive_fixed = worst_alive_ad = 0.0
    for r in recs:
        y = sig[r] + rng.normal(0, sigma * 1e-6, len(sig[r]))
        e, t = judge(y)
        f = 100 * np.mean(e < THR0); ad = 100 * np.mean(e < t)
        a_fix += (e < THR0).sum(); a_ad += (e < t).sum(); a_n += len(e)
        worst_alive_fixed = max(worst_alive_fixed, f); worst_alive_ad = max(worst_alive_ad, ad)
        if sigma > 0:
            z = rng.normal(0, sigma * 1e-6, len(sig[r]))                    # SIMULATED no-heartbeat chest: sensor noise only
            ez, tz = judge(z)
            d_fix += (ez < THR0).sum(); d_ad += (ez < tz).sum(); d_n += len(ez)
    rows.append(dict(sensor_noise_ug_rms=sigma,
                     living_seconds_called_still_fixed_pct=round(100 * a_fix / a_n, 2), living_worst_person_fixed_pct=round(worst_alive_fixed, 2),
                     living_seconds_called_still_adaptive_pct=round(100 * a_ad / a_n, 2), living_worst_person_adaptive_pct=round(worst_alive_ad, 2),
                     no_heartbeat_called_still_fixed_pct=(round(100 * d_fix / d_n, 1) if sigma else ""),
                     no_heartbeat_called_still_adaptive_pct=(round(100 * d_ad / d_n, 1) if sigma else "")))
    print(rows[-1], flush=True)
with open("results/tweak4_adaptive_still.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# gravity: 1 g DC on the living signal; the CEBS channel is AC coupled, the Pod's IMU is not
g = []
for r in recs[:20]:
    y = sig[r] + 1.0
    raw = sec_energy(y)                                         # no high-pass at all
    hp = sec_energy(sosfiltfilt(HP, y))                         # with 1 Hz high-pass
    ref = sec_energy(sosfiltfilt(HP, sig[r]))                   # same person, no gravity
    g.append(dict(record=r, no_filter_median_codes=round(float(np.median(raw)), 0), with_1Hz_highpass_median_codes=round(float(np.median(hp)), 2),
                  without_gravity_median_codes=round(float(np.median(ref)), 2)))
with open("results/tweak4_gravity.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(g[0].keys())); w.writeheader(); w.writerows(g)
print("gravity: median over people  no filter %.0f codes | 1 Hz high-pass %.2f | no gravity %.2f" % (
    np.median([x["no_filter_median_codes"] for x in g]), np.median([x["with_1Hz_highpass_median_codes"] for x in g]),
    np.median([x["without_gravity_median_codes"] for x in g])))
