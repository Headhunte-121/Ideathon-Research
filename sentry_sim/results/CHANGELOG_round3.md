# Changelog, round 3 (edge-AI proof)

Added (nothing existing edited): `py/c0_*, c1_*, c2_*, c3_*, c4_*, c5_*, c6_*`, `py/edge_nets.py`, `py/edge_int_model.py`; `rtl_edge/` (Verilog, testbench, vectors, weights); `run_edge_vivado.bat`; `splits/c1_edb_split.json`; `configs/c2_frozen.json`, `c3_quant_frozen.json`, `c5_frozen.json`; `results/c0_*` ... `c6_*`, `EDGE_AI_REPORT.md`, `round3_regression_start.txt`, `round3_regression_end.txt`.
Not touched: `rtl/`, `model/`, `tb/`, `run_vivado.bat`, team documents. (git already showed deleted/modified files in those folders and zips before this round started; unchanged by it.)

Freeze order (all committed locally, nothing pushed): split `59750b1` -> `c2_frozen` `e4f82a6` (before test scoring) -> C2 results -> C3 frozen parameters (before the Verilog vectors) -> Verilog check -> `c5_frozen` `b007471` -> chosen lead II committed before fold 10 was scored.

Deviations and notes
- C3: `py/c3_quantize.py` was run twice; the second run added the QAT fallback and a diagnostic column. The first-attempt and per-channel rows are deterministic and identical in both runs; the test folds were not used for any choice.
- C2: the first-launch regression call failed (relative `run_vivado.bat` not found from the helper batch) and was re-run with the full path; only the second run is saved.
- The first C2 commit accidentally staged earlier-round files and `__pycache__` (whole `py/` folder); it was reset locally (nothing pushed) and recommitted with only this round's files.
- Mutation checks use modified copies built at test time (no `ifdef` hooks in any source file).
- Not done: optional Artix-7 synthesis estimate; optional two-MAC-per-cycle Verilog variant; channel-1 sensitivity run on EDB; CUDA PyTorch (not installed; all training on CPU).

Bugs / traps handled: NaN samples (none found in EDB; forward-fill coded and counted); Windows multiprocessing `__main__` guards; quoted xsim plusargs through `Sim.run`; one key-name clash (`st`) in the windows script found on the first run and fixed before any result.
