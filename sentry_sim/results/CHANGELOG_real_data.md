# Changelog: code changes made while running the real-data experiments (6 Nov 2026)

**No RTL file (`rtl/`, `model/`, `tb/`) was changed.** `run_vivado.bat` re-run after the work started: 22/22, 20/20, 35/35 pass; mutation A fails 16/35, mutation B fails 1/35.

## Bugs the real files exposed (and the fix)

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | `py/download_physionet.py` (named in the brief) did not exist | only `download_physionet_heart_rate.py` was in the folder | **new** `py/download_physionet.py`: sequential, size-checked, resumable, skips finished files, repairs truncated ones. The earlier `real_data/nsrdb` copy was incomplete (missing `16272.atr`, `16273.hea`, `16786.atr`) and is now complete (18 records) |
| 2 | `xsim` printed its usage text and wrote no detections file | `xsim` is a `.bat`; `cmd` splits unquoted `NAME=value` at `=`, so `-testplusarg ECGFILE=...` broke | `py/real_lib.py` `Sim.run`: every plusarg is quoted |
| 3 | `real_batch.py ecg` crashed on a missing `det_*.txt` with no hint | the simulator's output was never checked | `py/real_batch.py`: stops with the simulator's last lines if it did not report "replay done" |
| 4 | **0 beats detected on every NSTDB record** | real recordings carry a DC offset (NSTDB sits near -6 mV); at 16 codes/uV the 16-bit range is only +/-2.05 mV, so every sample sat on the rail | `py/real_lib.py` `to_codes_250`: a causal 0.5 Hz high-pass (what an AC-coupled ECG front end does), start state = first sample. The count of samples still on the rail is now printed (`CLIP_STATS`) and reported per record |
| 5 | README E4 command named records `a001-a020` | CEBS records are `b001-b020` (basal), `m001-m020` (music, 50 min each), `p001-p020` (post-music) | README corrected; only `b` and `p` were downloaded. A default `cebsdb` download would have pulled the `m` records (about 2.4 GB each) |
| 6 | PhysioNet "per 24 h" figure in the Verilog testbench uses `hours = beats / mean(bpm)` | mean of rates is not mean of RR | the report uses real elapsed time (sum of RR intervals); both are given where they differ |
| 7 | `run_vivado.bat` from a non-interactive shell: "run_vivado.bat is not recognized" | launcher context (shell/cwd), not the bat file | run it as `call settings64.bat && call <full path>\run_vivado.bat` from the project folder |
| 8 | PPG-DaLiA zip contains a nested `data.zip`; pickles sit in `PPG_FieldStudy/S#/` | file layout | extracted both levels into fresh folders; run with `--dir real_data/ppg_dalia/PPG_FieldStudy` |

## New or extended files

| File | What |
|---|---|
| `py/download_physionet.py` | new, see #1 |
| `py/real_lib.py` | plusarg quoting (#2), AC-coupling high-pass and clip counter (#4) |
| `py/real_batch.py` | `--inject N N ...` for the drift mode (heart-rate step over the last quarter of a recording, delay to the first flag per person, `results/real_drift_injection_*.csv`); clip report for ECG mode; simulator-failure guard (#3) |
| `py/real_scg_cebs.py` | `--out NAME` and per-second energy dump (`results/<NAME>_seconds.csv`) for the histogram; pandas import |
| `py/drift_model.py` | **new**: bit-exact Python copy of `baseline_drift_detector.sv` plus a *proposal-only* smoothed-feature helper. Checked against the Verilog: identical false-flag counts on 4 records, first-flag beat within 1 beat on 2 records |
| `py/analyze_drift.py` | **new**: per-person false check-ins and detection delays for the RTL feature and for 30/60/120-beat averages (`results/drift_variants.csv`) |
| `py/real_ppg_dalia.py` | prints the sitting motion baseline with 4 decimals (it printed `0.0`, which looked like a zero threshold but was 0.003 g); saves per-second flags to `results/real_ppg_dalia_seconds.csv` |
| `py/e5_episodes.py` | **new**: counts runs of pulse-lost-and-chest-still of at least 3 s (the Pod's arming hold) |
| `py/make_charts.py` | **new**: all PNGs in `results/` |
| `py/build_report.py`, `py/report_template.md` | **new**: fill `results/REAL_DATA_REPORT.md` from the CSVs |
| `README_REAL_DATA.md` | CEBS record names and download warning corrected |

## Thresholds / parameters: nothing tuned

`SCG_THR`, `MIN_THR`, K values, window sizes and the 16 codes/uV scale were left exactly as in the repository. Where results are poor (sections 3.1 and 3.4 of the report) the report gives the cause and a proposal and marks it untested.

## Correction (found on review)

The first version of `results/fig_e5_pulse_lost_and_still_by_activity.png` showed every bar 100 times too large (lunch 32.7 % instead of 0.33 %): `py/make_charts.py` multiplied a value that was already a percentage by 100 again. The report's tables and text were correct; only the chart was wrong. Fixed in `py/make_charts.py`, chart regenerated, and the bar labels now show two decimals.

## Tweaks round (after the first report): what was added

No RTL changed. New files: `tb/tb_real_ecg_beats_scaled.sv` (same replay testbench with a top-level `MIN_THR_TB` parameter; picked up by `run_vivado.bat`'s compile step, which was checked), `py/beat_model.py` (functional Python port of the beat detector; NOT bit-exact, scores agree with the Verilog within 0.12 points on clean ECG and 2.8 points in heavy noise: `results/tweak_beat_model_vs_rtl.csv`), `py/tweak1_features.py`, `py/tweak1_rules.py`, `py/tweak2_resting_drift.py`, `py/tweak3_scale.py`, `py/tweak4_adaptive_still.py`, `py/tweak5_early_beat.py`, `py/tweak_validate_beat_model.py`, `py/build_tweaks_report.py`, `py/tweaks_template.md`. `py/drift_model.py` gained an optional `return_state` flag (same detector logic). Reports: `results/TWEAKS_REPORT.md`, `results/POSTER_EVIDENCE_TWEAKS.md`.

Problems met and fixed on the way: `xelab -generic_top` does not survive the `.bat` launcher (one generated testbench per threshold instead); the Verilog replay testbench's timing race shifts its reported beat indices by a few samples, so the Python port is checked by score, not index; the first tweak-2 run counted detection wrongly for people already alarming before the injected step (now counted only among people not alarming, denominators shown); a first E5 chart was 100x too large (above).

**Claim withdrawn:** "heavy-noise beat detection is partly limited by our 16-bit scaling" (tweak 3 refutes it); corrected in `results/REAL_DATA_REPORT.md` and `results/POSTER_EVIDENCE_SUMMARY.md`.
