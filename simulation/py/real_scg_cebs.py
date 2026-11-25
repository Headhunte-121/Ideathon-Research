"""CEBS (PhysioNet) real seismocardiogram check: how strong is the chest heartbeat vibration in 20 real subjects,
measured the way the Pod measures it (250 Hz, per-second mean |acceleration| in LSM6DSOX codes of 122 ug/LSB)?
The Pod's "chest is still" test says the heart has stopped when this number is BELOW a threshold (SCG_THR = 5 in the sims).
If real living subjects sit near that threshold, an arrest cannot be told from a healthy resting person.

  python py/real_scg_cebs.py --dir real_data/cebs --records b001 b002 ... b020 --mv-per-g 660
--mv-per-g : sensor sensitivity incl. gain, in the units of the CEBS channel (check info.txt, the record header and the
             LIS344ALH datasheet; a wrong value scales every result). It is NOT guessed here.
Output: results/real_scg_cebs.csv and a printed summary."""
import argparse, csv, os, sys
import numpy as np, pandas as pd, wfdb
from scipy.signal import resample_poly, butter, sosfiltfilt

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True); ap.add_argument("--records", nargs="+", required=True)
ap.add_argument("--mv-per-g", type=float, required=True)
ap.add_argument("--minutes", type=float, default=5.0, help="use at most this many minutes per record")
ap.add_argument("--thr", type=float, nargs="+", default=[5, 8, 12], help="'still' thresholds in codes to test")
ap.add_argument("--out", default="real_scg_cebs", help="output name under results/ (no extension)")
a = ap.parse_args()
UG_PER_CODE = 122.0
rows = []; SEC = []
for rec in a.records:
    path = os.path.join(a.dir, rec)
    h = wfdb.rdheader(path); fs = h.fs
    names = [n.lower() for n in h.sig_name]
    ch = next((i for i, n in enumerate(names) if "scg" in n or "acc" in n), len(names) - 1)
    n1 = int(min(h.sig_len, a.minutes * 60 * fs))
    r = wfdb.rdrecord(path, sampfrom=0, sampto=n1, channels=[ch])
    x = r.p_signal[:, 0]
    g = x / a.mv_per_g * (1.0 if (r.units[0] or "").lower() == "mv" else 1.0)
    q = int(round(fs / 250.0)); y = resample_poly(g, 1, q) if q > 1 else g
    sos = butter(2, 1.0, "highpass", fs=250.0, output="sos"); y = sosfiltfilt(sos, y)
    codes = np.abs(y) * 1e6 / UG_PER_CODE
    nsec = len(codes) // 250
    en = codes[: nsec * 250].reshape(nsec, 250).mean(axis=1)
    SEC.append(pd.DataFrame(dict(record=rec, second=np.arange(nsec), energy_codes=en)))
    row = dict(record=rec, seconds=nsec, median=float(np.median(en)), p5=float(np.percentile(en, 5)),
               p1=float(np.percentile(en, 1)), minimum=float(en.min()))
    for t in a.thr:
        row[f"pct_below_{t:g}"] = round(100.0 * float((en < t).mean()), 2)
    rows.append(row)
    print(f"{rec}: median {row['median']:.1f}  p5 {row['p5']:.1f}  p1 {row['p1']:.1f} codes;  " +
          "  ".join(f"<{t:g}: {row[f'pct_below_{t:g}']}%" for t in a.thr))
os.makedirs("results", exist_ok=True)
pd.concat(SEC).to_csv(f"results/{a.out}_seconds.csv", index=False)      # per-second energies (for the histogram)
with open(f"results/{a.out}.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
med = np.array([r["median"] for r in rows])
print(f"\nacross {len(rows)} records: median-of-medians {np.median(med):.1f} codes, weakest subject {med.min():.1f} codes")
for t in a.thr:
    print(f"threshold {t:g}: seconds of a LIVING resting person that look 'still' -> mean {np.mean([r[f'pct_below_{t:g}'] for r in rows]):.2f}%, worst subject {max(r[f'pct_below_{t:g}'] for r in rows):.2f}%")
