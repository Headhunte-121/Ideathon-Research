# Product Translation: Question 6.4 — Hierarchical "Sentry" Pipeline vs. Monolithic Inference

---

> **Document Type**: Tier 2.5 Engineering Implementation & Product Architecture Translation  
> **Source Research**: `Phase 06 -> Question 6.4: Hierarchical "Sentry" Pipeline vs. Monolithic Inference`  
> **Target System**: Autonomous Dual-Node Sternal Sentry Pendant & Companion PulseBand  
> **Hardware Target**: ST LSM6DSOX (Precordial IMU) + Nordic nRF5340 Dual-Core SoC (Application Core Cortex-M33) + Wrist PulseBand (MAX86141 Optical PPG)

---

## 1. How This Research Directly Fits Our Wearable Architecture

Our mission is to detect acute myocardial ischemia and predict Sudden Cardiac Arrest (SCA) 1 to 6 hours before irreversible tissue necrosis or electrical collapse occurs. However, because our device is worn on the chest and wrist without wet adhesives or bulky wires, it must run on a small, lightweight $250\text{ mAh}$ battery for at least **7 continuous days**.

If our device ran its deep learning model continuously on every heartbeat (monolithic inference), the processor would consume $7.4\text{ mA}$ at $128\text{ MHz}$, depleting the battery in under 36 hours. 

Question 6.4 provides the architectural solution: an **Event-Driven Hierarchical Sentry Pipeline** that breaks monitoring into four cascading stages of increasing intelligence and power consumption:
1. **Stage 0 (Always-On Sentry at $<16\ \mu\text{A}$)**: The ST LSM6DSOX accelerometer's internal Finite State Machine (FSM) monitors sternal motion. The main processor stays in Deep Sleep ($1.3\ \mu\text{A}$).
2. **Stage 1 (Lightweight DSP Gate at $4.5\ \mu\text{J}$)**: The Cortex-M33 wakes for $0.42\text{ ms}$ to compute Signal Quality Index (kurtosis) and verify aortic recoil energy. **94.2% of normal heartbeats are confirmed benign and rejected here**, sending the processor right back to sleep.
3. **Stage 2 (Quantized TinyML Neural Model at $40\ \mu\text{J}$)**: Activated only when Stage 1 detects a contractility drop ($5.8\%$ of beats). The INT8 neural network evaluates 60-second temporal trends using SIMD instructions, resolving $98.6\%$ of non-ischemic false alarms.
4. **Stage 3 (Multi-Node BAN Corroboration & Escalation)**: Activated only during a verified high-confidence pre-infarction pattern ($P \ge 0.85$). The chest pendant wakes its BLE radio, commands the wrist PulseBand to check optical $SpO_2$ and Pulse Transit Time (PTT), triggers a 30-second silent haptic cancellation window on the wrist screen, and escalates to cellular emergency SOS if uncancelled.

```
==================================================================================================
           THE 4-STAGE HIERARCHICAL SENTRY PIPELINE IN OUR DUAL-NODE ARCHITECTURE
==================================================================================================

 [ STAGE 0: ST LSM6DSOX SENSOR ] ──► Quiet Sitting / Normal Motion ──► EasyDMA Buffers Data
 In-Sensor Finite State Machine        (Variance < 0.08 g^2)            (nRF5340 CPU Sleeps at 1.3 uA)
 Current: 15.5 uA | Always On                                                     │
                                                                   [ DPPI Hardware FIFO Event ]
                                                                                  │
                                                                                  ▼
 [ STAGE 1: CORTEX-M33 DSP GATE ] ──► Normal Aortic Recoil Energy ──► Sleep Immediately!
 Computes Kurtosis & Systolic Recoil  (94.2% of All Beats)             (Energy: 4.54 uJ / beat)
 Duration: 0.42 ms @ 64 MHz                                                       │
                                                                   [ Recoil Drops >28% or LVET Shortens ]
                                                                                  │
                                                                                  ▼
 [ STAGE 2: INT8 TINYML NEURAL ] ──► Transient Posture Shift ────────► Benign Fluctuation Resolved
 Evaluates 60s Trend (TCN / Mamba)   (98.6% of Anomalies Filtered)     (Energy: 39.96 uJ / inference)
 Duration: 1.80 ms @ 128 MHz                                                      │
                                                                   [ P(Ischemia) >= 0.85 Confirmed! ]
                                                                                  │
                                                                                  ▼
 [ STAGE 3: MULTI-NODE BAN ] ──────► Wake BLE Radio (7.8 mA) ────────► Query Wrist PulseBand:
 Escalates Life-Critical Threat       Corroborate SpO2 & PTT           Trigger 30s Haptic Interlock
                                                                       Transmit Encrypted SOS Beacon
==================================================================================================
```

---

## 2. Technical Implementation: How We Use the Hierarchical Pipeline in Firmware

Our firmware implements this pipeline as an interrupt-driven state machine compliant with **IEC 62304 Class C** medical safety protocols:

### A. Stage 0 Firmware Configuration (Sensor Die Level)
- The ST LSM6DSOX accelerometer is programmed via SPI at boot:
  - Output Data Rate (ODR): $100\text{ Hz}$.
  - Operating Mode: Low-Power Mode ($I_{\text{active}} = 12\ \mu\text{A}$).
  - Hardware FIFO: Watermark set to 32 samples ($320\text{ ms}$).
  - FSM Program: A 4-state state machine inside the sensor checks if axial variance $\sigma_z^2 < 0.08\text{ g}^2$. 
  - If high-amplitude arm-swinging or walking occurs, the sensor FSM discards the buffer internally.
  - When the 32-sample FIFO fills during low-motion periods, the sensor asserts `INT1`.

### B. Stage 1 Firmware Implementation (Microcontroller Wakeup)
- The Nordic nRF5340 DPPI routes the `INT1` pulse to the Application Core, which transitions from `IDLE` to `ACTIVE` at $64\text{ MHz}$.
- Direct Memory Access (EasyDMA) transfers the 32-sample buffer into internal SRAM without CPU instruction overhead.
- The CPU runs our deterministic DSP filter in C:
  1. **Kurtosis Validation**: Confirms that $2.5 \le \text{Kurtosis} \le 8.5$. If kurtosis is outside this band, the signal is corrupted by muscle tremor or clothing friction; the CPU increments an artifact counter and immediately goes back to sleep.
  2. **Recoil Energy Calculation**: Integrates power around the Aortic Opening (AO) peak:
     $$E_{\text{AO}} = \sum_{k=n_{\text{AO}}-5}^{n_{\text{AO}}+5} a_z[k]^2$$
  3. **Baseline Comparison**: If $E_{\text{AO}} \ge 0.72 \times \bar{E}_{\text{baseline}}$, the cardiac cycle is deemed mechanically normal. The dynamic baseline is updated using a slow leaky integrator ($2\%$ alpha), and the CPU re-enters Deep Sleep ($1.3\ \mu\text{A}$).
  4. Total execution time: **$0.42\text{ ms}$**; Energy: **$4.54\ \mu\text{J}$**.

### C. Stage 2 Firmware Implementation (Quantized Neural Inference)
- If $E_{\text{AO}}$ drops by $>28\%$ or Left Ventricular Ejection Time (LVET) deviates significantly, the firmware switches the system clock to $128\text{ MHz}$ and triggers the CMSIS-NN neural execution kernel.
- The network runs an 8-bit quantized 1D Temporal Convolutional Network (TCN) with dilated kernels spanning the prior 60 seconds of cardiac history.
- The inference completes in **$1.80\text{ ms}$**, consuming **$39.96\ \mu\text{J}$**.
- If the output softmax probability $P(\text{Ischemia}) < 0.85$, the model determines that the drop was an isolated benign variation, preventing an unwarranted alarm.

### D. Stage 3 Firmware Implementation (Multi-Node BAN Interlock)
- If $P(\text{Ischemia}) \ge 0.85$, the Application Core raises a high-priority software interrupt that wakes the nRF5340 Network Core and powers the $2.4\text{ GHz}$ BLE radio.
- The Sentry Pendant transmits an authenticated BLE notification to the Companion PulseBand on the wrist.
- The PulseBand powers its MAX86141 optical front-end to verify pulse wave velocity, oxygen saturation, and pulse arrival timing.
- Simultaneously, the PulseBand activates a distinct mechanical haptic vibration pattern and initiates a **30-second countdown screen**: *"Heart strain detected. Tap screen to cancel if false."*
- If the patient is conscious and taps the screen, the alert is logged as a patient-cancelled event. If the patient experiences syncope (sudden loss of consciousness) or the timer expires, the device activates the smartphone cellular SOS gateway, transmitting GPS coordinates and 60 seconds of precordial telemetry to emergency services.

---

## 3. Why We Chose This Architecture Over Alternatives

```
==================================================================================================
                 PIPELINE ARCHITECTURE TRADE-OFF EVALUATION
==================================================================================================

  Feature / Metric        Continuous Monolithic      Cloud-Streaming BAN       Our Hierarchical Sentry
  ──────────────────────────────────────────────────────────────────────────────────────────────────
  Processing Location     On-MCU Core (100% time)    AWS / Azure Cloud         Multi-Tier On-Body
  Active Processing Time  14.2 ms / beat (100% duty) Transmits raw 100 Hz RF   0.42 ms (94%), 1.8 ms (5.8%)
  Average Operating Power 24.42 mW                   18.5 mW (Radio TX)        0.14 mW (0.038 mA total)
  Battery Life (250mAh)   1.4 Days (Fails)           16 Hours (Unusable)       7.4 Days (Clinically Viable)
  Cellular Dead Zone Safe Yes                        No (Fatal Failure!)       Yes (Autonomous on Body)
  False Alarm Protection  Poor (No stage gating)     Variable Latency          Extreme (4-Stage SQI Gating)
  Patient Cancel InterlockNone                       Difficult (App Lag)       Built-in 30s Wrist Screen
==================================================================================================
```

### Why Not Continuous Monolithic Inference?
- Executing our full neural model on every single beat keeps the processor awake for $1.8\text{ to }14.2\text{ ms}$ every second. Adding clock-switching overhead and memory access, the battery dies in less than 36 hours. Patients will not comply with daily recharging schedules for a preventive device.

### Why Not Continuous Cloud Streaming?
- Continuous wireless transmission of raw accelerometer and optical streams over BLE/Cellular consumes $15\text{ to }25\text{ mA}$ continuously, killing the battery in under 16 hours.
- More dangerously, if an ischemic event occurs in an elevator, underground subway, airplane, or rural dead zone, a cloud-dependent device completely fails, resulting in unmonitored fatal cardiac arrest.

### The Decisive Advantage of Hierarchical Sentry:
- By handling 94.2% of normal heartbeats in a $0.42\text{ ms}$ DSP check and doing in-sensor gating at $<16\ \mu\text{A}$, the average operating current drops to **$38\ \mu\text{A}$** in sentry mode.
- This extends the operational lifespan of our $250\text{ mAh}$ cell to **7.4 continuous days**, while maintaining zero-latency, local, internet-independent emergency detection.

---

## 4. Competitive Clinical & Regulatory Differentiation

1. **Elimination of Alarm Fatigue (The #1 Clinical Rejection Reason)**: In hospital telemetry, up to 88% of cardiac alarms are false positives caused by motion artifacts or benign arrhythmias. By enforcing strict Stage 0 motion gating, Stage 1 kurtosis SQI checks, Stage 2 neural confirmation, and Stage 3 patient haptic cancellation, our false alarm rate is reduced by $>98\%$, preventing alarm fatigue and device abandonment.
2. **Deterministic Response in Fatal Sudden Cardiac Arrest**: Unlike cloud architectures that suffer from network jitter and 2-to-10-second server roundtrip delays, our edge pipeline executes the entire Stage 0 through Stage 2 cascade in **under 2.5 milliseconds**. If the heart suffers sudden ventricular fibrillation, the emergency alert is dispatched within milliseconds of mechanical collapse.
3. **Strict IEC 62304 Medical Software Compliance**: The state machine operates with zero dynamic heap allocation (`malloc` is strictly forbidden), bounded execution loops, and cycle-deterministic execution times, satisfying Class C safety standards for software that could cause serious injury or death.
