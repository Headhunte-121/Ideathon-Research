# Evidence summary for the poster's evidence table (paste-ready; label: "Replayed on public recordings")

1. Alarm logic simulated in Verilog (Vivado xsim): 77 self-checking tests pass (22 + 20 + 35); deliberately broken versions are caught.
2. Replayed on real recordings of 18 + 2 + 20 + 15 people (PhysioNet NSRDB, NSTDB, CEBS; PPG-DaLiA). No arrest or ischemia data exists for this sensor set, so arrest detection remains simulated.
3. Heartbeat detector, clean real ECG (18 people, 30 min each): 99.95 % of beats found, 99.64 % correct detections.
4. Heartbeat detector in heavy real motion/muscle noise: falls to 57-62 % found and 45-48 % correct at -6 dB (re-tested at a smaller scale: the loss is the detector's, not clipping).
5. Chest vibration of 20 resting volunteers (CEBS): never dropped below the "no heartbeat" threshold in any second (weakest person 2.5x above it; sensor scale from datasheet, assumed).
6. Resting-heart-rate drift detector, about 382 hours of real heart rate: 1 false check-in in total at the sensitive setting, none at the others.
7. BUT the same detector missed a sustained +15 % heart-rate rise in all 18 people: low false alarms came with very low sensitivity; fix proposed (resting-only heart rate), not yet tested.
8. In 36 person-hours of living people in daily life (PPG-DaLiA), wrist pulse loss with a still chest lasted at least 3 s on 13 occasions (2 of 15 people, mostly one person at lunch): the chest heartbeat check must be what prevents a false dispatch there; untested outside lying down.
9. Cancel window, phone call, siren and CPR beat were exercised only in simulation, not on real data.
10. Not claimed: validated, clinically tested, or any sensitivity or specificity for arrest or ischemia. Data licences: PhysioNet sets ODC Attribution 1.0; PPG-DaLiA CC BY 4.0.
