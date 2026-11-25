# Sentry simulation: where to find things

Nothing is moved or renamed by this file; it only points to what is already here.

## Start here
| I want to... | Open |
|---|---|
| Read the real-data results (what was run, numbers, what they do NOT show) | [results/REAL_DATA_REPORT.md](results/REAL_DATA_REPORT.md) |
| Paste the 10 evidence lines on the poster | [results/POSTER_EVIDENCE_SUMMARY.md](results/POSTER_EVIDENCE_SUMMARY.md) |
| See every code change made while running on real files | [results/CHANGELOG_real_data.md](results/CHANGELOG_real_data.md) |
| Read the follow-up changes tried after the first report (5 tweaks, tune/test split) | [results/TWEAKS_REPORT.md](results/TWEAKS_REPORT.md) |
| Paste the poster lines from the tweaks round | [results/POSTER_EVIDENCE_TWEAKS.md](results/POSTER_EVIDENCE_TWEAKS.md) |
| Read round 2 (real ischemia / arrest datasets + the tweaks, with tune/test splits) | [results/REAL_DATA_REPORT_2.md](results/REAL_DATA_REPORT_2.md) |
| Paste round-2 poster wording (may say / must not say) | [results/POSTER_EVIDENCE_ROUND2.md](results/POSTER_EVIDENCE_ROUND2.md) |
| See round-2 code changes and bugs | [results/CHANGELOG_round2.md](results/CHANGELOG_round2.md) |
| Understand the whole simulator | [README.md](README.md) |
| Re-run the real-data experiments (exact commands) | [README_REAL_DATA.md](README_REAL_DATA.md) |

## Folders
| Folder | What is in it |
|---|---|
| [rtl/](rtl) | Verilog for the Pod and PulseBand logic (beat detector, drift detector, alarm FSM, noise canceller) |
| [model/](model) | Simulation-only models: patient, sensor chips, BLE link, phone app |
| [tb/](tb) | Testbenches (system end-to-end, decision logic, drift false alarms, real ECG replay, ...) |
| [py/](py) | Python: downloads, real-data batch runs, analysis, charts, report builder |
| [splits/](splits), [configs/](configs), [rtl_variants/](rtl_variants) | Round-2 tune/test split files, frozen configurations (committed locally before each test run), and generated RTL variants + variant testbenches (baseline rtl/, model/, tb/ untouched) |
| [results/](results) | Everything produced by runs (see the lists below) |
| data/ | Generated heart-rate and ECG hex files fed to the testbenches (can be regenerated) |
| real_data/ | Downloaded public recordings, about 29 GB (nsrdb, nstdb, cebs, ppg_dalia, plus the original zips) |
| xsim_work/ | Vivado simulator scratch files |

Batch files in this folder: [run_vivado.bat](run_vivado.bat) (all regression tests), [run_real_data.bat](run_real_data.bat) (one NSRDB person).

## results/ by experiment
| Experiment | Files |
|---|---|
| Regression (simulated) | `vivado_*.txt`, `system_end_to_end_log.txt`, `mutation_A_log.txt`, `mutation_B_log.txt`, `regression_run.txt` |
| E1 beat detector, real noise (NSTDB) | `real_ecg_nstdb.csv`, `fig_e1_beat_detector_vs_snr.png`, `e1e2_ecg_clipping.csv` |
| E2 beat detector, clean (NSRDB) | `real_ecg_nsrdb.csv`, `fig_e2_beat_detector_clean.png` |
| E3 drift detector (NSRDB) | `real_drift_nsrdb.csv`, `real_drift_injection_nsrdb.csv`, `drift_variants.csv`, `fig_e3_false_checkins_per_person.png`, `fig_e3_detection_vs_shift.png` |
| E4 chest vibration (CEBS) | `e4_scg_*.csv` (baseline / post-music, 660 and 220 mV/g), `e4_band_energy_baseline_660mVg.csv`, `fig_e4_chest_vibration_vs_still_threshold.png` |
| E5 wrist pulse + motion (PPG-DaLiA) | `real_ppg_dalia.csv`, `real_ppg_dalia_seconds.csv`, `e5_episodes.csv`, `e5_ppg_dalia_log.txt`, `fig_e5_pulse_lost_and_still_by_activity.png` |
| Tweak 1 false starts (DaLiA) | `tweak1_false_starts.csv`, `tweak1_selection.txt`, `tweak1_ecg_gap_living.csv`, `tweak1_features_log.txt` (per-second features cached in `data/dalia_feats/`) |
| Tweak 2 resting drift (DaLiA) | `tweak2_resting_drift.csv`, `tweak2_selection.txt`, `tweak2_context_hr.csv`, `tweak2_log.txt` |
| Tweak 3 beat detector scale (NSTDB) | `tweak3_scale_nstdb.csv`, `tweak3_log.txt` |
| Tweak 4 adaptive still threshold (CEBS) | `tweak4_adaptive_still.csv`, `tweak4_gravity.csv`, `tweak4_log.txt` |
| Tweak 5 early-beat rejection | `tweak5_early_beat.csv` |
| Python beat-detector port check | `tweak_beat_model_vs_rtl.csv` |
| Round 2 (B2-B5, A1-A4) | `b2_*`, `b3_*`, `b4_*`, `a1_*`, `a2_*`, `a3_*`, `a4_*`, `b5_*` (CSV), `fig_b2_*`, `fig_b3_*`, `fig_a1_*`, `fig_a3_*`, `fig_a4_*`, `fig_b5_*`; logs `b2_log.txt`, `b5_log*.txt`, `a*_log.txt` |
| Report build inputs | `_tables.md`, `_e5_section.md` (made while building the report; the report is rebuilt with `python py/build_report.py`) |
| Download logs | `download_log.txt`, `download_log_cebs.txt` |

## py/ by job
| Job | Scripts |
|---|---|
| Download data | `download_physionet.py`, `download_physionet_heart_rate.py` |
| Run experiments | `real_batch.py` (E1-E3), `real_scg_cebs.py` (E4), `real_ppg_dalia.py` + `e5_episodes.py` (E5) |
| Drift diagnosis | `drift_model.py` (Python copy of the RTL), `analyze_drift.py` |
| Tweaks | `tweak1_features.py`, `tweak1_rules.py`, `tweak2_resting_drift.py`, `tweak3_scale.py`, `tweak4_adaptive_still.py`, `tweak5_early_beat.py`, `beat_model.py` (Python port of the beat detector), `tweak_validate_beat_model.py` |
| Round 2 experiments | `b3_features.py`, `b3_ecg_rtl.py`, `b3_arming.py`, `b4_rest_drift.py`, `a1_ltstdb.py`, `a1_hint.py`, `drift_eval.py`, `a2_edb.py`, `a3_ptbxl.py`, `a4_windows_rtl.py`, `a4_beats_py.py`, `a4_analysis.py`, `b2_scales.py`, `b5_adaptive_sweep.py` |
| Charts and reports | `make_charts.py`, `make_charts2.py`, `build_report.py`, `build_report2.py`, `report2_template.md`, `report_template.md`, `build_tweaks_report.py`, `tweaks_template.md` |
| Shared helpers | `real_lib.py` |
| Older helpers | `real_data_prepare.py`, `real_data_score.py`, `check_noise_canceller_vs_float.py` |
