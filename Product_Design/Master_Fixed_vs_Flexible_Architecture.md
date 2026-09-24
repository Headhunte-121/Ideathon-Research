# Master Systems Architecture: Fixed Realities vs. Flexible Choices
### The Single Source of Truth for What Is Scientifically Locked vs. What the Team Can Decide

---

> **Purpose**: This document tracks the hard boundaries of our project.  
> * **PART 1: FIXED REALITIES**: Biophysical laws, clinical timelines, and engineering constraints that are **100% locked in by research** and cannot be changed without breaking the medical validity of the device.  
> * **PART 2: FLEXIBLE CHOICES**: Product design choices, form factors, styling, battery trade-offs, and business models that are **completely open for the team to choose and customize**.

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
* 🌟 **[OFFICIALLY SELECTED BY TEAM] Option D: The Dual-Node BAN Ecosystem (Sentry Pendant + Companion PulseBand)**:
  * **System Reference**: 📄 [`Dual_Node_Pendant_and_Wristband_Architecture.md`](file:///c:/College/Ideathon/Product_Design/Dual_Node_Pendant_and_Wristband_Architecture.md)
  * **Chest Pendant**: 38 mm sleek tech pendant mounted on an adjustable tension cord (100% GLUE-FREE, ZERO ECG electrodes). Houses ultra-low-noise 6-axis IMU (LSM6DSOX) for Seismocardiography (SCG) mechanical ejection tracking.
  * **Wristband**: Minimalist bracelet with optical PPG (MAX30102 / MAX86141) for $SpO_2$, pulse rate, PRV, arm-motion filtering, and haptic alert/display.
  * **Why Selected**: 100% adhesive-free comfort; ultra-affordable ₹820 BOM; captures mechanical contractility collapse 1-3 hours early; solves user interface and PTT blood pressure tracking without sticky chest patches.
* **Option A: The Magnetic Snap-to-Skin Pendant (Jewelry / Lifestyle Focus)**
* **Option B: Contoured Biowearable Sternal Pod (Abbott Lingo / Dexcom Focus)**
* **Option C: Smart Athleisure / Base Layer (Whoop AnyWear Focus)**

---

### Choice 2: Industrial Design, Casing & Aesthetics
* **Materials**:
  * *Aerospace-grade Grade 5 Titanium*: Premium, hypoallergenic, ultra-lightweight, luxury finish.
  * *Zirconia Ceramic*: Scratch-resistant, glass-like finish (similar to Oura Ring or Apple Watch backplate).
  * *Medical Polycarbonate*: Durable, cost-effective, high-impact resistance for athletic/sports telemetry.
* **Finishes & Colorways**:
  * Matte Stealth Black, Brushed Silver, Rose Gold, or Athletic Graphite.

---

### Choice 3: Battery Capacity vs. Thickness & Weight
* **Ultra-Lightweight Profile**:
  * *Battery*: 150 mAh rechargeable LiPo cell.
  * *Dimensions*: ~6.5 mm thick, total weight ~18 grams.
  * *Runtime*: 3 to 4 days of continuous multi-modal monitoring.
* **Extended Endurance Profile**:
  * *Battery*: 250 mAh rechargeable LiPo cell.
  * *Dimensions*: ~8.5 mm thick, total weight ~26 grams.
  * *Runtime*: 7 to 10 days of continuous monitoring on a single charge.

---

### Choice 4: User Alerting & Emergency Escalation UX
* **Alert Trigger Protocol**:
  * *Discreet Haptic Interlock*: On-device silent vibration alert with a 30-second double-tap countdown to cancel accidental false alarms before anyone else is notified.
  * *Smartphone Escalation*: Paired smartphone sounds a high-decibel alarm and automatically displays hospital routing and bystander CPR instructions.
  * *Zero-Touch Cloud Dispatch*: Automatic encrypted transmission of GPS coordinates, patient history, and telemetry to emergency EMS dispatch (911) if the user loses consciousness (syncope).

---

### Choice 5: Go-to-Market Beachhead & Business Strategy
* **Option A: Post-PCI / CABG Hospital Discharge Pilot (The B2B Medical Route)**:
  * Target 1.2 million angioplasty and bypass surgery patients during their high-risk 30-day recovery window.
  * Sold to hospital cardiology networks to reduce 30-day readmission penalties under Remote Patient Monitoring (RPM) insurance codes.
* **Option B: Cardiology Clinic Outpatient Prescription (The Specialist Route)**:
  * Prescribed by cardiologists for patients with unexplained syncope, high calcium scores, or family history of sudden death.
* **Option C: High-Risk Consumer Direct-to-Consumer (The D2C Wellness Route)**:
  * Sold directly to health-conscious consumers with diabetes, hypertension, or high athletic cardiovascular stress.

---

### Choice 6: Poster Block Selection for the Competition
* Your team can open [`A0_Poster_Modular_Canvas.md`](../Ideathon_Poster_and_Pitch/A0_Poster_Modular_Canvas.md) and pick which candidate blocks, tables, and diagrams to highlight on your final visual presentation.

---

### Summary Table: Fixed vs. Flexible at a Glance

| Category | What is FIXED (Non-Negotiable Science) | What is FLEXIBLE (Team Choices) |
| :--- | :--- | :--- |
| **Anatomy & Location** | Must be placed on the breastbone (8 cm axis, LLSB 4th ICS, suprasternal notch). | Whether it is held there by a magnetic necklace dock, a direct adhesive pod, or an undershirt. |
| **Electronics & Sensors** | Requires 24-bit ECG/Bio-Z (ADS1292R), dual-IMUs for walking cancellation, and optical AFE. | Enclosure styling, casing material (titanium vs. ceramic), and exact PCB layout shape. |
| **Clinical Mission** | Intercepting the 1-to-6-hour pre-infarction countdown before irreversible tissue necrosis. | Target launch market (Post-PCI discharge hospital sales vs. direct-to-consumer subscription). |
| **Motion Noise** | Walking creates -27 dB noise; requires dual-IMU NLMS adaptive filtering. | Visual branding, product name, companion app user interface, and poster color scheme. |
