"""Unattended finisher: keeps Windows awake (per-process SetThreadExecutionState, no system setting changed), waits for the two searches to end (or 6 h), runs the analysis, commits locally.
   python py/c8_finish.py   -> results/c8_finish_log.txt"""
import os, sys, time, subprocess, ctypes, datetime
os.chdir(r"C:\College\Ideathon\sentry_sim")
import psutil
LOG = open("results/c8_finish_log.txt", "a", buffering=1)
def log(m): LOG.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} {m}\n")
ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)          # ES_CONTINUOUS | ES_SYSTEM_REQUIRED while this process lives
def running():
    n = 0
    for p in psutil.process_iter(["cmdline"]):
        c = " ".join(p.info["cmdline"] or [])
        if ("c8_search.py" in c or "c8_cnn_search.py" in c) and "c8_finish" not in c: n += 1
    return n
t0 = time.time(); log("waiting for searches")
while time.time() - t0 < 6 * 3600:
    r = running()
    if r == 0: break
    time.sleep(60)
log(f"searches ended (running={running()}), waited {int((time.time() - t0) / 60)} min; starting analysis")
for p in psutil.process_iter(["cmdline"]):                           # if the time limit hit, stop leftover search workers before analysis
    c = " ".join(p.info["cmdline"] or [])
    if ("c8_search.py" in c or "c8_cnn_search.py" in c) and "c8_finish" not in c: p.kill()
time.sleep(10)
r = subprocess.run([sys.executable, "-I", "py/c8_analyze.py"], capture_output=True, text=True)
open("results/c8_analyze_stdout.txt", "w", encoding="utf-8").write(r.stdout + "\n" + r.stderr[-3000:]); log(f"analysis exit code {r.returncode}")
if r.returncode == 0:
    subprocess.run(["git", "add", "results/C8_SEARCH_REPORT.md", "results/c8_nested_picks.csv", "results/c8_winners_curse.csv", "results/c8_factor_breakdown.csv", "results/c8_bootstrap.csv", "results/c8_auroc_by_fold.csv",
                    "results/c8_search_log.csv", "results/c8_cnn_log_a.csv", "results/c8_cnn_log_b.csv", "results/c8_configs.json", "results/c8_cnn_configs.json", "py/c8_analyze.py", "py/c8_finish.py"], capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m", "Docs: C8 large nested search results (auto-generated, unattended)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"], capture_output=True); log("committed locally")
log("finished")
