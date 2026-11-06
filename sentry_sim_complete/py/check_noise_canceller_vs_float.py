"""Compare the RTL NLMS output with a floating-point NLMS on the same data.
Run after the Vivado/iverilog NLMS test:  python py/check_noise_canceller_vs_float.py results/noise_canceller_output.csv"""
import sys, numpy as np
a = np.genfromtxt(sys.argv[1] if len(sys.argv) > 1 else "results/noise_canceller_output.csv", delimiter=",", names=True)
clean, noisy, ref, rtl = a["clean"], a["noisy"], a["ref"], a["rtl"]
# same scaling as the testbench: data were halved before conversion to Q1.15
n = len(clean); taps = 16; mu = 0.25
w = np.zeros(taps); x = np.zeros(taps); out = np.zeros(n)
for i in range(n):
    x = np.roll(x, 1); x[0] = ref[i]
    y = w @ x
    e = noisy[i] - y
    w += mu * e * x / (x @ x + 1e-9)
    out[i] = e
h = slice(n // 2, n)
def snr(est): return 10 * np.log10(np.sum(clean[h]**2) / np.sum((est[h] - clean[h])**2))
before = 10 * np.log10(np.sum(clean[h]**2) / np.sum((noisy[h] - clean[h])**2))
print(f"SNR before            : {before:6.2f} dB")
print(f"SNR float NLMS (exact): {snr(out):6.2f} dB")
print(f"SNR RTL (fixed point) : {snr(rtl):6.2f} dB")
print(f"RMS gap RTL vs float  : {np.sqrt(np.mean((rtl[h]-out[h])**2)):.4f}  (signal RMS {np.sqrt(np.mean(clean[h]**2)):.4f})")
