# Competition Abstract
## Autonomous Sternal Sentry: a two-node wearable concept for cardiac emergency alerting

> **Event**: MakeInSilicon 2026 Ideathon, Track 1: Smart Innovation in AI with Embedded Platforms (Smart Healthcare Systems)  
> **Stage**: Concept and simulation prototype  

---

## 100-word version

> When the heart stops, the wearer cannot call for help. Autonomous Sternal Sentry is a concept for a chest pod and wristband that check each other before raising an alarm: wrist pulse lost and chest heartbeat still, followed by a 30-second cancel window, an emergency call and CPR guidance. Slow changes from the wearer's baseline only prompt a gentle check-in. The alarm logic passes 77 self-checking Verilog tests in simulation, and its heartbeat detector found 99.95 % of beats in 18 resting people's public recordings. Hardware and clinical evaluation are the next stages.

## Extended version

**Title:** A two-node embedded wearable concept for cardiac emergency alerting using cross-checked chest and wrist sensing

Sudden cardiac arrest leaves little time and often leaves the wearer unable to act. A single wrist sensor can also mistake a loose strap or movement for a lost pulse. We propose a two-node wearable: a Sentry Pod on the breastbone (ECG, chest vibration, breathing, temperature and sound) and a PulseBand on the wrist (optical pulse, skin conductance and a cancel button), linked by Bluetooth Low Energy to a phone app.

The design follows two rules. Sustained drift from the wearer's own baseline only produces a haptic check-in. An emergency requires agreement between both nodes (wrist pulse lost and no chest heartbeat vibration), followed by a 30-second cancel window, a call and text to 112, and a siren with a 110 BPM CPR beat.

We implemented the signal chain and alarm logic in Verilog and tested them against our own simulated patient, sensor chips, radio link and phone: 22, 20 and 35 self-checking tests pass, and deliberately broken versions are caught. On public recordings, the heartbeat detector reached 99.95 % sensitivity and 99.64 % positive predictivity on clean ECG from 18 people. Replays also identified what the next design must improve: robustness in heavy noise, a "no heartbeat" check that does not rely on ECG alone, and warning signals beyond heart rate. A small 8-bit neural network was reproduced bit for bit in a stand-alone Verilog block; it did not yet outperform simple rules.

No hardware has been built, and detection or prediction of heart attack or cardiac arrest has not been demonstrated. The next stages are bench prototypes with measured noise and battery life, followed by supervised data collection with a clinical partner.

---

Related: [poster content](Official_MakeInSilicon_Poster_Content.md) · [system design](../design/DESIGN.md)
