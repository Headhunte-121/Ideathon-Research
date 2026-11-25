# Poster lines from the tweaks round (label: "Replayed on public recordings"; tuned and tested on different people)

1. Daily-life false starts of the 30 s countdown (pulse lost + still chest, 36 person-hours, 15 people): 13 in the 8 tuning people (2 people, 0.70 per person-hour), 0 in the 7 test people. Requiring "no chest-ECG beat for 3 s" removed all 13 at no time cost; a 10 s hold also removed all 13 at a cost of 7 s of dispatch delay. The test people had no false starts either way, so the fix is confirmed only on the tuning people.
2. Trade-off to state: the ECG-beat condition would block the countdown in pulseless electrical activity (PEA); the longer hold does not.
3. Wrist-still check alone barely helped (0.70 to 0.48 per person-hour).
4. Resting heart-rate warning: heart rate at rest (chest still) is about 29 % (median) higher while working than while sitting, so one resting baseline false-alarms 2-4 times per resting hour. With a baseline learned in the same context (uses an activity label the device does not have) it gave 0 false alarms and caught a +25 % rise in 5 of 7 test people (+15 %: 2 of 7), after about 5-6 minutes.
5. Heavy-noise beat detection (0 to -6 dB): not caused by signal clipping (re-tested at a smaller scale, no improvement); rejecting too-early beats did not help either.
6. Fixed "chest still" threshold fails to recognise a chest with no heartbeat once sensor noise reaches about 0.8 mg RMS (simulated); an adaptive threshold recognised it at every noise level tested, at the cost of calling living people still when noise reaches about 1 mg or more. The chip's real noise figure was not verified.
7. A 1 g gravity offset would hide a missing heartbeat completely without a 1 Hz high-pass; with it the result is unchanged.
8. Not claimed: validated, clinically tested, any sensitivity or specificity for arrest or ischemia.
