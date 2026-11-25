"""(Index-by-index comparison; expect mismatches, see py/beat_model.py docstring.)  Check py/beat_model.py against the Verilog detector's own output (data/det_<rec>.txt made by real_batch.py).
    python py/tweak_validate_beat_model.py 16265 16272 118e06 ..."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import beat_model as B

ok = True
for rec in sys.argv[1:]:
    x = np.array([int(l, 16) for l in open(f"data/ecg_{rec}.hex")]); x = np.where(x > 32767, x - 65536, x)
    rtl = np.loadtxt(f"data/det_{rec}.txt", dtype=int, ndmin=2)
    rtl = rtl[:, 0] if rtl.size else np.array([], int)
    py = B.detect(x)
    same = len(rtl) == len(py) and bool(np.all(rtl == py))
    ok &= same
    print(f"{rec}: Verilog {len(rtl)} beats, Python replica {len(py)} beats, identical indices: {same}")
sys.exit(0 if ok else 1)
