"""Fill py/report_template.md from results/_tables.md (+ E5 section if present) -> results/REAL_DATA_REPORT.md"""
import os, re
t = open("results/_tables.md", encoding="utf-8").read()
sec = {m.group(1).strip(): m.group(2).strip() for m in re.finditer(r"### (.*?)\n(.*?)(?=\n### |\Z)", t, re.S)}
def get(prefix):
    k = next(k for k in sec if k.startswith(prefix)); return sec[k]
rep = open("py/report_template.md", encoding="utf-8").read()
e5 = open("results/_e5_section.md", encoding="utf-8").read() if os.path.exists("results/_e5_section.md") else \
    "**NOT RUN YET.** The PPG-DaLiA data (2.7 GB, UCI) had not finished downloading when this report was generated, so no E5 number exists. Nothing in sections 3.1-3.5 depends on it."
scope = "15 people, about 2 h each, wrist PPG (Empatica E4), chest accelerometer (RespiBAN), activity labels" if os.path.exists("results/_e5_section.md") else "NOT RUN YET (download pending)"
note = "E5 results are in section 3.6" if os.path.exists("results/_e5_section.md") else "E5 pending"
for k, v in {"<<E1>>": get("E1 table"), "<<E2>>": get("E2 table"), "<<E3A>>": get("E3 table"), "<<E3B>>": get("E3 detection"),
             "<<E3C>>": get("E3 proposal"), "<<E4>>": get("E4 table"), "<<E5>>": e5, "<<E5SCOPE>>": scope, "<<E5NOTE>>": note}.items():
    rep = rep.replace(k, v)
open("results/REAL_DATA_REPORT.md", "w", encoding="utf-8").write(rep); print("wrote results/REAL_DATA_REPORT.md", len(rep), "chars")
