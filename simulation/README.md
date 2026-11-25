# Simulation

The logic of the Sentry Pod and PulseBand written in Verilog and tested in a simulator, plus Python scripts that replay public recordings. There are no sensors, battery or body: the tests show how the design logic behaves.

## Layout

| Folder | Contents |
|---|---|
| `rtl/` | Design, one block per file |
| `model/` | Behavioural models used only in simulation |
| `tb/` | Self-checking testbenches |
| `rtl_variants/` | Experimental variants used in round 2; the baseline in `rtl/` is unchanged |
| `rtl_edge/` | Stand-alone 8-bit neural network block, testbench, weights and vectors |
| `py/` | Experiments and analysis |
| `configs/`, `splits/` | Frozen settings and patient-wise splits |
| `results/` | Tables and figures |

## Design blocks (`rtl/`)

| File | Role |
|---|---|
| `motion_noise_canceller.sv` | 16-tap adaptive filter that removes walking noise from the chest vibration signal |
| `ecg_beat_detector.sv` | Finds heartbeats in the ECG and reports heart rate |
| `signal_summary_1s.sv` | Per-second wrist pulse size, chest heartbeat strength and motion level |
| `baseline_drift_detector.sv` | Learns the wearer's resting heart rate and flags sustained change (check-in only) |
| `alarm_state_machine.sv` | Monitor, check-in, cancel window, call, siren and CPR beat |
| `signal_chain_top.sv`, `decision_chain_top.sv` | Top levels for the block-level tests |
| `pod_node.sv`, `pod_alarm_fsm.sv`, `band_node.sv` | The two wearable nodes |
| `sentry_device_top.sv` | Both nodes, radio and phone wired together |

Models in `model/` cover the patient's signals, the sensor chips (sample rate, resolution, noise and saturation, without SPI or I2C wiring), the Bluetooth link (delay, jitter and loss) and the phone app.

## Running the tests

All tests, with Vivado xsim, from a Windows Command Prompt in this folder:

```bat
C:\AMDDesignTools\2025.2\Vivado\settings64.bat
run_vivado.bat
```

| Testbench | Checks |
|---|---|
| `tb_decision_logic` | Alarm state machine and drift detector (22 checks) |
| `tb_signal_chain` | Raw sensor samples through the whole chain (20 checks) |
| `tb_system_end_to_end` | Both nodes, radio and phone (35 checks, plus two mutations that must fail) |
| `tb_drift_false_alarms` | False check-ins per day at several sensitivity settings |
| `tb_noise_canceller` | Noise reduction on a synthetic signal |

The end-to-end testbench accepts `+ONLY=n` (one scenario), `-d MUT_A` / `-d MUT_B` (mutations), `BLE_LOSS` (packet loss) and `ACCN` (sensor noise) options.

Neural network block (bit-exact check against the Python integer model):

```bat
run_edge_vivado.bat
```

## Experiments

| Scripts in `py/` | Round | Guide or report |
|---|---|---|
| `real_*`, `e5_episodes.py` | 1: public recordings | [REAL_DATA.md](REAL_DATA.md) |
| `tweak*`, `analyze_drift.py` | Follow-up changes | [Tweaks report](../docs/reports/TWEAKS_REPORT.md) |
| `a1_*` to `a4_*`, `b2_*` to `b5_*` | 2: ischemia and arrest datasets | [Round 2 report](../docs/reports/REAL_DATA_REPORT_2.md) |
| `c1_*` to `c8_*`, `edge_*` | 3: edge AI | [Edge-AI report](../docs/reports/EDGE_AI_REPORT.md) |

Run scripts from this folder, for example `python py/c2_eval.py`.

## Limits

- Sensor signals in the testbenches are waveforms we wrote. Passing tests show the logic is wired and timed as intended, not that real sensors look like this.
- Thresholds (pulse size, chest strength, motion level, drift sensitivity, hold and cancel times) are placeholders.
- Not modelled: sensor bus timing, firmware and microcontroller timing, the radio layer, power supply, audio and a real phone.
- Nothing here shows that the device detects ischemia or cardiac arrest in people.
