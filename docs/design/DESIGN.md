# System Design

This document records the design intent for the two-node wearable. No hardware has been built. What has been tested is described in the [reports](../reports/README.md).

## Architecture

| Node | Position | Controller | Sensors and outputs |
|---|---|---|---|
| Sentry Pod | Lower breastbone | nRF5340 | ADS1292R (ECG, bio-impedance), LSM6DSOX (chest vibration, motion, falls), SPH0645 microphone, TMP117 temperature, siren |
| PulseBand | Wrist | nRF52840 | MAX86141 optical pulse, skin conductance pads, screen, vibration motor, cancel button |
| Phone app | Wearer's smartphone | | Bluetooth Low Energy gateway, call and text to 112 with location |

## Design decisions

| Topic | Decision | Reason | Status |
|---|---|---|---|
| Form factor | A pod worn by clip, soft neck cord or optional adhesive dock | Lets the wearer choose comfort or firm skin contact | Proposed |
| Sensing sites | Chest and wrist | Each site can cross-check the other | Logic simulated |
| Alert tiers | Baseline drift gives a check-in only; an emergency needs lost wrist pulse and a still chest | Limits unnecessary calls | Logic simulated |
| Controller | nRF5340 on the pod, nRF52840 on the band | Bluetooth Low Energy and signal-processing instructions in low-power parts | Proposed |
| Connectivity | Phone as the gateway, with no cellular modem in the wearable | Smaller, lower power, no separate subscription | Modelled in simulation |
| Motion noise | Adaptive (NLMS) filter, with a wavelet stage planned | Removes walking noise from chest vibration | Adaptive filter simulated; wavelet stage not built |
| On-device learning | A small model with a personal baseline | Hearts differ between people | A small stand-in was tested on public data; the full model is not built |
| False-alarm cancel | Physical button held for 2 s within a 30 s window, locked after a detected fall | Usable without looking at a screen | Logic simulated |
| Escalation | Call and text, then siren and a 110 BPM CPR beat | Gets help and guides bystanders | Logic simulated |
| Power | 150 mAh pod cell, 220-250 mAh band cell | The optical sensor draws most on the wrist | About 4.3 and 3.4 days, calculated and not measured |

## Open questions

* Whether the chest-still hold before the countdown is 3 s or 10 s.
* The choice of ECG front end and the number and material of electrodes.
* Whether the wristband needs its own motion sensor.
* A "no heartbeat" check that does not rely on ECG beats alone.
