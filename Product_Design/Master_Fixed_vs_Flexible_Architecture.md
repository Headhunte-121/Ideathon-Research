# Master Systems Architecture: Fixed Realities vs. Flexible Choices
### The Single Source of Truth for What Is Scientifically Locked vs. What the Team Can Decide

---

> **Purpose**: This document tracks the hard boundaries of our project.  
> * **PART 1: FIXED REALITIES**: Biophysical laws, clinical timelines, and engineering constraints that are **100% locked in by research** and cannot be changed without breaking the medical validity of the device.  
> * **PART 2: FLEXIBLE CHOICES**: Product design choices, form factors, styling, battery trade-offs, and business models that are **completely open for the team to choose and customize**.  
> * 🌟 **LOCKED DECISIONS LOG**: See [`OFFICIAL_TEAM_DECISIONS_LOG.md`](file:///c:/College/Ideathon/Product_Design/OFFICIAL_TEAM_DECISIONS_LOG.md) for the team's official locked architecture choices.

---

```
=================================================================================================================================
                                            MASTER PROJECT ARCHITECTURAL BOUNDARIES
=================================================================================================================================
```

---

## PART 1: The FIXED Realities (Non-Negotiable Facts from Research)

These points are locked in by peer-reviewed clinical literature and signal acquisition physics. Changing any of these would cause the device to fail clinically or physically:

### 1. The Pre-Infarction Countdown & Clinical Need (Phase 1)
* **[LOCKED] 70% to 80% Ischemic Origin**: 70% to 80% of sudden non-traumatic cardiac arrests in adults stem from acute myocardial ischemia (coronary blood starvation).
* **[LOCKED] The 20-Minute Necrosis Window**: Cellular death begins within **20 minutes** of total arterial blockage; irreversible full-thickness (transmural) necrosis occurs within **2 to 4 hours**.
* **[LOCKED] The 1-to-6-Hour Physiological Timeline**: Ischemia does not strike instantly. It triggers an ordered biological countdown:
  1. *Hours -6 to -4*: Autonomic destabilization (vagal withdrawal, loss of HRV, cold diaphoresis).
  2. *Hours -4 to -2*: Left ventricular active relaxation failure (mechanical pump stiffening; SCG AO amplitude drops $>50\%$).
  3. *Hours -3 to -1*: Retrograde pulmonary transudation (LVEDP $>20\text{ mmHg}$, fluid accumulates in lungs, $Z_0$ drops $15\%\text{--}35\%$, rapid breathing $>20\text{ bpm}$).
  4. *Hours -1 to 0*: Subendocardial microvolt injury currents ($5\text{--}20\ \mu\text{V}$ ST-deviation) and repolarization dispersion, triggering lethal ventricular fibrillation.
* **[LOCKED] Hospital Arrival Lag**: Patients arrive at hospitals an average of **2 to 4 hours post-infarction**, after irreversible tissue death has already occurred.
* **[LOCKED] Smartwatch "Hour 0" Failure**: Consumer smartwatches detect arrhythmias only **after** the heart has already electrically collapsed.

### 2. Anatomical Sensing Physics & Location Rules (Phase 2)
* **[LOCKED] Chest-Only Signal Propagation**: Mechanical cardiac recoil micro-vibrations (SCG) and thoracic pulmonary fluid transudation (Bio-Z) **do not physically propagate down the arm**. They can only be measured on the anterior chest cage.
* **[LOCKED] Peripheral Vasoconstriction Blind Spot**: During acute ischemic distress, sympathetic vasoconstriction clamps down arm and wrist microvasculature to save core organs. Wrist pulse signals collapse by **$>95\%$**, while sternal chest vessels retain **$71.3\%$** pulsatile amplitude.
* **[LOCKED] The 8.0 cm Sternal ECG Axis**: 352-node BSPM proves an 8.7 cm bipolar lead over the left ventricle yields a peak **1.9 mV** QRS signal. An **8.0 cm longitudinal axis** captures $>90\%$ amplitude. Anchoring to the sternal bone avoids $20\text{--}1000\text{ Hz}$ pectoralis major muscle electrical noise.
* **[LOCKED] The 3-Centimeter Precision Penalty (LLSB 4th Rib Space)**: The Left Lower Sternal Border is the acoustic sounding board for cardiac vibrations. Shifting the sensor by just **3 cm** introduces a **7% waveform distortion** and a **9% Pre-Ejection Period (PEP) error**.
* **[LOCKED] Tracheal Respiration (Suprasternal Notch)**: Listening directly over the windpipe isolates breath sounds from thoracic heart thumping, achieving respiratory rate error **$<1\%$** ($<3\text{ bpm}$).
* **[LOCKED] Tetrapolar (4-Electrode) Bio-Z**: Two electrodes inject high-frequency current ($50\text{--}100\text{ kHz}$) and two independent electrodes measure voltage ($55\text{ mm}$ spacing). This physical separation is mathematically mandatory to decouple skin sweat resistance from internal lung fluid measurements.

### 3. Kinematic Noise & Motion Artifacts (Phase 2 & 3)
* **[LOCKED] The Walking Foot-Strike Shockwave**: Normal walking sends skeletal shockwaves into the chest that drive mechanical SCG SNR down to **$-27\text{ dB}$**.
* **[LOCKED] Dual-IMU Adaptive Filtering**: A single motion sensor cannot separate footsteps from a failing heart. A primary sensor on the sternum paired with an upper clavicle reference sensor running an NLMS adaptive filter improves systolic signal clarity by **$7\times$** and diastolic filling clarity by **$11\times$**.
* **[LOCKED] The Loose Hanging Pendant Barrier**: A freely swinging necklace pendant generates pendulum forces of **$500\text{ to }1,500\text{ milli-g}$**, which is **100 times larger** than the heart's $5\text{--}20\text{ milli-g}$ micro-thump. A loose pendant also lifts off the chest, breaking the electrical circuit and leaking ambient sunlight into optical diodes.

---

## PART 2: The FLEXIBLE Choices (Open for Team Decisions)

These are the customizable engineering, product, aesthetic, and business options. Your team has full freedom to decide, tweak, and prioritize these points:

```
+----------------------------------------------------------------------------------------------------+
|                                    OPEN TEAM DESIGN CHOICES                                        |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|   1. FORM FACTOR SELECTION      --> Magnetic Snap Pendant vs. Sternal Pod vs. Smart Undershirt     |
|   2. INDUSTRIAL DESIGN & LOOK   --> Luxury Titanium Jewelry vs. Sleek Minimalist Sports Tech       |
|   3. BATTERY SIZE VS. WEIGHT    --> 150 mAh (Ultra-light, 3-day) vs. 250 mAh (Thin, 7-day)         |
|   4. USER ALERTING UX           --> Silent Haptic Vibration vs. Smartphone Siren vs. Cloud App     |
|   5. BUSINESS BEACHHEAD TARGET  --> Post-PCI Hospital Discharge vs. Cardiology Outpatients vs D2C |
|   6. POSTER CONTENT SELECTION   --> Picking specific candidate blocks from A0 Modular Canvas       |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

### Choice 1: The Physical Form Factor & System Architecture
* 🌟 **[OFFICIALLY LOCKED TEAM ARCHITECTURE] The Modular "2-in-1" Sentry Pod with On-Contact Dry ECG & Companion PulseBand**:
  * **System Reference**: 📄 [`Dual_Node_Pendant_and_Wristband_Architecture.md`](file:///c:/College/Ideathon/Product_Design/Dual_Node_Pendant_and_Wristband_Architecture.md)
  * **Core Architectural Decision**:
    * **Node A: The Modular 2-in-1 Sentry Pod (Lower Sternum)**:
      * *Mode 1 (Sentry Clinical Mode)*: Worn against the skin via an adjustable soft neck cord (0.8 N preload) or compression undershirt cradle directly over the breastbone. Integrated dry 316L stainless steel back electrodes provide continuous precordial ECG with **zero wet hydrogel glue**, synchronized with mechanical Seismocardiography (SCG).
      * *Mode 2 (Casual Clothing Clip Mode)*: Magnetically unclips to snap onto an outer shirt collar or pocket. Hardware Lead-Off automatically powers down the ECG front-end to conserve battery, while the IMU tracks chest-wall breathing and fall dynamics through fabric. A front bezel contact enables **30-second on-demand finger spot-check ECG**.
      * *Primary Motion Sensor*: **ST LSM6DSOX** ($60\ \mu\text{g}/\sqrt{\text{Hz}}$ ultra-low noise, 9 KB FIFO, embedded MLC). Measures Aortic Opening ($F = m \cdot a$) and Left Ventricular Ejection Time (LVET).
      * *Clinical Breakthrough*: Enables **Pre-Ejection Period (PEP)** measurement (electrical Q-wave to mechanical AO peak delay) to detect ischemic myocardial contractility collapse hours before electrical arrest.
    * **Node B: The Companion PulseBand (Non-Dominant Wrist)**:
      * *Sensors*: ADI MAX86141 dual-wavelength optical PPG ($SpO_2$, pulse volume) + **Palmar Galvanic Skin Response (GSR)** to detect autonomic cold-sweat diaphoresis.
      * *Denoising*: Onboard 3-axis arm IMU acts as an adaptive reference, feeding an on-device NLMS filter to subtract footstrike shockwaves from the chest readings.
      * *Continuous PTT*: Measures sub-millisecond Pulse Transit Time between sternal AO and radial pulse arrival for continuous cuffless blood pressure.
      * *Cancellation UX*: OLED micro-display with a 30-second multi-modal cancel window (side-rail squeeze or palm-cover reflex).
  * **Why This Won**: Eliminates 100% of adhesive skin tears (MARSI-free) and bypasses the Day-5 hydrogel desiccation wall, while preserving true clinical electrical ECG, mechanical contractility, and cold-sweat verification.
* **Archived Alternative Proposals**:
  * 📄 [Asmita Two-Node PPG & IMU Clip Proposal](file:///c:/College/Ideathon/Product_Design/Asmita_Two_Node_PPG_IMU_Proposal.md) (Integrated: Palmar GSR, fall detection, and clothing clip mode adopted into modular pod).
  * Option A: Magnetic Snap-to-Skin Pendant (Jewelry / Lifestyle Focus)
  * Option B: Contoured Biowearable Sternal Pod (Abbott Lingo / Dexcom Focus)
  * Option C: Smart Athleisure / Base Layer (Whoop AnyWear Focus)

---

### Choice 2: Industrial Design, Casing & Aesthetics
* 🌟 **[OFFICIALLY LOCKED TEAM DECISION 2 & 9] Medical-Grade Polycarbonate & Biocompatible Silicone**:
  * Chest Pod: Injection-molded medical polycarbonate with liquid silicone overmold and stamped 316L surgical stainless steel electrodes. Soft neck cord (0.8 N preload) with magnetic break-away clasp. Featherweight $15\text{ grams}$ total, $6.8\text{ mm}$ thickness.
  * Companion PulseBand: Hypoallergenic medical silicone strap with integrated palmar stainless steel / conductive elastomer GSR contacts and side tactile click button.

---

### Choice 3: Battery Capacity vs. Thickness & Weight
* 🌟 **[OFFICIALLY LOCKED TEAM DECISION 9] Asymmetric 150 mAh Chest Pod + 240 mAh Wristband**:
  * Sternal Pod: 150 mAh LiPo pouch cell (Model 502025: 3.2g, 5mm thick) delivers 5–7 days of continuous monitoring with minimal pendulum inertia for clean SCG detection.
  * PulseBand: 240 mAh LiPo pouch cell (Model 502030: 5.4g) comfortably powers high-current optical PPG LEDs and display for 5–7 days.
  * Charging: Single dual-dock magnetic pogo-pin cradle recharges both nodes simultaneously in under 45 minutes every Sunday. Power BOM: $3.50.

---

### Choice 4: User Alerting & Emergency Escalation UX
* 🌟 **[OFFICIALLY LOCKED TEAM DECISIONS 7 & 8] Tactile Cancel Button + Syncope-Gated 85 dB Siren & Bystander CPR Metronome**:
  * 30-Second Cancel Window: Haptic vibration + visual OLED countdown on wrist; cancelled via intentional 2-second hold of a physical textured click button.
  * Hardware Fall Lockout: $>3.0\ g$ impact followed by stillness automatically locks out the button so an unconscious patient on the floor cannot abort emergency dispatch.
  * Syncope-Gated Siren: 85 dB alarm and 110 BPM AHA CPR voice coach sound ONLY if physical collapse (horizontal posture + loss of pulsatile flow) is confirmed. If ambulatory/conscious, siren remains muted and silent SMS dispatch is routed to family and doctor.

---

### Choice 5: Go-to-Market Beachhead & Commercial Strategy
* 🌟 **[OFFICIALLY LOCKED TEAM DECISION 10] Two-Tiered Clinical Rollout**:
  * Primary Beachhead: 30-Day Post-PCI / Stent Discharges (~4.3M annual US/India cases) to prevent lethal stent thrombosis and shield hospitals from Medicare 30-day HRRP readmission penalties.
  * Secondary Beachhead: The 40-to-90-Day Post-Infarction ICD Waiting Gap ($LVEF \le 35\%$), displacing the suffocating $3,500–$4,000/month ZOLL LifeVest rental.

---

### Choice 6: Unit Economics & Bill of Materials Presentation
* 🌟 **[OFFICIALLY LOCKED TEAM DECISION 11] Unified Lab-to-Factory & 6x Hospital Reusability Model**:
  * Benchtop Lab Prototype: Functional proof-of-concept built for ₹4,595 (~$55) using COTS modules.
  * Factory 10k SMT Scale: Scaled kit BOM drops to $33.50 (~₹2,775) including chest pod, wristband, charger, and packaging.
  * Reusable Hospital Economics: 100% glue-free design sanitizes with 70% isopropyl wipes and re-issues across 6 patients/year, yielding an unbeatable clinical cost of **$5.58 (~₹460) per patient**.

---

### Summary Table: Fixed vs. Flexible at a Glance

| Category | What is FIXED (Non-Negotiable Science) | Officially Locked Team Decisions |
| :--- | :--- | :--- |
| **Anatomy & Location** | Must be placed on breastbone (8 cm axis, LLSB 4th ICS) + wrist radial artery. | Modular 2-in-1 Sentry Pod (Mode 1 Sentry on sternum + Mode 2 Casual clip) + Companion PulseBand. |
| **Electronics & Sensors** | Ultra-low-noise IMU ($<100\ \mu\text{g}/\sqrt{\text{Hz}}$), optical PPG, palmar cold sweat. | ST LSM6DSOX + ADI MAX86141 + Knowles MEMS Mic + 316L Dry ECG + Palmar GSR. |
| **Compute & Algorithms** | Dual-core processing, motion-compensated DSP, baseline adaptation. | Nordic nRF5340 + Hybrid NLMS/DWT ($28\ \mu\text{s}$, $38\ \mu\text{W}$) + Foundational CNN + Personalized Autoencoder. |
| **Emergency Telemetry** | Low-latency dispatch without heavy 2A cellular modem bulk. | Smartphone BLE 5.3 Gateway (uses phone GPS/cellular; $0 hardware SIM fees). |
| **False-Alarm & Alert UX** | Tremor-resistant cancellation, high-decibel bystander intervention. | Physical click button (2s hold + fall lockout) + syncope-gated 85 dB siren with 110 BPM CPR coach. |
| **Power Profile** | Minimum 5–7 day clinical window; lightweight sternal node. | Asymmetric: 150 mAh Pod (15g, 6.8mm) + 240 mAh Wristband (synchronized 7-day recharge). |
| **Clinical Beachhead** | High-density acute mortality window with hospital economic alignment. | Tiered: 30-Day Post-PCI Stent Discharges primary + 90-Day Weak Heart ICD Waiting Gap secondary. |
| **Unit Economics** | Accessible healthcare cost structure without single-use waste. | ₹4,595 prototype BOM $\rightarrow$ $33.50 factory kit BOM $\rightarrow$ $5.58/patient across 6 hospital reuses. |
