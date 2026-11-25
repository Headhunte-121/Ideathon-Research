# Reports

File paths such as `results/...` or `py/...` written inside a report are relative to the [`simulation/`](../../simulation) folder.

| Report | Covers |
|---|---|
| [REAL_DATA_REPORT.md](REAL_DATA_REPORT.md) | Round 1: beat detector, drift check, chest vibration and wrist pulse on public recordings |
| [TWEAKS_REPORT.md](TWEAKS_REPORT.md) | Follow-up changes, with separate tuning and test people |
| [REAL_DATA_REPORT_2.md](REAL_DATA_REPORT_2.md) | Round 2: ischemia, infarction and fibrillation datasets |
| [EDGE_AI_REPORT.md](EDGE_AI_REPORT.md) | Tiny neural network, 8-bit conversion, Verilog check and per-person calibration |
| [C8_SEARCH_REPORT.md](C8_SEARCH_REPORT.md) | Large model search, with the optimism of picking the best measured |

Result tables and figures are in [`simulation/results/`](../../simulation/results). Raw simulator and run logs are not kept in the repository; re-running a test or script regenerates them.

Commit IDs cited in the reports refer to this repository's history. The history was rewritten on 25 November 2026 to edit commit messages; file contents and commit dates in earlier commits are unchanged, and the cited IDs were updated to match.
