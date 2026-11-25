"""C4: run the Verilog copy on 2,064 vectors as parallel xsim chunks (own work folder each), merge, mutation checks.  Simulated.   python py/c4_run.py"""
import os, sys, shutil, re, time
os.environ["PATH"] = r"C:\AMDDesignTools\2025.2\Vivado\bin;" + os.environ["PATH"]
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd, real_lib as L
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.abspath(".").replace("\\", "/"); NV = 2064; NCH = 12
RTL = "rtl_edge/rtl/edge_cnn_beat.sv"; TB = "rtl_edge/tb/tb_edge_cnn.sv"


def chunk(args):
    tag, rtl, start, count = args
    work = f"xsim_work_c4_{tag}"; sim = L.Sim("xsim", work=work); sim.build([rtl, TB], "tb_edge_cnn", "snap")
    out = f"{ROOT}/{work}/out.txt"
    log = sim.run("snap", [f"VEC_START={start}", f"VEC_COUNT={count}", f"OUT={out}", f"VEC_IN={ROOT}/rtl_edge/tb/vectors_in.mem", f"VEC_EXP={ROOT}/rtl_edge/tb/vectors_expected.txt"])
    return tag, log, open(out).read() if os.path.exists(out) else ""


def run(tag, rtl, n_vec, nch):
    per = -(-n_vec // nch); jobs = [(f"{tag}{i}", rtl, i * per, min(per, n_vec - i * per)) for i in range(nch) if i * per < n_vec]
    with ThreadPoolExecutor(nch) as ex: res = list(ex.map(chunk, jobs))
    return res


def summarize(res):
    rows = [list(map(int, l.split())) for _, _, o in res for l in o.strip().splitlines()]
    df = pd.DataFrame(rows, columns=["vector", "expected", "got", "match", "compute_cycles"]); return df.sort_values("vector").reset_index(drop=True)


if __name__ == "__main__":
    t0 = time.time(); res = run("m", RTL, NV, NCH); df = summarize(res)
    df["kind"] = ["real test beat"] * 2000 + ["synthetic extreme"] * 64; df.to_csv("results/c4_rtl_vs_python.csv", index=False)
    with open("results/c4_rtl_log.txt", "w") as f:
        f.write(f"# edge_cnn_beat vs Python integer model, xsim 2025.2, {NCH} parallel chunks, wall {time.time() - t0:.0f} s\n")
        for tag, log, _ in res: f.write(f"\n##### chunk {tag}\n" + "\n".join(l for l in log.splitlines() if re.search(r"MISMATCH|compute_cycles|===|ERROR|FATAL", l)) + "\n")
    print("merged:", len(df), "vectors,", int(df.match.sum()), "match,", int((df.match == 0).sum()), "mismatch;", f"{time.time() - t0:.0f}s")
    cyc = df.compute_cycles; macs = 43144
    pd.DataFrame([dict(vectors=len(df), min=cyc.min(), median=float(cyc.median()), max=cyc.max(), calculated_MACs=macs, overhead_cycles=int(cyc.median()) - macs, overhead_pct=100 * (cyc.median() - macs) / macs,
                       note="compute cycles = clocks after the 75-sample load until done; 1 MAC per cycle (zero-padding taps counted as MAC cycles); overhead = 1 init cycle/output element (1,512) + 304 GAP adds + 2 fc init + 0 other; Simulated")]).to_csv("results/c4_cycles.csv", index=False)
    # mutations (first 120 real vectors each)
    s = open(RTL).read(); os.makedirs("xsim_work_c4_mutsrc", exist_ok=True)
    m1 = s.replace("(64'sd1 <<< (nsh - 1))", "(64'sd1 <<< (nsh - 2))"); assert m1 != s; open("xsim_work_c4_mutsrc/edge_cnn_mut_round.sv", "w").write(m1)
    os.makedirs("xsim_work_c4_mutsrc/weights", exist_ok=True)
    for f in os.listdir("rtl_edge/weights"): shutil.copy(f"rtl_edge/weights/{f}", f"xsim_work_c4_mutsrc/weights/{f}")
    w = open("xsim_work_c4_mutsrc/weights/conv2_w.mem").read().split("\n"); w[100] = "%02x" % ((int(w[100], 16) + 1) & 255); open("xsim_work_c4_mutsrc/weights/conv2_w.mem", "w").write("\n".join(w))
    m2 = s.replace('"../rtl_edge/weights/"', f'"{ROOT}/xsim_work_c4_mutsrc/weights/"'); assert m2 != s; open("xsim_work_c4_mutsrc/edge_cnn_mut_weight.sv", "w").write(m2)
    out = []
    for nm in ("round", "weight"):
        r = run("mut" + nm, f"xsim_work_c4_mutsrc/edge_cnn_mut_{nm}.sv", 120, 4); d = summarize(r)
        out.append(dict(mutation={"round": "rounding constant (1<<(n-1)) -> (1<<(n-2))", "weight": "one conv2 weight +1"}[nm], vectors=len(d), failed=int((d.match == 0).sum()), expected="must fail"))
    pd.DataFrame(out).to_csv("results/c4_mutation_check.csv", index=False); print(pd.DataFrame(out))
