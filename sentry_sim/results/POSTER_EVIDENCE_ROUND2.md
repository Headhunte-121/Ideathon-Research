# Poster wording from round 2 (copy only accepted lines; full context in REAL_DATA_REPORT_2.md)

## May say

| Result | Exact wording | Label |
|---|---|---|
| B3 | In 17.9 person-hours of living people (7 test people), wrist pulse loss with a quiet chest held for 3 s occurred 13 times (2 people); an ECG-beat veto removed all 13 and a 10 s hold removed them at the default threshold (7 s slower). The veto would also suppress pulseless electrical activity. Not an independent test. | Replayed (PPG-DaLiA) |
| B2 | The beat detector misses about 20% (0 dB) to 40% (-6 dB) of beats in heavy real noise and 40-55% of its detections are wrong; this is not an ADC-scaling artefact. | Replayed (NSTDB, 2 records) |
| B4 | Feeding only resting beats to the unchanged drift detector did not let it detect +10 to +25% heart-rate steps in 7 people (about 2 h each). | Replayed + Simulated step (PPG-DaLiA) |
| A1 | A heart-rate drift check (tuned on 40 patients, tested on 40 other patients, 43 records) caught 8 of 178 ischemic ST episodes at 1.07 false check-ins per 24 h; catching most episodes costs tens of false check-ins per day. Most episodes follow heart-rate rises. | Replayed (LTSTDB) |
| A2 | The same setting, unchanged, caught 3.8% of ST-change episodes in 75 two-hour recordings of a second database (15 overlapping records excluded); the false-alarm rate is too uncertain to quote. | Replayed (EDB) |
| A3 | On 10-second resting 12-lead ECGs (test fold 10, 1462 ECGs), ST level and slope alone give an AUC of 0.59 to 0.77 for MI vs normal depending on the lead; five simple features give 0.71 to 0.86. Not early warning, not wearable. | Replayed (PTB-XL, Python) |
| A4 | On real recordings of ventricular fibrillation (10 test records) the beat detector kept finding beats in the fibrillation waves, so a 6 s 'no beat' rule fired within 5 minutes in only 5 of 10 records. ECG only; not representative of our device. | Replayed (SDDB, Verilog on windows) |
| B5 | A fixed 'chest still' threshold stops recognising a chest with no heartbeat once simulated sensor noise reaches about 0.65-0.8 mg RMS; the real chip's noise was not verified. | Simulated (end-to-end testbench) |
| B5 | In the simulator a fixed 'chest still' threshold fails to recognise a chest with no heartbeat once sensor noise reaches about 0.65-0.8 mg RMS. An adaptive threshold that fixes this in the simulator would call 95% of real resting seconds 'still' (emulated on 40 recordings), so it is not adopted. | Simulated + Replayed emulation (CEBS) |

## Must not say

| Do not write | Why |
|---|---|
| "validated", "clinically tested", "proven" | Nothing here is a clinical test of the device or of the combined sensor set |
| "detects heart attacks / ischemia / arrest", any sensitivity or specificity for them, any lead time as a capability | No recording has our sensors during a heart attack; the A1 "lead times" are check-ins that follow heart-rate changes, not predictions |
| "ECG-beat check catches ventricular fibrillation" | A4: the detector keeps finding beats during real VF (half the onsets never triggered the no-beat rule in 5 minutes) |
| "heart-rate drift detects ischemia" | A1: it caught 4.5% of episodes at about 1 false alarm per day; catching more costs tens of false alarms per day |
| "ST level detects a heart attack" | A3: ST alone is weak; it is a resting diagnostic ECG, not a wearable or sternal lead |
| "adaptive threshold fixes the sensor-noise problem" | B5: not shown; the chip's real noise figure is unverified |
| the ECG-veto's zero false arms as a result without the PEA caveat | The veto would also block the countdown in pulseless electrical activity (PEA); DaLiA cannot test that |
| any number from the tune sets as a result | Only test-set numbers are results; tune-set numbers are in separate tables |
