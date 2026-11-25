"""Score the beat detector against the database's own beat annotations.
Usage:  python py/real_data_score.py 16265     (after the tb wrote data/det_16265.txt)
A detected beat counts as correct if it is within 150 ms of a reference beat (each reference used once).
Note: the detector skips the very first beat (it needs two beats to get an interval)."""
import sys, numpy as np
rec = sys.argv[1]
ref = np.loadtxt(f"data/ref_{rec}.txt", dtype=int, ndmin=1)
det = np.loadtxt(f"data/det_{rec}.txt", dtype=int, ndmin=2)
didx, dhr = det[:, 0], det[:, 1] / 16.0
tol = int(0.150 * 250)
used = np.zeros(len(ref), bool); tp = 0; hr_err = []
for k, d in enumerate(didx):
    j = np.searchsorted(ref, d)
    cands = [c for c in (j - 1, j) if 0 <= c < len(ref) and not used[c] and abs(ref[c] - d) <= tol]
    if cands:
        c = min(cands, key=lambda c: abs(ref[c] - d)); used[c] = True; tp += 1
        if c > 0:
            hr_err.append(dhr[k] - 60.0 * 250.0 / (ref[c] - ref[c - 1]))
fp = len(didx) - tp
fn = int((~used).sum()) - 1            # first reference beat cannot be reported
fn = max(fn, 0)
sens = tp / max(tp + fn, 1) * 100; ppv = tp / max(tp + fp, 1) * 100
print(f"reference beats {len(ref)}, detected {len(didx)}")
print(f"true positives {tp}, missed {fn}, false detections {fp}")
print(f"sensitivity {sens:.2f} %   positive predictivity {ppv:.2f} %")
if hr_err:
    e = np.array(hr_err); print(f"heart-rate error per beat: mean {e.mean():.2f} bpm, 95th percentile of |error| {np.percentile(abs(e),95):.2f} bpm")
