# Product Translation: Question 11.1 — Failure Mode & Effects Analysis (FMEA) and Safe-State Architecture

---

> **Document Type**: Tier 2.5 Engineering Implementation Dossier  
> **Question Reference**: `Phase 11 -> Question 11.1`  
> **Source Research**: [`Q11_1_Failure_Mode_Effects_Analysis.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_11_Failure_Modes_Failsafes/11.1_Failure_Mode_Effects_Analysis/Q11_1_Failure_Mode_Effects_Analysis.md)  
> **Target Audience**: Systems Engineers, Embedded Firmware Developers, and Regulatory Auditors

---

## 1. How the Finding Fits Our Device Concept

Our life-critical wearable system is designed to guard vulnerable cardiac patients against Sudden Cardiac Arrest (SCA) and acute ischemic events outside the hospital. In a Class C medical device, the most dangerous failure mode is a **silent failure**—a situation where an internal electronic glitch, sensor failure, or loose strap stops the device from monitoring the heart, while the patient falsely believes they are fully protected.

To prevent this hazard, our dual-node body area network (the Sentry Sternal Pendant and Companion PulseBand) implements a formal Failure Mode and Effects Analysis (FMEA) governed by **ISO 14971:2019** and **IEC 60812:2018**. Every physical sensor, battery cell, communication link, and firmware bus has an automated, continuous diagnostic supervisor running in real time. If any component breaks, degrades, or falls out of calibration, the system never silently fails. Instead, it immediately and deterministically transitions to a pre-defined safe state, alerts the user, and maintains as much lifesaving protection as physically possible.

---

## 2. How We Implement It in Hardware & Firmware

### A. Real-Time Sensor Health Supervision
1. **IMU Stiction & Pinning Defense (ST LSM6DSOX)**:
   - *Physics*: A physical drop or mechanical shock can cause the microscopic polysilicon fingers inside the accelerometer to adhere permanently (stiction) due to van der Waals forces, outputting a frozen, static number.
   - *Firmware Logic*: The supervisory thread executes an online **Welford Variance Test** on the raw 104 Hz accelerometer stream. Over a 4.0-second sliding window during waking hours, human breathing and micro-movements naturally produce subtle acceleration variance. If variance collapses below $\sigma^2 < 1.0 \times 10^{-6}\text{ g}^2$, the firmware flags the sensor as mechanically frozen and initiates a hardware self-test deflection pulse.
2. **Optical Saturation Defense (ADI MAX86141)**:
   - *Physics*: Intense direct sunlight leaking through the wristband seal generates massive photocurrent that overwhelms the photodiode transimpedance amplifier, clipping the ADC code to maximum (524,287) and drowning out the cardiac pulse wave.
   - *Firmware Logic*: The firmware monitors the **Perfusion Index** ($\text{PI} = \frac{\text{AC}}{\text{DC}} \times 100\%$). If $\text{PI} < 0.05\%$ while DC baseline exceeds 95% full-scale, the Ambient Light Cancellation (ALC) engine steps up its current subtraction DAC. If clipping persists for more than 3 consecutive seconds, the optical pulse channel is marked degraded.

### B. Autonomous Hardware Bus Recovery
1. **The 9-Clock I2C Un-Stick Routine**:
   - When an unexpected power dip or reset occurs mid-transmission, a peripheral sensor can hold the I2C data line (`SDA`) low indefinitely, causing the entire communication bus to freeze.
   - Our microcontroller peripheral driver reconfigures the clock line (`SCL`) into a general-purpose output and rapidly pulses it 9 times. This clocks out whatever byte the stuck sensor was trying to transmit, releasing the data line back to high.
2. **P-MOSFET Power-Cycle Gating**:
   - If the sensor fails to release the line after 9 clock pulses, the firmware toggles a dedicated Texas Instruments `TPS22918` load switch. This physically cuts the $1.8\text{ V}$ power rail to the sensors for 50 milliseconds, draining all capacitors and forcing a cold power-on reset without crashing the main microcontroller.

### C. 4-Tier Deterministic Safe-State Ladder
1. **Tier 0 (Fully Nominal)**: Both nodes active, dual-node Pulse Transit Time (PTT) blood pressure and Seismocardiography (SCG) contractility tracking fully operational.
2. **Tier 1 (Graceful Fallback)**: If the wrist optical PPG saturates (e.g., direct sunlight or loose strap), the system does not shut down. It automatically falls back to single-node precordial SCG contractility and heart rhythm tracking, logged silently while giving a gentle wrist haptic cue: *"Adjust wristband"*.
3. **Tier 2 (Critical Service Annunciation)**: If the primary chest IMU suffers an unrecoverable failure or the harness is completely removed for $>30$ seconds, the device sounds an audible 75 dB piezo buzzer and delivers a synthesized voice alert: *"Device service required. Sensor check needed."* Simultaneously, an encrypted notification is pushed to the family caregiver dashboard via Bluetooth/cellular uplink.
4. **Tier 3 (System Lockup & Safe Crash Dump)**: If a memory corruption or unrecoverable bus hang occurs, the ARM Cortex-M33 hardware watchdog timer forces a deterministic reboot, saving a diagnostic crash dump into persistent SPI flash for clinical engineering analysis.

---

## 3. Why We Chose This Over Alternatives

* **Why Deterministic Fallback vs. Full System Shutdown**:
  - *Alternative*: Traditional consumer wearables simply display an error screen or shut off when a sensor reading is lost.
  - *Clinical Rationale*: A patient wearing our device is at high risk of sudden cardiac arrest. If the wristband optical sensor is blinded by sunlight, shutting down the entire system leaves the patient completely unprotected. Our graceful fallback retains precordial sternal vibration monitoring, ensuring basic ventricular contractility and rhythm tracking continue uninterrupted.
* **Why Hardware Load-Switch Power Cycling vs. MCU Software Resets**:
  - *Alternative*: Many embedded devices reset the entire microcontroller when an I2C bus locks up.
  - *Engineering Rationale*: Resetting the main MCU wipes real-time clock synchronization, loses buffered data packets, and interrupts emergency Bluetooth beacons. By placing a discrete P-MOSFET load switch on the sensor rail, we can cold-boot only the misbehaving sensor in 50 ms while the microcontroller continues executing vital background tasks.
* **Why Annunciated Safe States vs. Silent Logging**:
  - *Alternative*: Many devices silently log sensor faults to an internal error file to avoid bothering the user.
  - *Safety Rationale*: Under IEC 60601-1-8 and ISO 14971, silent failure in a cardiac monitor is classified as a Severity 10 hazard (potential patient death). When monitoring cannot continue, the patient and caregiver must be actively informed so manual monitoring or clinical evaluation can take over immediately.

---

## 4. Summary Specifications Table

| Subsystem Parameter | Production Specification | Clinical & Engineering Rationale |
| :--- | :--- | :--- |
| **Risk Management Standard** | ISO 14971:2019 & IEC 60812:2018 | Mandatory international frameworks for medical device risk and FMEA |
| **Maximum Unannounced Downtime** | 0.00 seconds (Zero tolerance for silent failures) | Prevents dangerous false sense of security in high-risk cardiac patients |
| **IMU Stiction Detection Window** | 4.0 seconds ($\sigma^2 < 10^{-6}\text{ g}^2$) | Detects mechanical accelerometer pin without false-triggering during sleep |
| **I2C Bus Recovery Protocol** | 9 SCL clock pulses followed by STOP | NXP / TI standard for releasing hung open-drain slave devices |
| **Sensor Power-Cycle Pulse** | 50 ms cut via TPS22918 P-MOSFET | Clears internal silicon latches and drains decoupling capacitor charge |
| **Audible Alarm Annunciation** | $\ge 75\text{ dB}$ at 10 cm, $2,730\text{ Hz}$ tone | Meets IEC 60601-1-8 audibility standards for life-critical medical equipment |
| **Graceful Fallback Mode** | Automated transition to Sternal SCG only | Maintains core cardiac monitoring even if peripheral wrist optical link drops |
