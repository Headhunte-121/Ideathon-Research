# Sentry virtual device (Vivado simulation)

The Sentry's logic written as hardware (Verilog) and tested in simulation. No sensors, battery or body:
it shows the design logic is wired correctly and behaves as intended.

## What is what

### rtl/  (the design, one block per file)
| File | What it is | Where it sits in the chain |
|---|---|---|
| motion_noise_canceller.sv | 16-tap adaptive filter that removes walking noise from the chest vibration signal | step 1 |
| ecg_beat_detector.sv | finds heartbeats in the ECG and gives heart rate for each beat | step 2 |
| signal_summary_1s.sv | once a second: wrist pulse size, chest heartbeat strength, body motion level | step 3 |
| baseline_drift_detector.sv | learns the wearer's normal heart rate, flags SUSTAINED change (check-in only) | step 4 |
| alarm_state_machine.sv | monitor / check-in / 30 s cancel window / call / siren + 110 BPM CPR beat | step 5 |
| **sentry_full_device_top.sv** | **the whole device: steps 1 to 5 wired together, takes raw sensor samples** | top for the end-to-end test |
| decision_chain_top.sv | steps 4 and 5 only, takes ready-made summary values | top for the quick logic test |

### tb/  (the tests, in the order I suggest you run them)
| File (top module name) | What it tests | Time |
|---|---|---|
| **tb_full_device.sv** | **END TO END. Fake sensors (ECG, chest vibration, wrist PPG, motion) feed the whole device. 7 scenarios, 20 checks: arrest timeline, cancel, drift, walking, loose watch, lifted electrode.** | about 1 min |
| tb_decision_logic.sv | state machine + drift detector only, 10 scenarios, 22 checks, easy-to-read waveforms | seconds |
| tb_drift_false_alarms.sv | how many false check-ins per 24 h at 3.0 / 3.8 / 4.5 sigma, and detection delay. Synthetic data, or real PhysioNet data | seconds |
| tb_noise_canceller.sv | SNR gain of the walking-noise filter on a synthetic signal | seconds |

### py/  (helper scripts, run on your PC)
| File | What it does |
|---|---|
| download_physionet_heart_rate.py | downloads a real 24 h heart recording from PhysioNet, writes data/hr_<id>.hex for tb_drift_false_alarms |
| check_noise_canceller_vs_float.py | compares the hardware filter output with a floating-point filter |

### results/  (logs from my own run)
full_device_test_log.txt, decision_logic_test_log.txt, drift_false_alarms_log.txt, noise_canceller_log.txt,
noise_canceller_vs_float_log.txt, noise_canceller_output.csv

## Run in Vivado (GUI)
1. File > Project > New. RTL project, any part (xc7a35tcpg236-1 is fine). No constraints.
2. Add design sources: every file in rtl/.
3. Add simulation sources: every file in tb/.
4. Settings > Simulation > Simulation top module name: tb_full_device (change it to run another test).
5. Run Simulation > Run Behavioral Simulation, then in the Tcl console type: run all
   PASS/FAIL lines appear in the Tcl console. For the poster screenshot, add to the Wave window:
   dut_g/state_o, dut_g/ppg_pp, dut_g/scg_energy, dut_g/hr_q4, dut_g/siren_en, dut_g/cpr_beat, ecg, ppg, scg
   and zoom to the arrest in scenario E3.
6. tb_noise_canceller writes results/noise_canceller_output.csv in the simulation folder: first create a folder named
   results inside <project>.sim/sim_1/behav/xsim.
7. tb_drift_false_alarms on real data: Settings > Simulation > xsim.simulate > More Options:
   -testplusarg HRFILE=C:/full/path/data/hr_16265.hex -testplusarg NBEATS=<number printed by the python script>
   For a heart-rate shift test add -testplusarg INJECT=1 -testplusarg PCT=25

## Run from a terminal (Vivado command prompt, in this folder)
    xvlog -sv rtl/*.sv tb/tb_full_device.sv
    xelab tb_full_device -s full && xsim full -runall
(Same pattern for the other tests: replace tb_full_device with the test name.)

## Real data (needs internet on your PC)
    pip install wfdb numpy
    python py/download_physionet_heart_rate.py 16265
Repeat for other MIT-BIH Normal Sinus Rhythm records (16272, 16273, 16420, ...).

## Honest limits (put these on the poster)
- The sensor signals in tb_full_device are waveforms WE wrote (simple models of ECG, chest vibration, wrist PPG,
  walking motion). The test shows the chain is wired and behaves correctly, not that real sensors look like this.
- In tb_full_device the noise canceller is in the path but the checks would also pass without it. Its benefit is
  measured in tb_noise_canceller on synthetic noise only, and that gain is optimistic.
- Walking at 105 bpm gives a false check-in unless the rest-only gate is on (scenario E1 shows both).
- Thresholds (pulse size, chest strength, motion level, 3.8 sigma, 3 s hold, 30 s window) are placeholders.
- Nothing here says the device detects ischemia. It shows the alarm logic is sound and the timing is right.
- I ran everything in Icarus Verilog, not xsim. If xsim complains about a line, send me the message.
