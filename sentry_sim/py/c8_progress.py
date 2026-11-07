"""Live progress for the C8 search.  python py/c8_progress.py          (live, refreshes every 15 s; Ctrl+C to stop)
   python py/c8_progress.py --file   (also keeps results/C8_PROGRESS.txt updated; used by the background updater)"""
import os, sys, glob, time, json, datetime
os.chdir(r"C:\College\Ideathon\sentry_sim")
import psutil, pandas as pd
TOTAL_CFG = 400; hist = []


def status():
    d = pd.concat([pd.read_csv(p) for p in glob.glob("results/c8_cnn_log_*.csv")]).drop_duplicates(["cfg", "fold"])
    done_cfg = int((d.groupby("cfg").fold.nunique() == 5).sum()); rows = len(d)
    t = len(pd.read_csv("results/c8_search_log.csv")); now = time.time(); hist.append((now, rows)); hist[:] = [h for h in hist if now - h[0] < 300]
    rate = (hist[-1][1] - hist[0][1]) / max((hist[-1][0] - hist[0][0]) / 60, 1e-9) if len(hist) > 1 else 0.0
    left = TOTAL_CFG * 5 - rows; eta = left / rate if rate > 0.5 else float("nan")
    procs = [" ".join(p.info["cmdline"] or []) for p in psutil.process_iter(["cmdline"])]
    cnn = sum("c8_cnn_search" in c for c in procs); fin = any("c8_finish" in c for c in procs); done_rep = os.path.exists("results/C8_SEARCH_REPORT.md")
    vm = psutil.virtual_memory(); bar = "#" * int(30 * rows / (TOTAL_CFG * 5)) + "-" * (30 - int(30 * rows / (TOTAL_CFG * 5)))
    stage = "REPORT WRITTEN: results/C8_SEARCH_REPORT.md" if done_rep else ("analysis running / waiting to start" if cnn == 0 and fin else "CNN search running")
    return "\n".join([f"C8 progress  {datetime.datetime.now():%H:%M:%S}", f"CNN fits   [{bar}] {rows}/{TOTAL_CFG*5}  ({done_cfg} of {TOTAL_CFG} configs complete)",
                      f"speed      {rate:.0f} fits/min   ETA to search end: {'%.0f min' % eta if eta == eta else 'n/a'}   (then ~10-15 min analysis)",
                      f"processes  CNN search: {cnn}   finisher alive: {fin}", f"tabular    stopped at {t} fits (about {t // 5} configs)", f"memory     RAM used {vm.percent:.0f}%  free {vm.available / 1e6:.0f} MB   CPU {psutil.cpu_percent(1):.0f}%",
                      f"stage      {stage}"])


if __name__ == "__main__":
    wf = "--file" in sys.argv
    while True:
        try: s = status()
        except Exception as e: s = f"progress error: {e}"
        if wf: open("results/C8_PROGRESS.txt", "w", encoding="utf-8").write(s + "\n")
        else: os.system("cls"); print(s)
        if "REPORT WRITTEN" in s: break
        time.sleep(15)
