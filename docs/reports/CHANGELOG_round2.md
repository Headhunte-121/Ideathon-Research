# Changelog, round 2 (6 Nov 2026)

**No file in `rtl/`, `model/` or `tb/` was edited.** New simulation sources are in `rtl_variants/`. The baseline regression was re-run at the end: 22/22, 20/20, 35/35 pass; mutation A fails 16/35; mutation B fails 1/35 (`results/round2_regression_run.txt`).

## Rule deviations to know about
- In the previous tweaks round a testbench copy had been added to `tb/` (`tb_real_ecg_beats_scaled.sv`); it was **moved to `rtl_variants/`** this round and the two scripts that read it were updated.
- Round-1 tweak experiments (`results/tweak*`, `results/TWEAKS_REPORT.md`) were run before the round-2 rules existed (no seeded split files, no frozen configs). They are kept as history; the round-2 versions are B2 to B5 below.
- B3's pre-specified variants are not an independent test: S5 and S8, the two people with all the false arms, were examined in round 1 and fall in the round-2 test group.
- The A1 ST hint was **not run** (decision: LTSTDB raw/ST files too slow to download). `py/a1_hint.py` exists but has not been executed.

## Splits, frozen configs and local commits (never pushed)
`splits/dalia_split.json`, `splits/a4_split.json`, `splits/a1_split.json`; PTB-XL uses the dataset's folds. `configs/b3_frozen.json`, `b4_frozen.json`, `a4_frozen.json`, `a1_frozen.json`, `a3_frozen.json`, `a4_episodes.json`. Local commits: `4e7c09a` (DaLiA split + B3), `abf5f6c` (B4), `672b09a` (A4), the A1 split commit, `b12e732` (A1), `1d4a287` (A3). Each test stage checks the split file's SHA-256 against the frozen file.

## Bugs found and fixed while running on the new data
| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | SDDB beats: 295 beats in a 24.6 h record | invalid ADC samples (NaN) poison the high-pass filter for the rest of the record | forward-fill NaN samples and count them (`py/a4_beats_py.py`, `py/a4_windows_rtl.py`) |
| 2 | downloads about 7 s per small file; PTB-XL would need days | PhysioNet redirects some databases to an S3 host; one request per redirect | `py/download_physionet.py`: follows cross-host redirects, persistent connections, `--threads` for S3-hosted sets, `--ext/--prefix/--extra`, size preflight (`--dry-run/--max-gb`) |
| 3 | PTB-XL feature run crashed | Windows multiprocessing needs a `__main__` guard; one record missing from the first download | wrapped the stages in `main()`; fetched the missing record |
| 4 | `xelab -generic_top` ignored by the `.bat` launcher | `.bat` argument splitting at `=` | one generated testbench per threshold (`py/b2_scales.py`), defines in a small header file (B5) |
| 5 | Python beat-detector port differs from the Verilog by a few samples | the replay testbench's sample timing shifts its reported indices | port checked by score against the same annotations, not by index (`results/tweak_beat_model_vs_rtl.csv`); a streaming version added for day-long records |
| 6 | B5: variant identical to baseline at k up to 1.0 | k too low in the simulator; faster floor tracking made it worse (floor collapses before the wrist pulse loss is seen) | scanned k up to 1.75 and holdoff variants; the working k is unsafe on real data (emulated on CEBS, `py/b5_cebs_emulation.py`) |
| 7 | LTSTDB raw ECG 6 GB at about 0.15-0.5 MB/s | PhysioNet throttling | A1 needs only beat and episode annotations (complete); raw ECG and `.16a` download abandoned by decision, ST hint skipped |
| 8 | A4 flags: 18-72 false flags per hour | low-rate rule (pauses, ectopic beats) and irregularity threshold too sensitive | widened the grid **on tune records only**, then re-froze before testing |

## New or extended files
`py/download_physionet.py`, `py/b2_scales.py`, `py/b3_features.py`, `py/b3_ecg_rtl.py`, `py/b3_arming.py`, `py/b4_rest_drift.py`, `py/a1_ltstdb.py`, `py/a1_hint.py`, `py/drift_eval.py`, `py/a2_edb.py`, `py/a3_ptbxl.py`, `py/a4_windows_rtl.py`, `py/a4_beats_py.py`, `py/a4_analysis.py`, `py/beat_model.py` (streaming detector added), `py/drift_model.py` (`return_edges`), `py/b5_adaptive_sweep.py`, `py/make_charts2.py`, `py/build_report2.py`, `py/report2_template.md`, `rtl_variants/*` (generated variants and the scaled-ECG testbench), `splits/`, `configs/`.
