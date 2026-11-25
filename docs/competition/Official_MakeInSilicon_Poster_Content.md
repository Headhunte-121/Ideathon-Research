# MakeInSilicon 2026: Poster Content
## Track 1: Smart Innovation in AI with Embedded Platforms (Smart Healthcare Systems)

> **Event**: MakeInSilicon, International Symposium on Enabling Indigenous Semiconductor Infrastructure, 13-15 November 2026  
> **Host**: Dr. SPM International Institute of Information Technology (IIIT) Naya Raipur  
> **Template**: five organiser sections (Abstract, Novelty, Implementation, Working Modeling, Social Impact), 3:4 portrait  

**Tags used on the poster:** **NOW** = ran in simulation or on public recordings. **NEXT** = designed from datasheets, to be built and measured. **FUTURE** = needs patients, hospitals and approvals.

---

## Title block

**AUTONOMOUS STERNAL SENTRY**  
A two-node wearable concept for cardiac emergency alerting

---

## 1. Abstract

Use the 100-word version in the [competition abstract](Official_Competition_Abstract.md).

## 2. Novelty

* **Two body locations cross-check each other.** An emergency needs the wrist pulse lost *and* no heartbeat vibration at the chest.
* **A slow change never calls anyone.** Drift from the wearer's own baseline gives a haptic check-in only.
* **The wearer stays in control.** A 30-second cancel window with a physical button, locked out after a detected fall.
* **Help for bystanders.** Siren and a 110 BPM CPR beat.

## 3. Implementation (NEXT: designed, not yet built)

| Node | Controller | Parts |
|---|---|---|
| Sentry Pod (breastbone) | nRF5340 | ADS1292R (ECG and bio-impedance), LSM6DSOX (motion and chest vibration), SPH0645 microphone, TMP117 temperature, siren |
| PulseBand (wrist) | nRF52840 | MAX86141 optical pulse, skin conductance pads, screen, vibration motor, cancel button |
| Phone app | Smartphone | Bluetooth Low Energy gateway, call and text to 112 with location |

Battery design estimate (calculated from datasheet currents, not measured): pod 150 mAh, about 4.3 days; band 240 mAh, about 3.4 days.

## 4. Working modeling (NOW)

**Signal path:** chest motion → noise canceller → heartbeat vibration strength; ECG → beat detector → drift detector; wrist PPG → pulse size; all feed the alarm state machine.

**Alarm path:** Monitor → (pulse lost and chest still for 3 s) → 30 s cancel window → call and text → siren and CPR beat. Hold and thresholds are initial values.

| Result | Evidence |
|---|---|
| 77 self-checking tests pass (22 + 20 + 35); broken versions are caught | Simulated |
| Beat detector: 99.95 % sensitivity, 99.64 % positive predictivity on clean ECG, 18 people | Replayed (NSRDB) |
| Chest vibration of 20 resting volunteers stayed above the "no heartbeat" threshold (sensor scale assumed) | Replayed (CEBS) |
| An ECG check or a 10 s hold removed all 13 false countdown starts in 17.9 h of daily life | Replayed (PPG-DaLiA) |
| 8-bit network (1,538 parameters, 43,144 multiply-adds per beat) matches the software model on 2,064 of 2,064 inputs in Verilog, 44,962 cycles per beat | Simulated |

**What the next design addresses:** heavy motion noise; a "no heartbeat" check that does not rely on ECG alone; warning signals beyond heart rate; building personalisation into the learned model.

## 5. Social impact (FUTURE)

* **Goal:** shorten the time between a collapse and the first call for help, including for people who are alone.
* **Accessibility:** uses the wearer's own phone; no separate mobile subscription in the device.
* **Path:** bench prototype → measured noise and battery life → supervised data collection with a clinical partner → regulatory review.

**Footer line:** Research prototype. Not a medical device. Detection or prediction of heart attack or cardiac arrest has not been demonstrated.

