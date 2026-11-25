# Edge-AI proof, round 3: a tiny heartbeat-shape network (trained, shrunk to 8-bit, copied into Verilog)

Written 7 Nov 2026 for the Autonomous Sternal Sentry ideathon entry (no hardware exists). Every number below comes from a file in `results/`. Evidence labels: **Replayed** (our model or Verilog on a public recording), **Simulated** (xsim), **Calculated** (arithmetic from the design), **Cited**, **Assumed**, **Proposed**, **Target**.

---

## 0. Summary

**What we built.** A very small neural network ("beatnet-tiny": 1,538 numbers, 43,144 multiply-adds per heartbeat). It looks at one heartbeat's shape (0.6 s of ECG) and says "this beat looks like it is inside a cardiologist-marked ST-change episode" or "ordinary beat". We trained it on public ECG recordings (European ST-T Database, EDB), shrank it to 8-bit whole numbers, and wrote a Verilog copy of those 8-bit calculations.

**What the numbers say.**
1. **Verilog copy: it works as arithmetic.** On 2,000 real held-out beats plus 64 extreme test patterns, the Verilog gave exactly the same answer as our Python 8-bit model every time (2,064 of 2,064; a deliberately broken copy failed, so the test can fail). It takes 44,962 clock cycles per beat at one multiply-add per clock (**Simulated**).
2. **AI vs a simple rule on EDB: no added value shown.** On patients the network never saw, it was *not* better than a simple ST-amplitude rule at the same false-alarm rate. A small six-number logistic model on the same beats did better than the network. The result is the same sign in 5 of 5 ways we looked at it.
3. **8-bit vs 32-bit: fails our pre-written test.** The 8-bit network ranks beats almost exactly like the 32-bit one (area under the curve within 0.04 on every fold), but when a single alarm threshold is applied, the decisions agree on only 93-99.9 % of beats (rule required >= 99 %) and the episode sensitivity moved by more than 2 points on 4 of 5 folds. First attempt and both fallbacks all fail the rule.
4. **Leakage matters hugely.** The same recipe scores area-under-curve 0.95 if beats of the same person are mixed between training and test, and 0.39 (worse than a coin) on the first patient-wise test fold. Anyone quoting a high number without a patient-wise split is quoting a leak.
5. **PTB-XL (a different dataset: 10-second resting ECGs, heart-attack diagnosis vs normal):** the tiny network (lead II, area under the curve 0.87-0.89 over three seeds) was in the same range as our earlier five-number model (0.859) and clearly better than ST alone (0.655). This is a diagnosis on a resting ECG in hospital, not early warning, and not a chest-patch signal.

**What the numbers do NOT say.** Public data has no recording with chest vibration + ECG + wrist pulse during a heart attack. So **nothing here can show that early ischemia or arrest is sensed with our sensor set.** The Verilog block is a separate stand-alone copy; it is not wired into the Pod's alarm logic, and the nRF5340 is a microcontroller, not an FPGA. No battery, energy or "milliseconds on the chip" figure is claimed.

**The single most important honest sentence about the labels:** the EDB "ST episodes" were marked by cardiologists using an ST-amplitude rule (ST deviation of at least 0.1 mV for at least 30 s), so a rule that measures ST amplitude partly "knows the answer", and a model that beats a crude rule may only be measuring ST better; winning would not mean it understands ischemia (and EDB does not say which ST changes were ischemic).

---

## 1. Inventory (C0)

**Machine.** 16 logical CPUs; NVIDIA GeForce RTX 5050 Laptop GPU present, but PyTorch is `2.14.1+cpu` (CUDA unavailable). The CUDA build was not installed (large download, not needed): **every model of the final run was trained on CPU**, one process per (fold, seed), 1 torch thread each (53-208 s per model). Python 3.14.3, numpy/scipy/pandas/wfdb/scikit-learn/matplotlib present. Vivado xsim 2025.2 (`C:\AMDDesignTools\2025.2`). Free disk 165 GB. Nothing was downloaded; no `real_data` size scan was run. `git status` at the start already showed many modified/deleted files outside this task (e.g. old `rtl/drift_det.sv`, `rtl/nlms16.sv`, `rtl/sentry_fsm.sv`, `rtl/sentry_top.sv`, `tb/tb_drift.sv` etc. deleted, `../sentry_sim*.zip` modified); I did not touch them.

**Baseline regression** (`results/round3_regression_start.txt`): 22/22, 20/20, 35/35, mutation A 19 passed 16 failed, mutation B 34 passed 1 failed. Identical at the end (`results/round3_regression_end.txt`). (The first launch of the regression failed because a relative `run_vivado.bat` call did not resolve; it was re-launched with the full path. No result was kept from the failed launch.)

**Dossier arithmetic (Calculated; `results/c0_dossier_arithmetic.csv`).**

| Network | MACs | Weights + biases = parameters | int8 weight bytes | ideal cycles (MACs / 2) | ideal time at 128 MHz |
|---|---:|---:|---:|---:|---:|
| Dossier Q6.4 "Stage 2" (3->16, 16->32, 32->32 conv k3 over 6,000 samples, + 32->2) | 28,512,064 (28,512,000 conv + 64 final) | 4,816 + 82 = 4,898 | 4,816 (about 4.8 KB) | 14,256,032 | **111.4 ms** |
| beatnet-tiny (ours, per heartbeat) | 43,144 | 1,496 + 42 = 1,538 | 1,496 | 21,572 | 0.169 ms |

The notes' quoted figures (a stage-2 time of 1.8 ms from 230,400 cycles; 0.74 ms in Q6.1; a 410 KB model) are about 62x too fast and about 80x too big for 4,898 parameters, so they must not be printed. Our network is about 660x smaller in compute than the Q6.4 network. *Both timings are Calculated, ideal lower bound; real firmware is slower.* Nothing else about energy or battery is computed.

**EDB record check** (`results/fig_c0_edb_check.png`, record e0103, channel 0 = lead V4, 2.0 h, 7,296 annotated beats, 5 ST episodes, 0 T episodes): the plotted annotation marks and the detected R peaks line up with the QRS complexes.

**EDB facts confirmed from the PhysioNet documentation (not from memory).** ST episode = ST deviation of at least 0.1 mV lasting at least 30 s; T episode = T deviation of at least 0.2 mV for at least 30 s; deviation measured against a reference beat taken from the first 30 s of the record; ischemia is stated only at the subject level ("diagnosed or suspected"), not per episode. Two cardiologists annotated each record independently; a third resolved differences.

---

## 2. C1: windows, labels, split (EDB). *Replayed.*

**Method.** `py/c1_make_split.py`, `py/c1_edb_windows.py`, `py/c1_lib.py`. Split of subjects into 5 folds written **before** any experiment (`splits/c1_edb_split.json`, seed 20261107, SHA-256 `4d6f08c9...c9971a`, committed `59750b1`). Subjects: records with identical header comments (age, sex, diagnosis; recorder and medications ignored) are one subject; this gives **79 subjects from 90 records**, matching the published subject count. Folds have 16/16/16/15/16 subjects and 26.5 k positive beats each. Beats = the database's beat annotations; kept only if the beat is `N`, the previous beat is `N` and RR is 0.4-1.5 s; R peak = largest |value| within +-60 ms. Channel 0 through `real_lib.to_codes_250` (16 codes/uV, 0.5 Hz causal high-pass). Window: R-50..R+99 at 250 Hz, pair-averaged to 75 samples, baseline = mean of R-18..R-11, `>> 8` (1 LSB = 16 uV), clipped to int8. Labels: positive = inside an ST episode; negative = at least 30 min from every ST/T episode; everything else excluded from training and scoring but still passed through the causal baselines. First 60 s of each record never scored. R1 needs at least 30 eligible beats in the previous 10 min; beats without that history are dropped from every method's scoring (Assumption A5).

**Data / result** (`results/c1_edb_counts.csv`).

| | beats |
|---|---:|
| Annotated beats (90 records, 180.0 h) | 790,565 |
| Excluded: not `N`, previous not `N`, or RR outside 0.4-1.5 s | 16,413 |
| Excluded: window would leave the record | 45 |
| Eligible beats | 774,107 |
| of which scored positive (in an ST episode) | 132,374 |
| scored negative (>= 30 min from every episode) | 128,285 |
| excluded as near an episode or inside a T-only episode | 507,450 |
| first 60 s (not scored) | 5,998 |

Per fold (positive / negative scored beats): fold 0 26,502 / 24,666; fold 1 26,458 / 29,654; fold 2 26,487 / 30,523; fold 3 26,456 / 30,261; fold 4 26,471 / 13,181. ST episodes (unmerged, counting each ST1/ST2 marker separately): 364, T episodes 396. Channel-0 lead names: V5 39 records, MLIII 18, V4 15, V2 9, V1 4, V3 4, D3 1. NaN samples: 0 in all records. Fraction of samples on the 16-bit ADC rail: median 4e-6, maximum 1.9 % (one record). Checks: windows are built by a function that receives only samples R-50..R+99 (changing samples after R+99 leaves the window unchanged, asserted), and no scored beat is earlier than 60 s (asserted).

**What it shows.** The data set, labels and split are in place; each fold has tens of thousands of positive beats from only 43-101 episodes, so the effective sample is the *episodes and subjects*, not the beats.

**What it does NOT show.** Anything about performance. Beats inside one episode are strongly correlated.

---

## 3. C2: train, score, compare (EDB). *Replayed.*

**Method.** Settings frozen in `configs/c2_frozen.json` (commit `e4f82a6`) before any outer-test scoring; train/validation selection in `py/c2_train.py`, test scoring once in `py/c2_score.py` (`data/edge/c2_scores_fold*.npz`), evaluation in `py/c2_eval.py`. Outer fold k: test = fold k, inner validation = fold (k+1) mod 5, train = other three. M2 = tiny CNN float, 3 seeds (Adam lr 1e-3, wd 1e-4, batch 256, <= 30 epochs, early stop on validation AUPRC patience 5, balanced 1:1 epochs; early stopping picked epochs 0-22, mean 10.7 epochs run). M1 = standardised logistic regression on six hand features (C picked on validation). R0 = |ST level|; R1 = |ST - median ST of previous 10 min|. Operating point = score threshold giving 1 % false-positive rate on inner-validation negatives. Episode alert = 24 of the last 30 eligible beats above threshold; caught = alert between onset and end. Bootstrap by subject, 2,000 resamples. No frozen setting changed after seeing test numbers; test set not re-used.

**Result A: beat level, pooled over the five test folds** (`results/c2_beat_metrics.csv`; 132,371 positive and 128,260 negative scored beats, prevalence 0.508).

| Method | AUROC | AUPRC | sensitivity at 1 % FPR (curve, per-fold) | deployed sensitivity | deployed FPR |
|---|---:|---:|---:|---:|---:|
| R0 absolute ST | 0.640 | 0.593 | 0.124 | 0.106 | 0.081 |
| R1 personal-baseline ST | 0.719 | 0.730 | 0.120 | 0.128 | 0.021 |
| M1 six-feature logistic | 0.663 | 0.652 | 0.232 | 0.198 | 0.082 |
| M2 CNN seed 0 | 0.629 | 0.602 | 0.109 | 0.062 | 0.088 |
| M2 CNN seed 1 | 0.649 | 0.630 | 0.091 | 0.081 | 0.088 |
| M2 CNN seed 2 | 0.570 | 0.573 | 0.070 | 0.070 | 0.087 |
| R0 clinical-style point |ST| >= 100 uV | - | - | - | 0.622 | 0.385 |

(Pooled AUROC/AUPRC concatenate raw scores of five differently trained models and are only indicative; per-fold values are in the CSV: M2 seed 0 AUROC by fold 0.389, 0.702, 0.564, 0.800, 0.747.) The deployed FPR on the test folds is far above the 1 % chosen on validation (e.g. 8-9 % for R0, M1, M2): thresholds set on other patients do not transfer.

**Result B: pass rule 1 (subject bootstrap, `results/c2_bootstrap.csv`).**

| Quantity | point | 95 % range |
|---|---:|---:|
| R0 sensitivity at 1 % FPR | 0.124 | 0.062-0.284 |
| R1 | 0.120 | 0.081-0.204 |
| M1 | 0.232 | 0.162-0.414 |
| M2 (mean of 3 seeds; seed range 0.070-0.109) | 0.090 | 0.069-0.223 |
| **M2 - better rule (R0)** | **-0.034** | **-0.161 to +0.089** |
| M2 - R1 | -0.030 | -0.079 to +0.073 |
| M2 - M1 | -0.142 | -0.261 to -0.048 |

**Pass rule 1 outcome: the lower end (-0.161) is not above 0, so: "no added value shown on this data".** The network is also worse than the six-number logistic model M1 (range excludes 0).

**Result C: episode level, 90 records, 364 ST episodes, 31.0 episode-free hours** (`results/c2_episode_metrics.csv`, rule 24 of 30 beats).

| Method | caught | sensitivity | median lead (min, positive = before onset) | false alerts | false per 24 h | records with a false alert |
|---|---:|---:|---:|---:|---:|---:|
| R0 | 20 / 364 | 5.5 % | -1.8 | 5 | 3.9 (5 events) | 1 |
| R1 | 73 / 364 | 20.1 % | -1.1 | 1 | 0.8 (**1 event: too uncertain to quote**) | 1 |
| M1 | 44 / 364 | 12.1 % | -0.8 | 39 | 30.2 | 3 |
| M2 seeds 0 / 1 / 2 | 24 / 28 / 21 | 6.6 / 7.7 / 5.8 % | -1.4 / -1.1 / -0.7 | 53 / 48 / 13 | 41.0 / 37.2 / 10.1 | 2 / 1 / 2 |
| R0 at |ST| >= 100 uV | 177 / 364 | 48.6 % | -0.5 | 175 | 135 | 21 |
| existing drift: `rtl K=3.8` | 33 / 247 merged episodes | 13.4 % | +16.8 | 25 | 18.9 | 20 |
| existing drift: A1 frozen `rest_proxy +25% for 10 min` | 7 / 247 | 2.8 % | +1.3 | 1 | 0.8 (1 event: too uncertain) | 1 |

(The drift rows use the older code that merges overlapping episodes, so their denominator is 247, not 364; its time window also starts 30 min before onset, a different convention from the 'between onset and end' rule here. They are shown for scale, not as a like-for-like comparison.) False-alert counts are small and concentrated in 1-4 records, so the false-per-24-h values are rough; rows resting on fewer than about 5 events are marked too uncertain. Persistence sensitivity rows (80 % rule at 15 and 60 beats; descriptive, not tuning): caught 31/36/34/32 and 8/18/22/20 of 364 for R0/M2(s0,s1,s2) at 12-of-15 and 48-of-60 respectively; full table in the CSV.

**Result D: where it fails** (`results/c2_failure_analysis.csv`, M2 seed 0 at its deployed threshold, beat sensitivity over positive beats): heart rate under 60 bpm 2.5 %, 60-80 bpm 3.2 %, 80-100 bpm 4.4 %, 100 bpm or more 11.8 %; by channel-0 lead: V1 16.6 %, V3 7.9 %, V2 8.0 %, V5 6.8 %, V4 3.1 %, MLIII 2.3 %, D3 0.3 %. Episode-level: ST depression 5.4 % vs elevation 8.1 % of episodes caught; shortest third of episodes (0.5-1.8 min) 2.5 %, longest third (5-88 min) 11.6 %. Five subjects with zero beat sensitivity for M2: s00, s10, s37, s46, s48 (R0's five lowest: s00, s03, s10, s37, s70). Everything is low everywhere; no group is reliably handled.

**Result E: the leakage demonstration** (`results/c2_leakage_demo.csv`, M2 recipe seed 0, same sizes of train/validation/test beats as fold 0):

| Split | validation AUPRC | test AUROC | test AUPRC | sensitivity at 1 % FPR | deployed sens / FPR |
|---|---:|---:|---:|---:|---:|
| patient-wise (fold 0, seed 0) | 0.838 | 0.389 | 0.423 | 0.001 | 0.109 / 0.401 |
| random beat-wise (subjects mixed) | 0.960 | 0.954 | 0.959 | 0.597 | 0.598 / 0.010 |

The gap is about **0.57 in AUROC**; the mixed split also lets the network pass the validation test and hit the 1 % FPR target, which the patient-wise split never does. Note the patient-wise fold-0 AUROC below 0.5: the validation fold (fold 1) said 0.84 AUPRC, the new patients said below chance, i.e. what the network learned on some people points the wrong way on others.

**Result F: through the Python port of our detector** (`results/c2_secondary_detector.csv`, fold-0 test records, frozen fold-0 seed-0 M2, R0, R1; detected beats instead of annotated ones, 145,125 detections, 51,695 scored beats vs 51,168 annotated): sensitivity at 1 % FPR changed by +0.004 (R0), +0.012 (R1), +0.017 (M2), all near zero; AUROC 0.42/0.63/0.46 vs 0.42/0.62/0.39. Label: **Replayed end to end through the Python port of our beat finder (not bit-exact RTL).** Detected beats are not filtered to `N` beats, so the sets differ slightly.

**What it shows.** On unseen patients the network did not beat the simple rule; ordinary ST-measurement features (M1) and the personal-baseline rule (R1) carried more. Mixing beats of one person between train and test hugely inflates scores.

**What it does NOT show.** That a larger or better-trained network, a different input shift, other leads, or more data would not help (the early-stopped epochs were 0-22; the network overfits subjects quickly). Nothing about early warning: these are labels *during* ST episodes. Because the labels came from an ST-amplitude rule, even a win would not show understanding of ischemia, and EDB does not say which ST changes were ischemic. R0's poor result probably partly reflects the labels being measured against each record's first-30 s reference beat, which an absolute-level rule cannot know.

---

## 4. C3: shrink to 8-bit integers. *Replayed (integer model on public recordings) + Calculated.*

**Method.** `py/c3_quantize.py`, `py/edge_int_model.py` (the integer reference = the specification for the Verilog), `py/c3_freeze.py`. Symmetric per-tensor int8 weights, int32 biases, int8 activations (ReLU outputs clamped to [0,127]) with scales from the 99.9th percentile of 4,000 training-patient beats, requantisation `y = (acc*M0 + (1<<(n-1))) >> n` (int64, arithmetic shift, M0 in [2^30, 2^31)), pooling keeps the sum of 19 positions, score = logit1 - logit0 (int32). Seed-0 model of each outer fold quantised with its own training patients. Integer threshold = the one with the same positive fraction as the float threshold on the inner-validation fold. Fallback a = per-output-channel conv scales; fallback b = 3 epochs of quantisation-aware fine-tuning (straight-through estimator). First attempt and fallbacks are all listed.

**Result** (`results/c3_int8_vs_float.csv`; first attempt, per fold):

| Fold | AUROC float -> int | sens at 1 % FPR float -> int | decision agreement | ST episodes caught float -> int (of) | change, pp |
|---|---|---|---:|---|---:|
| 0 | 0.389 -> 0.395 | 0.001 -> 0.001 | 93.2 % | 8 -> 25 (66) | -25.8 |
| 1 | 0.702 -> 0.740 | 0.114 -> 0.131 | 97.8 % | 2 -> 6 (101) | -4.0 |
| 2 | 0.564 -> 0.553 | 0.037 -> 0.029 | 93.4 % | 7 -> 0 (67) | +10.4 |
| 3 | 0.800 -> 0.791 | 0.301 -> 0.279 | 98.9 % | 7 -> 5 (43) | +4.7 |
| 4 | 0.747 -> 0.748 | 0.092 -> 0.091 | 99.9 % | 0 -> 0 (87) | 0.0 |

Fallback a (per-channel) agreement: 93.1, 98.0, 93.4, 98.8, 99.9 %; fallback b (QAT): 90.9, 98.9, 93.4, 98.7, 99.9 %; episode counts essentially unchanged by the fallbacks.

**Pass rule 2 outcome: INT8 NOT acceptable under the rule as written** (a: episode sensitivity within 2 points only on fold 4 - the others moved by 4.0 to 25.8 points; b: agreement >= 99 % only on fold 4). The cause is not the arithmetic: the integer and float models rank beats nearly identically (AUROC differences of +0.006, +0.038, -0.010, -0.009, +0.001), but a single alarm threshold sitting in the extreme tail of one validation set flips thousands of borderline beats, and when the float model's deployed rate is near zero or near 40 % the episode counts swing. As a diagnostic only (not a pass/fail), using the integer model's own 1 % threshold gives deployed sensitivity/FPR on fold 0 of 0.107/0.370 vs float 0.109/0.401. Size and memory (Calculated, `results/c3_layers.csv`): 1,496 int8 weights + 42 int32 biases (168 B) + 200 B of requantisation constants = **1,864 B flash**; peak activation memory with two ping-pong buffers **1,208 B** (+75 B input); 43,144 MACs; **ideal cycles = 21,572 (MACs / 2, SMLAD) and ideal time 168.5 microseconds at 128 MHz: Calculated, ideal lower bound; real firmware is slower.** Largest accumulator magnitude seen on any fold 1.2e5 (< 2^17), so 32-bit accumulators are ample. Float32 storage of the same 1,538 parameters would be 6,152 B (Calculated).

**What it shows.** The network can be written as whole-number arithmetic with a few hundred requantisation constants and keeps its ranking quality; the weights are 1.5 KB.

**What it does NOT show.** That the shrunk model is better or worse at detecting anything (the float model itself did not beat the rules); the pass rule's decision-agreement requirement was not met.

---

## 5. C4: Verilog copy of the integer network, bit-exact. *Simulated.*

**Method.** `rtl_edge/rtl/edge_cnn_beat.sv` (one shared int8 x int8 -> int32 MAC, one controller with layer/channel/position/tap/input-channel counters, ROMs loaded with `$readmemh` from `rtl_edge/weights/`, two ping-pong buffers of 608 and 600 bytes, 64-bit requantiser with arithmetic shift, zero-padding handled in the controller, global pooling by adds with no division). Testbench `rtl_edge/tb/tb_edge_cnn.sv`, vectors from `py/c4_make_vectors.py`: **2,000 held-out fold-0 test beats** (1,000 positive-label, 1,000 negative-label, seeded; 15 different subjects have at least 20 beats each) **+ 64 synthetic extreme vectors** (all +127, all -128, zeros, alternating, ramps, impulses, random). Expected scores are `forward_int`. The 2,064 vectors ran as 12 parallel xsim chunks, each with its own work folder (`xsim_work_c4_m0..m11`), and were merged (`py/c4_run.py`); serial runner `run_edge_vivado.bat` provided. Integer parameters frozen in `configs/c3_quant_frozen.json` and committed before the vectors were generated.

**Result.** `results/c4_rtl_vs_python.csv`, `results/c4_rtl_log.txt`:

| | vectors | bit-exact | mismatches |
|---|---:|---:|---:|
| real held-out beats | 2,000 | 2,000 | 0 |
| synthetic extreme | 64 | 64 | 0 |
| **total** | **2,064** | **2,064** | **0** |

**Pass rule 3 outcome: PASS (100 % bit-exact).** **Mutation checks** (`results/c4_mutation_check.csv`): a copy with the rounding constant changed from `1<<(n-1)` to `1<<(n-2)` failed 120 of 120 vectors; a copy with one conv2 weight changed by +1 failed 45 of 120, so the test can fail. (Mutations are modified *copies* generated at build time in `xsim_work_c4_mutsrc`; no source file was edited.) **Cycles** (`results/c4_cycles.csv`, `results/fig_c4_cycles.png`): every vector takes **44,962 compute cycles** after the 75-sample load = 43,144 multiply-accumulate cycles (zero-padding taps counted as MAC cycles with zero input, equal to the Calculated MAC count) + 1,512 initialisation cycles (one per output element) + 304 pooling adds + 2 final-layer initialisation cycles; overhead 4.2 %. At **one multiply-add per cycle** (label: Simulated). The optional two-MAC-per-cycle variant and the optional Artix-7 synthesis estimate were **not done** (time).

**What it shows.** The 8-bit arithmetic is simple and fixed-point enough to be reproduced exactly by a small, readable Verilog block with one multiplier.

**What it does NOT show.** The block is a **separate stand-alone copy of the network arithmetic. It is not wired into `pod_node.sv` or the alarm logic**, and the nRF5340 is a microcontroller, not an FPGA. No area, timing, power or "milliseconds on the chip" figure exists. It is what the design would use if the Pod's model moved to dedicated silicon (a **NEXT**-tier idea).

---

## 6. C5 (optional): PTB-XL, tiny CNN vs five-feature model. *Replayed.*

**Method.** `py/c5_windows.py`, `py/c5_ptbxl_cnn.py`; recipe frozen in `configs/c5_frozen.json` (commit `b007471`), lead chosen on fold 9 (lead II, mean validation AUROC 0.910 vs I 0.858, V2 0.831, V5 0.889; chosen lead committed before fold 10 was scored). Median beat per lead, same int8 window as C1 (causal 0.5 Hz high-pass; the earlier five-feature model used a zero-phase filter, so the comparison is not perfectly like-for-like). Patient-level bootstrap (2,000). Comparators: the A3 logistic models re-fit with the frozen A3 settings. PTB-XL records are **10-second resting diagnostic 12-lead ECGs; labels are diagnostic SCP codes**; this is not early warning, not a wearable and not a sternal lead.

**Result** (`results/c5_ptbxl_test.csv`, fold 10, lead II: 1,461 records, 549 MI; AUROC with 95 % patient-bootstrap range):

| Model | AUROC |
|---|---|
| CNN float seeds 0 / 1 / 2 | 0.891 (0.872-0.910) / 0.869 (0.848-0.889) / 0.889 (0.869-0.908) |
| CNN INT8 (seed 0) | 0.892 (0.873-0.911) |
| Five-feature logistic (A3) | 0.859 (0.838-0.880) |
| ST only | 0.655 (0.620-0.689) |
| Heart rate only | 0.629 (0.595-0.661) |

INT8 vs float (seed 0, fold-9 operating point): sensitivity 0.756 vs 0.743, specificity 0.873 vs 0.875, decision agreement 98.6 %. Other leads (CNN seeds, AUROC): I 0.838-0.862, V2 0.800-0.814, V5 0.867-0.875 (five-feature: 0.839, 0.714, 0.856).

**What it shows.** On a clean diagnostic task the tiny network is in the same range as, and on lead II not clearly above, the five-feature model, and far above ST alone; INT8 costs about nothing in AUROC here.

**What it does NOT show.** Early warning, a wearable result, or anything about ischemia before an event: these are resting-ECG diagnosis labels in hospital recordings. The seed-to-seed spread (0.869-0.891) is as large as the gap to the five-feature model.

---

## 7. C6 (optional): "an hour before", a weak hypothesis test. *Replayed, hypothesis only.*

**Method.** `py/c6_prelead.py`. Frozen fold models (no retraining). Beats from 60 to 15 min before each ST-episode onset, only where no other ST/T episode overlaps the hour before (57 episodes qualify; 73,114 such beats); compared with ordinary negatives of the same test patients not in any such window (95,622 beats). Statistic = mean over folds of per-fold AUROC; subject bootstrap 2,000.

**Result** (`results/c6_prelead.csv`): R0 0.456 (0.363-0.585), R1 0.438 (0.391-0.504), M1 0.542 (0.413-0.655), M2 seeds 0.464 / 0.502 / 0.487 (ranges all include 0.5).

**Outcome: every range includes 0.5, so "no separation shown".** This is not a lead-time or prediction claim, and no such claim may be made from it.

---

## 7b. C7 follow-up: "pretrain + calibrate to the person as you go" (EDB). *Replayed.*

**Why.** To test whether pretraining plus on-device per-person calibration could fix the patient-wise failure. Settings and the pass rule were frozen in `configs/c7_frozen.json` before any scoring (committed before the run). Same folds, labels, 1 % operating-point rule, persistence rule and bootstrap as C2; the C2 numbers above are unchanged.

**Method.** `py/c7_prep.py`, `c7_train.py`, `c7_score_eval.py`. Calibration = a causal, label-free running **median over the previous 10 minutes of that person's own beats** (needs >= 30 beats; current beat excluded). A1: frozen C2 network, its score minus its own running median. A2: frozen network, its 16 pooled features minus their running median, then the frozen final layer. A3 (**primary**): the same tiny network **retrained on residual windows** (window minus the person's running-median window, int8), 3 seeds, same recipe. M1c: the six-feature model fed (features minus running median). **Pass rule (fixed in advance):** calibration adds value only if the lower end of the 95 % subject-bootstrap range of (A3 sensitivity at 1 % FPR minus R1) is above 0.

**Result** (`results/c7_bootstrap.csv`, `c7_beat_metrics.csv`, `c7_episode_metrics.csv`):

| Quantity (sensitivity at 1 % FPR, pooled) | point | 95 % range |
|---|---:|---:|
| R1 personal-baseline ST rule | 0.120 | 0.081-0.204 |
| M2 frozen (3 seeds) | 0.090 | 0.069-0.223 |
| A1 score-level calibration | 0.066 | 0.050-0.114 |
| A2 feature-level calibration | 0.065 | 0.050-0.114 |
| **A3 retrained on residual windows (seeds 0/1/2: 0.122 / 0.108 / 0.066)** | **0.099** | 0.073-0.186 |
| M1c (six features + calibration) | 0.077 | 0.057-0.123 |
| **PRIMARY: A3 - R1** | **-0.021** | **-0.058 to +0.025** |
| A3 - M2 frozen | +0.009 | -0.079 to +0.053 |
| A1 - R1 / A2 - R1 | -0.054 / -0.054 | -0.111 to -0.014 |
| M1c - M1 (calibration hurt the six-feature model) | -0.155 | -0.313 to -0.085 |

**Pass rule outcome: the lower end (-0.058) is not above 0, so "no added value shown" at the pre-written metric.**

**But the full ranking improved a lot (descriptive, not a pre-written test).** Per-fold AUROC on unseen patients, folds 0-4: M2 frozen 0.389 / 0.702 / 0.564 / 0.800 / 0.747 (mean 0.640); R1 0.617 / 0.765 / 0.724 / 0.737 / 0.785 (mean 0.726); **A3 seed 0 0.701 / 0.840 / 0.794 / 0.825 / 0.867 (mean 0.805)**; seeds 1 and 2 similar (0.64-0.86). A3 also no longer falls below 0.5 on fold 0 (0.64-0.70), and its validation AUPRC was higher than the uncalibrated network's on every fold. Score-only or feature-only calibration (A1, A2) did not help (AUROC 0.54-0.59). Episode level (24 of 30 rule, 31.0 episode-free hours): A3 caught 66 / 79 / 55 of 364 (18 / 22 / 15 %) with 20 / 12 / 19 false alerts; R1 caught 73 (20 %) with 1 false alert; A2 seed 0 caught 73 with 7 false; the other methods are in the CSV. Note: C7 recomputes every method's threshold on the same scored validation set, so the re-listed M2 episode counts differ from section 3 (e.g. seed 0: 36 vs 24 caught), which shows how unstable single-threshold episode counts are.

**What it shows.** Calibration has to be built into the *training* (A3 learns from "difference from this person's normal"); bolting it on afterwards (A1, A2, M1c) did not work. With that built in, the tiny network ranks beats on new people clearly better than before and better than R1 on 4 of 5 folds, yet at the deployable operating point (1 % false-positive rate) it still does not beat the simple personal-baseline rule with any confidence.

**What it does NOT show.** The AUROC gain is a single pass over five folds with no bootstrap; it may be partly the network measuring ST better (circular labels); episode catches stay low (about 20 %); the baseline here is a 10-minute running median that would also absorb a slow real change in an ischemic person (not tested); the on-chip cost of keeping a rolling median window is not estimated. No lead time, no detection claim.

---

## 8. Assumptions
A1. EDB subjects = records with identical age/sex/diagnosis header comments (79 groups, equals the published 79).
A2. ST-episode labels come from `(STn` / `STn)` auxiliary notes; episodes counted per marker (364 total, ST1/ST2 overlapping markers counted separately); the older drift evaluation merges overlaps (247).
A3. Channel 0 only; its lead differs by record (V5, MLIII, V4, V2, V1, V3, D3). Channel 1 not run.
A4. The planned `>> 8` input shift was used unchanged; no architecture change from Appendix A (padding convention fixed as 'TF same': conv1 (3,3), conv2 (2,2), conv3 (0,1); float input = int8 / 16).
A5. A beat is "scored" only if it is at least 60 s into the record and R1 has at least 30 eligible beats of history; the M1/M2 validation thresholds were computed on all scored label-0/1 beats of the validation fold (including the few without R1 history).
A6. Pooled AUROC/AUPRC concatenate raw scores of five different models; sensitivity at 1 % FPR is per-fold (threshold from each test fold's own negatives) and pooled by counts.
A7. Bootstrap for M2 = mean of the three seeds' statistics; the "better rule" (R0) was chosen by point estimate.
A8. Episode alert rule: rising edge of 24-of-30 over eligible beats; the 15 and 60 beat rows use the same 80 % ratio (12/15, 48/60).
A9. False-alert time = record duration - 60 s - union of (episode +- 30 min).
A10. The beat window baseline is the pair-averaged window minus the mean of 250 Hz samples R-18..R-11.
A11. PTB-XL uses a causal high-pass for the CNN windows but A3's zero-phase filter for the comparator features.
A12. QAT (fallback b) ran 3 epochs at lr 1e-4 with activation scales fixed from the float calibration.
A13. The Verilog block uses combinational-read arrays (simulation oriented); no synthesis was run.
A14. 'Parallel equals serial' checked on C1 (record e0103: identical windows and features) and on one C2 training job (fold 4, seed 2: identical validation AUPRC and threshold). C4 is integer-exact by construction.

## 9. Regression
Start (`results/round3_regression_start.txt`) and end (`results/round3_regression_end.txt`) are identical: 22/22, 20/20, 35/35; mutation A 19 passed / 16 failed; mutation B 34 passed / 1 failed. No file was edited in `rtl/`, `model/`, `tb/` or `run_vivado.bat` by this round; their pre-existing git changes are listed in section 1.

## 10. Files
Scripts: `py/c0_dossier_arithmetic.py`, `c1_lib.py`, `c1_make_split.py`, `c1_edb_windows.py`, `edge_nets.py`, `c2_train.py`, `c2_score.py`, `c2_eval.py`, `c2_leakage.py`, `c2_secondary_detector.py`, `c2_figs.py`, `edge_int_model.py`, `c3_quantize.py`, `c3_freeze.py`, `c4_make_vectors.py`, `c4_run.py`, `c5_windows.py`, `c5_ptbxl_cnn.py`, `c6_prelead.py`. Verilog: `rtl_edge/rtl/edge_cnn_beat.sv`, `rtl_edge/tb/tb_edge_cnn.sv`, vectors, `rtl_edge/weights/*.mem`, `run_edge_vivado.bat`. Split/configs: `splits/c1_edb_split.json`, `configs/c2_frozen.json`, `c3_quant_frozen.json`, `c5_frozen.json`. Results: `results/c0_*`, `c1_*`, `c2_*` (beat metrics, bootstrap, episode metrics, failure analysis, leakage, secondary detector, train log, thresholds), `c3_*`, `c4_*`, `c5_ptbxl_*`, `c6_prelead.csv`, `round3_regression_*.txt`, figures `fig_c0_edb_check`, `fig_c2_roc_pr`, `fig_c2_episode`, `fig_c2_leakage`, `fig_c3_int8`, `fig_c4_cycles`, `fig_c5_ptbxl` (.png). C7 follow-up: `py/c7_*.py`, `configs/c7_frozen.json`, `results/c7_*`, `fig_c7_calibration.png`. Intermediate data (windows, scores, models) are under `data/edge/` (not committed).
