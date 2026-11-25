# Tweaks report: five changes tried after the real-data replay

Built by `py/build_tweaks_report.py` from the CSVs in `results/` (files starting `tweak`). **The original results are untouched** (`results/REAL_DATA_REPORT.md` and its CSVs); every number below is a new run, and "before" is quoted next to "after". No RTL file was changed: tweaks 1, 2, 4 and 5 are Python models of a proposed change, and tweak 3 re-ran the unchanged RTL with different input scaling. Nothing here says anything about detecting cardiac arrest or ischemia.

Evidence labels: **Replayed** = run on public recordings; **Simulated** = something added to a real recording (a step in heart rate, extra sensor noise, a no-heartbeat signal); **Assumed** = a value without a source.

## 0. Rules followed

- **Tune on some people, test on others.** PPG-DaLiA people S1-S8 = tune, S9-S15 = test (fixed before looking at any result). NSTDB record 118 = tune, record 119 and the 18 clean NSRDB people = test. Selections were made on the tune people only.
- **Before and after side by side**, with the people used named.
- **Judged by false starts (or false alarms) per person-hour, with detection delay as the cost.**
- Poster wording for any improved number: *"tuned on 8 people, tested on 7 other people, public recordings"*. Still no claim about arrest or ischemia.

## 1. Verdict in one table

| # | Tweak | Result | Safe to put on the poster as |
|---|---|---|---|
| 1 | Stop living people starting the countdown | A longer hold or an "ECG shows no beats" condition removes all 13 false starts; "wrist is still" alone barely helps. **The test people never had a false start, so the test group cannot confirm the fix** (section 2). | "13 false starts in 18.7 person-hours on 8 people; none after the change; the other 7 people had none either way" |
| 2 | Resting-only drift warning | Works only when the baseline is learned in the **same context** (working), which the device cannot know. With one pooled resting baseline it false-alarms 2-4 times per resting hour. | "Resting-only warning is an open problem: heart rate at rest differs by about 29 % (median) between sitting and working" |
| 3 | Beat detector at a smaller scale | **The clipping explanation was wrong.** Less clipping did not help; the loss in heavy noise is the detector's. | "Beat detector misses about 20 % (0 dB) to 40 % (-6 dB) of beats in heavy noise and 40-55 % of its detections are wrong; not a scaling artefact" |
| 4 | Adaptive "chest still" threshold | Fixes the fixed threshold's failure for sensor noise of about 0.7-1 mg RMS and above; costs wrong "still" calls in living people only when noise is about 1 mg or more. 1 g gravity needs the high-pass. | "Adaptive threshold simulated; real chip noise not verified" |
| 5 | Reject too-early beats | **Not adopted**: a small PPV gain for a larger sensitivity loss. | nothing |

## 2. Tweak 1: stopping false starts (PPG-DaLiA, Replayed; 15 people, 36.0 person-hours)

A **false start** = at least H seconds in a row in which, for a living person, the wrist pulse is lost AND the chest is not moving (E5 definitions) AND, depending on the rule, the wrist is still (wrist accelerometer variation at most X times that person's own sitting median) AND the chest ECG has had no beat for 3 s (beats found by the Python port of `rtl/ecg_beat_detector.sv`, py/beat_model.py). Cost in a real arrest: dispatch happens H seconds after onset (baseline H = 3 s), because all conditions are true together from the first second.

<<T1>>

**Selected on the tune people only:** hold 3 s + "no ECG beat for 3 s" (added delay 0 s): 0 false starts in the tune people and 0 in the test people.

What the table tells:
- **Before** (the E5 rule, hold 3 s): 13 false starts in S1-S8 (11 from S8 at lunch, 2 from S5 in an activity transition), 0 in S9-S15.
- **The test people had no false starts to remove.** "0 before, 0 after" on S9-S15 only shows that the new conditions did not add any; it is **not** evidence that they fix anything. All of the evidence for the fix is in the 8 tune people, and it comes from only two of them.
- **Hold longer:** 5 s leaves 0.27 per person-hour on the tune people; **10 s removes all 13** (the longest false run was 8 s) at a cost of 7 s of dispatch delay.
- **Wrist still:** only reduces 0.70 to 0.48 per person-hour at the strictest setting (3x); person 8's wrist was mostly still while the pulse signal dropped.
- **ECG no-beat:** in the 36 person-hours of living people the longest gap between detected chest-ECG beats was 4.4 s, and gaps of 3 s or more covered under 0.04 % of seconds (`results/tweak1_ecg_gap_living.csv`). This is the strongest guard and costs no time.
- **The trade-off the poster must state:** the ECG condition assumes an arrest shows *no electrical beats*. In pulseless electrical activity (PEA) the heart still produces electrical activity but no pulse, so this condition would **block** the countdown for those arrests. A longer hold has no such blind spot but is slower. This is a decision for the team, not something the data decides.
- Limits: 15 healthy adults, one wrist device, activity labels from the dataset; the ECG detector port agrees with the Verilog's scores within 0.12 points on clean ECG (py/beat_model.py), but ECG under real chest motion was only tested on these 15 people.

## 3. Tweak 2: resting heart-rate drift warning (PPG-DaLiA, Replayed + Simulated step)

Resting = chest not moving and (POOLED) activity sitting or working, or (WORKING) working only. Heart rate per beat from the dataset's R-peaks. A step of +10, +15 or +25 % (Simulated) is added over the last 10 (POOLED) or 8 (WORKING) resting minutes; false alarms are counted without it. PLAIN rule: 60 s mean resting HR above (1+T) x the person's own baseline for 5 minutes in a row. SIGMA: the Verilog detector's logic on the resting beats only. Detection counts only people who were not already alarming just before the step (the denominator shown).

<<T2>>

**Why the pooled version fails:** heart rate while sitting and while working (both "chest still") differs a lot (`results/tweak2_context_hr.csv`): working is 9 to 48 % above sitting, median about 29 %, so a baseline learned while sitting is the wrong reference for the rest of the day and the PLAIN rule alarms 2-4 times per resting hour in nearly everybody. The SIGMA rule stays quiet only because it is nearly blind (0 of 7 detections at +25 % on the tune people).
**With a baseline learned in the same context** (WORKING, an upper bound because it uses an activity label the device does not have): selected on the tune people, "+10 % for 5 min" gave 0 false alarms in both groups; on the 7 test people it caught +25 % in 5, +15 % in 2 and +10 % in 1, after about 5-6 minutes. The "+20 %" rule the plan suggested gives 0 false alarms but catches +25 % in only 2 of 7 test people.
**What this means:** the resting-only idea is only as good as the device's ability to know which resting context it is in. Untested ideas: use the Pod's posture or the time of day, or learn the baseline only from long still periods (sleep). Not done: separate baselines for rest and activity (activity heart rate is not the target of the warning and DaLiA has about 30 resting minutes per person, too little for a second baseline).

## 4. Tweak 3: beat detector at a smaller ECG scale (NSTDB, Replayed on the unchanged RTL)

The plan said part of the heavy-noise loss was my 16 codes/uV scaling clipping the signal. The same 12 NSTDB recordings were replayed at 16 (as before), 8 and 4 codes/uV through the unchanged `rtl/ecg_beat_detector.sv`, with the detector's `MIN_THR` floor kept at the same microvolts (1500, 750, 375). Noisy minutes only; mean of records 118 and 119. The 16 codes/uV rows reproduce the original E1 numbers exactly.

<<T3>>

- Clipping did go down (19 % of samples at -6 dB with scale 16, 1.5 % at scale 4), but **sensitivity did not improve**: at 0 dB it fell from 80 % to 71 % and at -6 dB from 60 % to 55 %; PPV moved by 0.4-3 points, slightly down. Scale 8 sits in between with no clear gain.
- So **the earlier statement that the low-SNR loss was partly my scaling is not supported by this test** and has been corrected in `results/REAL_DATA_REPORT.md` and `results/POSTER_EVIDENCE_SUMMARY.md`. (Clipping even limits the size of noise spikes, which may explain the small advantage of the high scale.)
- `MIN_THR` rescaling made no difference at all (identical counts): the floor is not what limits the detector in noise. The loss is the threshold following the noise bursts, as diagnosed in the original report.

## 5. Tweak 4: adaptive "chest still" threshold (CEBS, Replayed + Simulated noise)

Fixed rule (as built): chest still if the per-second mean |a| is below 5 codes. Adaptive proposal: below max(5, 3 x floor), with floor = causal 60 s median of the 40-100 Hz band energy (the heartbeat has no energy there). White sensor noise of RMS sigma is **Simulated**: added to the 40 living CEBS recordings (660 mV/g assumed), and alone as the "no heartbeat" chest. **Real chip noise was not verified**: the LSM6DSOX datasheet could not be opened from this machine, so no noise figure is quoted as cited. As arithmetic only: a noise density of D ug/sqrt(Hz) over a 125 Hz band gives about 11 x D ug RMS, so a density of 60-90 gives 0.7-1.0 mg, right where the fixed rule breaks. **Check the datasheet.**

<<T4>>

- **Fixed rule:** a living person is never called still at any noise level (adding noise only adds energy), but a chest with **no heartbeat is recognised only while noise stays below about 650 ug RMS**: 99.9 % at 650, **20.9 % at 800, 0 % at 1000 and above.** (This matches the earlier end-to-end simulation, where arrest scenarios started failing at 650 ug.)
- **Adaptive rule:** a no-heartbeat chest is recognised 100 % at every noise level tested. Cost: living people start to be called still at high noise: 0.01 % at 650, 0.03 % at 800 (worst person 0.7 %), **0.48 % at 1000 (worst person 12 %), 59 % at 2000** (the heartbeat is then smaller than the threshold; nothing could work at that noise).
- **Gravity** (`results/tweak4_gravity.csv`): with 1 g of DC added, the per-second chest energy reads 8196 codes without a high-pass (a living or dead person would never look still) and 21.3 codes with a 1 Hz high-pass, identical to the same recordings without gravity. The high-pass is required; the CEBS data was already AC coupled so the Pod's high-pass was not exercised before. Breathing-driven tilt was **not** tested.
- Not done: the RTL change itself. The adaptive rule needs a floor estimate and a comparator in the Pod's chest-activity path; it should be added to the RTL only after the real chip's noise is known, and then `run_vivado.bat` must be re-run.

## 6. Tweak 5: early-beat rejection (NSTDB + NSRDB, Replayed in the Python port, low priority)

Rule: ignore a beat arriving sooner than a fraction of the median of the last 5 RR intervals after the previous beat, unless its slope exceeds a multiple of the threshold. Tuned on NSTDB record 118 (6 noise levels), tested on record 119 and the 18 clean NSRDB people.

<<T5>>

Selection on the tune record (best PPV with at most 1 point of sensitivity lost): **none** (no variant qualified). The variants gain 0.5-3.9 PPV points but lose 1.4-34 sensitivity points (tune 1.4-6.0, test 1.9-33.9); on clean ECG they change nothing. **Not adopted.** As the plan said, the alarm does not depend on this detector, only the heart-rate display and the drift feature do.

## 7. Changes to earlier claims

1. The statement that heavy-noise beat-detection loss was "partly limited by our 16-bit scaling" is **withdrawn** (tweak 3).
2. "Drift detector: low false alarms" still needs the original caveat: it is nearly blind. Resting-only gating alone does not fix it (tweak 2).
3. E5's 13 daily-life false starts: removable, with the ECG-beat trade-off or a 7 s slower dispatch (tweak 1), but the confirming test people had no false starts.

## 8. Files

Scripts: `py/tweak1_features.py`, `py/tweak1_rules.py`, `py/tweak2_resting_drift.py`, `py/tweak3_scale.py` (+ `tb/tb_real_ecg_beats_scaled.sv`), `py/tweak4_adaptive_still.py`, `py/tweak5_early_beat.py`, `py/beat_model.py`, `py/build_tweaks_report.py`. Results: `results/tweak*.csv`, `results/tweak*_selection.txt`, `results/tweak_beat_model_vs_rtl.csv`.
