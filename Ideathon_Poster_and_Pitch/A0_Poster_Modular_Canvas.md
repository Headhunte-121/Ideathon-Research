# A0 Modular Poster Canvas: Autonomous Sternal Sentry
## Modular Visual Blueprint for Medical IoT Ideathon Poster (All 12 Phases + Extras)

---

> **Format**: A0 Portrait / Landscape Modular Canvas (Standard 841 mm × 1189 mm)  
> **Target Event**: College Medical IoT Ideathon  
> **Team Protocol**: This canvas **does not lock in** final text. Every block clearly presents our **suggested candidate points, clinical numbers, and hardware specs** based on verified research, accompanied by a clean **blank slot** where the team can pick, edit, and fill in final poster copy.  
> **Navigation**: Every block links directly to its 3-tier research layer (Takeaways, Product Translations, and Deep Research Vault).

---

```
===================================================================================================================
                                      A0 MODULAR POSTER LAYOUT SCHEMATIC
===================================================================================================================

 [ HEADER BLOCK: PROJECT TITLE, TEAM DOMAIN LEADS, AFFILIATION & 1-SENTENCE VALUE PROPOSITION ]
 ─────────────────────────────────────────────────────────────────────────────────────────────
  COLUMN 1: THE CLINICAL URGENCY    │  COLUMN 2: HARDWARE & BIOPHYSICS │  COLUMN 3: AI, DATA & REJECTION
 ───────────────────────────────────┼──────────────────────────────────┼─────────────────────────────────
  Block 1: Clinical Crisis & Hook   │  Block 4: Anatomical Sweet Spot  │  Block 7: Signal Processing (Ph3)
  (Phase 1: Q1.1 1-to-6-Hr Cascade) │  (Phase 2: Q2.2 Sternal Axis)    │  (Analog AFE & Adaptive Denoise)
                                    │                                  │
  Block 2: Non-Invasive Biometrics  │  Block 5: Sensor BOM & Modalities│  Block 8: TinyML & Edge Architecture
  (Phase 1: Q1.2 Physical Outputs)  │  (Phase 2: Q2.1 COTS Chips)      │  (Phases 4, 5, 6: AI Pipeline)
                                    │                                  │
  Block 3: Patient Demographics     │  Block 6: Digitization Physics   │  Block 9: Clinical False-Alarm Logic
  (Phase 1: Q1.3 & Q1.5 Circadian)  │  (Phase 2: Q2.3 24-bit FIFO/DMA) │  (Phase 1: Q1.4 Confounder Decouple)
 ───────────────────────────────────┴──────────────────────────────────┴─────────────────────────────────
  BOTTOM FOOTER ROW: MARKET VIABILITY, REGULATORY ROADMAP & COMPETITIVE DEFENSE
 ────────────────────────────────────────────────────────────────────────────────────────────────────────
  Block 10: Head-to-Head Competitive Moat Matrix (vs Apple Watch, Whoop, Holter, Zio, LifeVest)
  Block 11: Market Beachhead (Post-PCI), Health Economics & RPM Reimbursement (Phase 12)
  Block 12: Regulatory Strategy (FDA Class II 510(k), CDSCO) & 3-Phase Clinical Roadmap (Phases 9-11)
===================================================================================================================
```

---

## 🏷️ HEADER BLOCK: Project Identity & Domain Leadership
* **Poster Header Content**:
  * **Project Title**: The Autonomous Sternal Sentry: Predicting Sudden Cardiac Arrest in the Pre-Infarction Window
  * **Subtitle**: Continuous multi-modal sternal biowearable intercepting the 1-to-6-hour ischemic countdown before fatal ventricular collapse.
  * **Team Domain Leads**:
    * *Clinical Cardiology & Pathophysiology*: `[ Team Member 1 Name ]`
    * *Sensor Hardware & Biophysics*: `[ Team Member 2 Name ]`
    * *Firmware, DSP & Edge AI*: `[ Team Member 3 Name ]`
    * *Health Economics, Market & Regulatory*: `[ Team Member 4 Name ]`

---

## 🟥 COLUMN 1: THE CLINICAL URGENCY & PHYSIOLOGY

### BLOCK 1: The Clinical Crisis & 1-to-6-Hour Cascade (Phase 1.1)
* **Domain Lead**: Clinical / Pathophysiology
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🟢 [Q1.1 Takeaway Summary](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_1_Takeaway.md)
  * 🟡 [Q1.1 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_1_Product_Translation.md)
  * 🔵 [Phase 1.1 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md)
* **Suggested Candidate Bullet Points**:
  * Sudden Cardiac Arrest (SCA) claims >350,000 US and >700,000 India lives annually; out-of-hospital survival is <10%.
  * 70% to 80% of adult arrests stem from acute myocardial ischemia (coronary blood starvation).
  * Current care gap: Smartwatches alert only post-collapse (Hour 0); hospitals admit patients 2 to 4 hours post-infarction (after irreversible necrosis).
  * The 1-to-6-hour ischemic countdown: Sympathetic surge $\rightarrow$ Myocardial ATP depletion $\rightarrow$ Contractility collapse ($>50\%$) $\rightarrow$ Pulmonary fluid backpressure $\rightarrow$ Ventricular Fibrillation.
* **Suggested Visual**: 1-to-6-hour chronological countdown timeline showing physiological progression vs conventional hospital arrival delay.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate points and write finalized Block 1 text here ]
  ```

---

### BLOCK 2: Non-Invasive Physical Outputs & Signal Mapping (Phase 1.2)
* **Domain Lead**: Biomedical / Sensors
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🟢 [Q1.2 Takeaway Summary](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_2_Takeaway.md)
  * 🟡 [Q1.2 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_2_Product_Translation.md)
  * 🔵 [Phase 1.2 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.2_Non_Invasive_Physical_Outputs/Q1_2_Non_Invasive_Physical_Outputs.md)
* **Suggested Candidate Bullet Points**:
  * Cellular ischemia emits physical signals across 5 synchronized physiological channels:
    1. *Electrical*: Microvolt ST-shifts and T-wave alternans (repolarization heterogeneity).
    2. *Mechanical*: Aortic valve recoil decay and Pre-Ejection Period lengthening (myocardial stiffening).
    3. *Optical*: Sternal microvascular volume pulse changes.
    4. *Acoustic*: Pathologic $S_3 / S_4$ diastolic gallops from elevated filling pressures.
    5. *Bio-Impedance*: Baseline thoracic impedance ($Z_0$) drop indicating lung fluid transudation.
* **Suggested Visual**: Multi-modal waveform diagram illustrating synchronized mechanical, electrical, and impedance deviations during early ischemia.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate points and write finalized Block 2 text here ]
  ```

---

### BLOCK 3: Demographic Inclusivity & Circadian Intelligence (Phases 1.3 & 1.5)
* **Domain Lead**: Clinical / Data Science
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🟢 [Q1.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_3_Takeaway.md) | 🟢 [Q1.5 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_5_Takeaway.md)
  * 🟡 [Q1.3 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_3_Product_Translation.md) | 🟡 [Q1.5 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_5_Product_Translation.md)
  * 🔵 [Phase 1.3 Deep Research](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.3_Demographic_Variations/Q1_3_Demographic_Variations.md) | 🔵 [Phase 1.5 Deep Research](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.5_Circadian_Sleep_Adaptations/Q1_5_Circadian_Sleep_Adaptations.md)
* **Suggested Candidate Bullet Points**:
  * *Diabetic Silent Ischemia*: 30-40% of diabetics suffer painless infarctions due to autonomic neuropathy; mechanical contractility (SCG) and lung fluid (Bio-Z) catch what symptoms miss.
  * *Elderly Personalization*: Rolling 72-hour personalized $Z$-scores prevent false alarms from age-related arterial stiffness.
  * *Circadian Vulnerability*: 6:00 AM – 12:00 PM morning cortisol/platelet surge triggers dynamic sensitivity scaling.
  * *Sleep-Stage Gating*: Distinguishes benign REM dream tachycardia from nocturnal ischemic events.
* **Suggested Visual**: 24-hour circadian cardiac vulnerability curve with morning risk peak highlighted.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate points and write finalized Block 3 text here ]
  ```

---

## 🟦 COLUMN 2: HARDWARE, BIOPHYSICS & DIGITIZATION

### BLOCK 4: Anatomical Sweet Spot & Form Factor Physics (Phase 2.2 + Design)
* **Domain Lead**: Biomedical / Mechanical
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🟢 [Q2.2 Takeaway Summary](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_2_Takeaway.md)
  * 🟡 [Q2.2 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_2_Product_Translation.md)
  * 🔵 [Phase 2.2 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.2_Anatomical_Sweet_Spots/Q2_2_Anatomical_Sweet_Spots.md)
  * 💡 [Form Factor Evaluation Study](file:///c:/College/Ideathon/Product_Design/Form_Factor_Evaluation_Pendant_vs_Patch.md)
  * 🖼️ Anatomical Diagram: [`optimal_anatomical_landmarks_telemetry.png`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/assets/optimal_anatomical_landmarks_telemetry.png)
* **Suggested Candidate Bullet Points**:
  * Sternal Body / LLSB (4th Intercostal Space): Provides direct rigid bone acoustic window to aortic root and right ventricle.
  * Shock Resilience: During cardiogenic shock, peripheral wrist vessels constrict (>95% pulse signal lost); sternal vessels retain 71.3% perfusion.
  * Form Factor Breakthrough: Reusable titanium/ceramic pod magnetically docks (4.5 N pull force) to an ultra-thin (1.2 mm) concealed silicone skin dock. Eliminates pendulum swing noise while enabling 1-second snap-off recharging.
* **Suggested Visual**: Anatomical placement diagram showing sternal 8cm dipole axis and magnetic dock cross-section.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate points and write finalized Block 4 text here ]
  ```

---

### BLOCK 5: COTS Sensor Bill of Materials (BOM) & Modalities (Phase 2.1)
* **Domain Lead**: Embedded Hardware
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🟢 [Q2.1 Takeaway Summary](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_1_Takeaway.md)
  * 🟡 [Q2.1 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_1_Product_Translation.md)
  * 🔵 [Phase 2.1 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.1_Sensing_Modalities_Biomarker_Mapping/Q2_1_Sensing_Modalities_Biomarker_Mapping.md)
  * 🖼️ Modalities Matrix: [`sensing_modalities_viability_matrix.png`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/assets/sensing_modalities_viability_matrix.png)
* **Suggested Candidate Table**:
  | Subsystem | Component | Package | Active Power | Advantage |
  | :--- | :--- | :--- | :--- | :--- |
  | **ECG / Bio-Z** | TI **ADS1292R** | 32-QFN | $670\ \mu\text{W}$ | 24-bit $\Delta\Sigma$ ADC; integrated impedance engine |
  | **SCG / IMU** | ST **LSM6DSOX** | 14-LGA | $0.55\ \text{mA}$ | $60\ \mu\text{g}/\sqrt{\text{Hz}}$ noise floor; Machine Learning Core |
  | **PPG / $SpO_2$**| ADI **MAX86141**| 20-WLCSP| $1.2\ \text{mA}$ | 19-bit ADC; $>90\text{ dB}$ ambient light rejection |
  | **Acoustic PCG**| Knowles **SPH0645**| MEMS | $600\ \mu\text{A}$ | Direct 24-bit I2S digital audio output |
  | **MCU & BLE** | Nordic **nRF5340** | 94-aQFN | $3.2\ \text{mA}$ | Dual-core Cortex-M33 (128/64 MHz); BLE 5.3 |
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate table/specs and write finalized Block 5 text here ]
  ```

---

### BLOCK 6: Digitization Physics & Hardware FIFO Power Architecture (Phase 2.3)
* **Domain Lead**: Firmware / Embedded Systems
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🟢 [Q2_3 Takeaway Summary](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_3_Takeaway.md)
  * 🟡 [Q2_3 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_3_Product_Translation.md)
  * 🔵 [Phase 2.3 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.3_Sampling_Frequencies_Bit_Resolutions/Q2_3_Quantitative_Digitization_Architecture.md)
  * 🖼️ FIFO & DMA Diagram: [`embedded_event_driven_fifo_architecture.png`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/assets/embedded_event_driven_fifo_architecture.png)
* **Suggested Candidate Bullet Points**:
  * *Sub-Millisecond Timing*: 500 Hz sampling on ECG/PPG preserves clinical HRV HF-band and prevents $>2.1\text{ m/s}$ errors in arterial Pulse Wave Velocity (PWV).
  * *24-bit Quantization Physics*: Resolves $5\ \mu\text{V}$ ischemic ST-deviation over $\pm 300\text{ mV}$ half-cell skin battery offset ($<0.05\ \mu\text{V/LSB}$).
  * *Hardware FIFO Decoupling*: Sensors buffer in internal FIFOs; MCU sleeps in System ON ($<1.5\ \mu\text{A}$) 99% of the time, waking for 2 ms DMA bursts. Slashes power by 60%, delivering 7-14 day battery life on 150 mAh cell.
* **Suggested Visual**: Hardware FIFO watermark interrupt vs continuous polling power comparison curve.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate points and write finalized Block 6 text here ]
  ```

---

## 🟩 COLUMN 3: SIGNAL PROCESSING, AI & FALSE-ALARM REJECTION

### BLOCK 7: Signal Processing, Noise & Motion Denoising (Phase 3)
* **Domain Lead**: DSP / Biomedical
* **Status**: ⏳ **QUEUED FOR RESEARCH** (See [`Master_Research_Questionnaire_Expanded.md`](file:///c:/College/Ideathon/Master_Research_Questionnaire_Expanded.md) Phase 3)
* **Target Research Scope**:
  * *Analog AFE Filtering*: Passive RC anti-aliasing + active instrumentation notch filters.
  * *Adaptive Motion Cancellation*: Dual-IMU Normalized Least Mean Squares (NLMS) filter subtracting torso walking cadence from cardiac SCG.
  * *Real-Time SQI*: Sub-milliwatt Signal Quality Index gating uncorrupted frames.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to research Phase 3 and fill finalized Block 7 text here ]
  ```

---

### BLOCK 8: Edge AI, TinyML & Hierarchical Sentry Pipeline (Phases 4, 5, 6)
* **Domain Lead**: Machine Learning / Edge AI
* **Status**: ⏳ **QUEUED FOR RESEARCH** (See [`Master_Research_Questionnaire_Expanded.md`](file:///c:/College/Ideathon/Master_Research_Questionnaire_Expanded.md) Phases 4, 5, 6)
* **Suggested Candidate Architecture**:
  * *Stage 0 (Quiescent Surveillance - 95% of Day)*: Low-power ECG (250 Hz) + IMU hardware activity classifier ($4\ \mu\text{A}$). Total draw $<1.5\ \text{mW}$.
  * *Stage 1 (Diagnostic Burst - Event-Driven)*: Triggered on autonomic HRV crash ($SDNN < 50\text{ ms}$). Wakes 500 Hz SCG, PPG, and Bio-Z for 60 seconds to measure AO peak force decay and lung fluid $Z_0$.
  * *Stage 2 (Emergency Escalation)*: INT8 1D-CNN neural network verifies microvolt ST-shifts and T-wave alternans $\rightarrow$ triggers local haptics and cellular dispatch.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to research Phases 4-6 and fill finalized Block 8 text here ]
  ```

---

### BLOCK 9: Clinical False-Alarm Elimination Logic (Phase 1.4)
* **Domain Lead**: Clinical / Firmware
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🟢 [Q1.4 Takeaway Summary](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_4_Takeaway.md)
  * 🟡 [Q1.4 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_4_Product_Translation.md)
  * 🔵 [Phase 1.4 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.4_Differential_Diagnosis_Confounders/Q1_4_Differential_Diagnosis_Confounders.md)
* **Suggested Candidate Bullet Points**:
  * *Solving Alarm Fatigue*: Over 72% of hospital telemetry alarms are false; single-biomarker wearables cry wolf on panic and workouts.
  * *Multi-Modal Decoupling Rules*:
    * Panic Attacks: Tachycardia + hyperventilation, but thoracic bio-impedance is dry ($Z_0$ normal) and $SpO_2 \ge 99\%$ $\rightarrow$ Alarm suppressed.
    * Intense Exercise: Corroborated by high IMU cadence; cardiac contractility increases rather than decays $\rightarrow$ Alarm suppressed.
    * Vasovagal Syncope: Bradycardia without ST-deviation or lung fluid $\rightarrow$ Alarm suppressed.
  * *30-Second Patient Interlock*: Tactile cancellation window prevents false EMS calls.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate points and write finalized Block 9 text here ]
  ```

---

## 🟨 FOOTER ROW: MARKET VIABILITY, REGULATORY & COMPETITIVE MOAT

### BLOCK 10: Head-to-Head Competitive Moat Matrix
* **Domain Lead**: Business / Market Strategy
* **Status**: ✅ **COMPLETED RESEARCH (Synthesized across Phases 1 & 2)**
* **Suggested Candidate Comparison Table**:
  | Feature | Sternal Sentry | Apple Watch Ultra 2 | Whoop 4.0 / Oura | Hospital Holter | iRhythm Zio | Zoll LifeVest |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | **Early Warning Window** | **1 to 6 Hours Pre-Infarction**| None (Hour 0) | None (Recovery) | None (Retrospective) | None (Retrospective) | None (Post-arrest shock) |
  | **Anatomical Site** | **Sternal Breastbone** | Wrist | Wrist / Finger | Multi-wire Chest | Left Pectoral | Chest Harness |
  | **Mechanical SCG (Pump Stiffening)**| ✅ **Yes (AO Force)** | ❌ Impossible at wrist | ❌ No mechanical | ❌ No mechanical | ❌ No mechanical | ❌ No mechanical |
  | **Pulmonary Fluid (Bio-Z)** | ✅ **Yes ($Z_0$ Impedance)** | ❌ No lung access | ❌ No lung access | ❌ No Bio-Z | ❌ No Bio-Z | ❌ No Bio-Z |
  | **Ischemia Perfusion Resilience** | ✅ **High (71.3% sternal flow)**| ❌ Fails (>95% wrist drop)| ❌ Fails (>95% drop) | ✅ High (wires) | ✅ High (chest) | ✅ High (dry pads) |
  | **Real-Time Decision Latency** | **<1 Second On-Chip** | Arrhythmia only | None | **2 to 7 Days (Mailed)** | **7 to 14 Days (Mailed)**| Real-time shock |
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select competitor comparison table and write finalized Block 10 text here ]
  ```

---

### BLOCK 11: Market Beachhead, Health Economics & Reimbursement (Phase 12)
* **Domain Lead**: Health Economics / Business
* **Status**: ⏳ **CANDIDATE FRAMEWORKS COMPILED / OPEN FOR TEAM DECISION**
* **Suggested Candidate Points**:
  * *Beachhead Market*: Post-PCI (stent discharge) patients (1.8M US discharges/year). 30% of acute re-infarctions occur within 30 days.
  * *Established US Medicare Reimbursement*: Billed under existing Remote Patient Monitoring (RPM) CPT Codes:
    * CPT 99453 (Setup: $19) + CPT 99454 (Daily Telemetry: $56/mo) + CPT 99457 (Clinical Review: $51/mo). Prescribing clinics earn ~$107–$148/patient/month.
  * *Hospital ROI under HRRP*: Medicare penalizes hospitals for 30-day readmissions. Preventing just 5 emergency readmissions per 100 post-stent patients saves an institution >$250,000 in uncompensated ICU care.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select market sizing and write finalized Block 11 text here ]
  ```

---

### BLOCK 12: Regulatory Clearance Strategy & 3-Phase Clinical Roadmap (Phases 9–11)
* **Domain Lead**: Clinical / Regulatory
* **Status**: ⏳ **CANDIDATE FRAMEWORKS COMPILED / OPEN FOR TEAM DECISION**
* **Suggested Candidate Milestones**:
  * *US FDA Clearance*: Class II 510(k) Premarket Notification as Software as a Medical Device (SaMD), citing predicates iRhythm Zio Patch (K121319) and Bardy CAM (K172883).
  * *India CDSCO*: Class C Medical Device under MDR 2017.
  * *3-Phase Trial Roadmap*:
    * Phase A (Months 1-6): Retrospective training on PhysioNet PTB-XL (AUROC > 0.92 target).
    * Phase B (Months 7-12): 50-patient in-hospital Cardiac Care Unit (CCU) telemetry validation.
    * Phase C (Months 13-24): 300-patient multi-center post-PCI discharge ambulatory study.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select regulatory pathway and write finalized Block 12 text here ]
  ```
