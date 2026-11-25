"""B3/B4 step 2: run each DaLiA person's chest ECG (data/b3/ecg_S<k>.hex) through the UNCHANGED rtl/ecg_beat_detector.sv with
tb/tb_real_ecg_beats.sv (baseline testbench), in its own xsim folder so it can run next to other simulations.
Needs settings64.bat in the same window.   python py/b3_ecg_rtl.py 1 2 ... 15
Writes data/b3/det_S<k>.txt: one line per detected beat = (sample index at 250 Hz, heart rate bpm*16).
Note: the testbench's reported index can lag the true sample by a few samples (timing race); irrelevant at the 1 s resolution used here."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import real_lib as L

subs = [int(x) for x in sys.argv[1:]]
sim = L.Sim("xsim", work="xsim_work_b3")
sim.build(["rtl/ecg_beat_detector.sv", "tb/tb_real_ecg_beats.sv"], "tb_real_ecg_beats", "b3_ecg")
for s in subs:
    n = sum(1 for _ in open(f"data/b3/ecg_S{s}.hex"))
    out = sim.run("b3_ecg", [f"ECGFILE=../data/b3/ecg_S{s}.hex", f"NSAMP={n}", f"OUT=../data/b3/det_S{s}.txt"])
    if "replay done" not in out: sys.exit(f"simulator did not finish for S{s}:\n{out[-600:]}")
    print(f"S{s}: {out.strip().splitlines()[-3] if out.strip() else ''}", flush=True)
