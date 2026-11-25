"""Batch real-data experiments on the Verilog beat detector and drift detector.

  python py/real_batch.py ecg   --dir real_data/nstdb --records 118e24 118e18 118e12 118e06 118e00 118e_6 119e24 119e18 119e12 119e06 119e00 119e_6 --noisy
  python py/real_batch.py ecg   --dir real_data/nsrdb --records 16265 16272 ... --start-min 60 --minutes 30
  python py/real_batch.py drift --dir real_data/nsrdb --records 16265 16272 ...        (or --records all)
Options: --sim xsim (default, needs settings64.bat run) | iverilog.   Output: results/real_<mode>_<tag>.csv
"""
import argparse, csv, glob, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import real_lib as L

ap = argparse.ArgumentParser()
ap.add_argument("mode", choices=["ecg", "drift"])
ap.add_argument("--dir", required=True)
ap.add_argument("--records", nargs="+", required=True)
ap.add_argument("--start-min", type=float, default=0.0)
ap.add_argument("--minutes", type=float, default=None)
ap.add_argument("--noisy", action="store_true", help="NSTDB layout: score clean and noisy segments separately")
ap.add_argument("--sim", default="xsim", choices=["xsim", "iverilog"])
ap.add_argument("--tag", default=None)
ap.add_argument("--inject", type=int, nargs="*", default=[], help="drift mode: also inject +N%% heart-rate steps and report detection delay")
a = ap.parse_args()
recs = a.records
if recs == ["all"]:
    recs = sorted(os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(a.dir, "*.hea")))
tag = a.tag or os.path.basename(os.path.normpath(a.dir))
os.makedirs("results", exist_ok=True); os.makedirs("data", exist_ok=True)
sim = L.Sim(a.sim)
rows = []; inj_rows = []

if a.mode == "ecg":
    sim.build(["rtl/ecg_beat_detector.sv", "tb/tb_real_ecg_beats.sv"], "tb_real_ecg_beats", "real_ecg")
    for rec in recs:
        ns, nref = L.prepare_ecg(rec, a.dir, "data", a.start_min, a.minutes)
        so = sim.run("real_ecg", [f"ECGFILE=../data/ecg_{rec}.hex" if a.sim == "xsim" else f"ECGFILE=data/ecg_{rec}.hex",
                             f"NSAMP={ns}", f"OUT=../data/det_{rec}.txt" if a.sim == "xsim" else f"OUT=data/det_{rec}.txt"])
        if "replay done" not in so: sys.exit(f"simulator did not finish for {rec}:\n{so[-600:]}")
        sc = L.score_beats(rec, "data", a.noisy)
        for g, v in sc.items():
            rows.append(dict(record=rec, segment=g, ref_beats=nref, **v))
            print(f"{rec:10s} {g:6s} sens {v['sens']:6.2f}%  ppv {v['ppv']:6.2f}%  (tp {v['tp']} miss {v['fn']} false {v['fp']})")
else:
    sim.build(["rtl/baseline_drift_detector.sv", "tb/tb_drift_false_alarms.sv"], "tb_drift_false_alarms", "real_drift")
    for rec in recs:
        nb, hours = L.hr_file(rec, a.dir, "data")
        pre = "../data" if a.sim == "xsim" else "data"
        out = sim.run("real_drift", [f"HRFILE={pre}/hr_{rec}.hex", f"NBEATS={nb}"])
        m = re.search(r"K=3\.0:\s*(\d+)\s+K=3\.8:\s*(\d+)\s+K=4\.5:\s*(\d+)", out)
        h = re.search(r"about\s+([\d.]+)\s+hours", out)
        if not m: print(rec, "no result; simulator said:", out[-300:]); continue
        c30, c38, c45 = map(int, m.groups()); hrs = float(h.group(1)) if h else hours
        r = dict(record=rec, beats=nb, hours=round(hrs, 1), checkins_k30=c30, checkins_k38=c38, checkins_k45=c45,
                 per24h_k30=round(c30 * 24 / hrs, 2), per24h_k38=round(c38 * 24 / hrs, 2), per24h_k45=round(c45 * 24 / hrs, 2))
        rows.append(r); print(r)
        for pct in a.inject:                    # step change of +pct % in heart rate over the last quarter of the recording
            o2 = sim.run("real_drift", [f"HRFILE={pre}/hr_{rec}.hex", f"NBEATS={nb}", "INJECT=1", f"PCT={pct}"])
            m2 = re.search(r"first flag: K=3\.0:\s*(-?\d+)\s+K=3\.8:\s*(-?\d+)\s+K=4\.5:\s*(-?\d+)", o2)
            if not m2: print(rec, pct, "no injection result:", o2[-200:]); continue
            min_per_beat = hours * 60.0 / nb
            d = [int(v) for v in m2.groups()]
            inj_rows.append(dict(record=rec, shift_pct=pct, **{f"delay_min_k{k}": (round(v * min_per_beat, 1) if v >= 0 else "missed")
                                                                for k, v in zip(("30", "38", "45"), d)}))
            print("  inject +%d%%: delay (min) K3.0 %s  K3.8 %s  K4.5 %s" % (pct, *[x if x == "missed" else x for x in
                  [inj_rows[-1][f"delay_min_k{k}"] for k in ("30", "38", "45")]]))

if a.mode == "ecg":
    c = L.CLIP_STATS; print(f"ECG samples clipped at the 16-bit rail: {c['clipped']} of {c['samples']} ({100*c['clipped']/max(c['samples'],1):.3f}%)")
if rows:
    path = f"results/real_{a.mode}_{tag}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("saved", path)
if inj_rows:
    path = f"results/real_drift_injection_{tag}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(inj_rows[0].keys())); w.writeheader(); w.writerows(inj_rows)
    print("saved", path)
