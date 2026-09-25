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
  * 🌟 [Dual-Node Architecture Blueprint](file:///c:/College/Ideathon/Product_Design/Dual_Node_Pendant_and_Wristband_Architecture.md) *(Locked Team Selection)*
  * 🟢 [Q2.2 Takeaway Summary](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_2_Takeaway.md)
  * 🟡 [Q2.2 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_2_Product_Translation.md)
  * 🔵 [Phase 2.2 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.2_Anatomical_Sweet_Spots/Q2_2_Anatomical_Sweet_Spots.md)
  * 💡 [Form Factor Evaluation Study](file:///c:/College/Ideathon/Product_Design/Form_Factor_Evaluation_Pendant_vs_Patch.md)
  * 🖼️ Anatomical Diagram: [`optimal_anatomical_landmarks_telemetry.png`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/assets/optimal_anatomical_landmarks_telemetry.png)
* **Suggested Candidate Bullet Points**:
  * *Dual-Node BAN Innovation*: Sternal Sentry Pendant (Chest Node) + Companion PulseBand (Wrist Node) linked via BLE 5.3.
  * *100% Glue-Free Mounting*: Sentry Pendant held against lower sternal bone via soft tension cord (0.8 N preload) or compression undershirt pocket. Zero skin adhesives, zero skin irritation.
  * *Sternal Sweet Spot*: 4th Intercostal Space / LLSB directly over right ventricle and aortic root; captures pure mechanical cardiac recoil micro-vibrations (SCG).
  * *Pulse Transit Time (PTT)*: Synchronized delay between aortic valve opening on chest ($t_{\text{AO}}$) and radial pulse arrival on wrist ($t_{\text{wrist}}$) delivers continuous cuffless blood pressure and arterial stiffness.
* **Suggested Visual**: Dual-node diagram showing chest pendant and wristband communicating via BLE 5.3 with PTT pulse wave propagation.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate points and write finalized Block 4 text here ]
  ```

---

### BLOCK 5: Sensor Bill of Materials (BOM) & Dual-Node Hardware (Phase 2.1)
* **Domain Lead**: Embedded Hardware
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🌟 [Dual-Node Architecture Blueprint](file:///c:/College/Ideathon/Product_Design/Dual_Node_Pendant_and_Wristband_Architecture.md)
  * 🟢 [Q2.1 Takeaway Summary](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_1_Takeaway.md) | 🔵 [Phase 2.1 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.1_Sensing_Modalities_Biomarker_Mapping/Q2_1_Sensing_Modalities_Biomarker_Mapping.md)
  * 🟢 [Q2.4 Melanin Inclusivity Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_4_Takeaway.md) | 🔵 [Phase 2.4 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.4_Optical_Skin_Tone_Melanin_Inclusivity/Q2_4_Optical_Skin_Tone_Melanin_Inclusivity.md)
  * 🟢 [Q2.5 Electrode Physics Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_5_Takeaway.md) | 🔵 [Phase 2.5 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.5_Skin_Electrode_Interface_Impedance/Q2_5_Skin_Electrode_Interface_Impedance.md)
  * 🖼️ Modalities Matrix: [`sensing_modalities_viability_matrix.png`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/assets/sensing_modalities_viability_matrix.png)
* **Suggested Candidate Bullet Points**:
  * *Zero-Glue Biological Justification (Q2.5)*: Traditional Ag/AgCl hydrogel patches hit the "Day-5 Desiccation Wall" where water loss spikes contact impedance from $10\text{ k}\Omega$ to $>500\text{ k}\Omega$, collapsing CMRR below $65\text{ dB}$ and causing a 15–25% incidence of MARSI skin tears in elderly patients. Shifting to solid-state sternal SCG ($F = m \cdot a$) eliminates all adhesives and drying liquids.
  * *Fitzpatrick I–VI Optical Inclusivity (Q2.4)*: Dynamic closed-loop LED current control ($12\text{--}48\text{ mA}$) and programmable TIA gain eliminate occult hypoxemia bias, keeping SpO2 error $A_{\text{rms}} \le 1.6\%$ across all skin tones.
* **Suggested Candidate Table (Dual-Node Ecosystem - Total BOM ~₹820 / $10)**:
  | Node | Subsystem | Component | Package | Advantage & Function |
  | :--- | :--- | :--- | :--- | :--- |
  | **Pendant (Chest)** | **SCG / Kinematics** | ST **LSM6DSOX** | 14-LGA ($2.5\times 3\text{ mm}$) | $60\ \mu\text{g}/\sqrt{\text{Hz}}$ ultra-low noise; AO ejection force & LVET |
  | **Pendant (Chest)** | **Pendant Brain/BLE** | Nordic **nRF5340** | 94-aQFN ($7\times 7\text{ mm}$) | Dual-core Cortex-M33 (128/64 MHz); BLE 5.3 Isochronous Sync |
  | **Pendant (Chest)** | **Pendant Battery** | 150 mAh LiPo Cell | Micro-pouch | 5 to 7 days continuous mechanical telemetry |
  | **PulseBand (Wrist)**| **PPG / $SpO_2$** | ADI **MAX30102** | 14-OESIP ($5.6\times 3.3\text{ mm}$) | Dual-wavelength Red/IR pulse oximetry & peripheral pulse wave |
  | **PulseBand (Wrist)**| **Wrist Brain/BLE** | Nordic **nRF52840**| 73-aQFN ($7\times 7\text{ mm}$) | BLE 5.3 peripheral controller; arm gesture motion filtering |
  | **PulseBand (Wrist)**| **Display & Haptics** | 0.96" OLED + Motor | Modular | User alert screen & 30-second false-alarm cancellation interface |
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
* **Status**: ✅ **COMPLETED (Phase 3: Q3.1 through Q3.5 Fully Synthesized)**
* **Direct Evidence Links**:
  * 🟢 [Q3.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_1_Takeaway.md) | [Q3.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_2_Takeaway.md) | [Q3.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_3_Takeaway.md) | [Q3.4 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_4_Takeaway.md) | [Q3.5 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_5_Takeaway.md)
  * 🟡 [Q3.1 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_1_Product_Translation.md) | [Q3.2 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_2_Product_Translation.md) | [Q3.3 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_3_Product_Translation.md) | [Q3.4 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_4_Product_Translation.md) | [Q3.5 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_5_Product_Translation.md)
  * 🔵 [Phase 3 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/)
* **Suggested Candidate Bullet Points**:
  * *The Walking Noise Reality*: Footstrike impact transients ($1.5\text{ to }3.0\text{ g}$) occur at $1\text{--}2\text{ Hz}$, overlapping heart rate frequencies and swamping cardiac SCG micro-vibrations by $50\times\text{ to }100\times$ ($SNR = -20\text{ dB}$).
  * *Dual-Node NLMS Motion Cancellation (Route 3)*: Wristband IMU captures pure arm swings and footstep cadence as noise reference $x(n)$; on-device Normalized Least Mean Squares (NLMS) filter subtracts walking shockwaves, boosting sternal SCG clarity by $>26\text{ dB}$ consuming just $18.2\ \mu\text{W}$ ($14.2\ \mu\text{s}$ latency).
  * *Route 1 Digital DSP & On-Chip Rejection*: On-chip hardware anti-aliasing ($400\text{ Hz}$ LPF on LSM6DSOX) and $>90\text{ dB}$ ambient optical subtraction (MAX86141) strip static and lamp flicker; ARM CMSIS-DSP firmware handles bandpass filtering ($1\text{--}45\text{ Hz}$), keeping hardware sleek and under ₹820 BOM.
  * *Postural Gravity Normalization*: Continuous static gravity vector tracking ($0.05\text{ Hz}$) and tri-axial kinetic energy ($a_{\text{kinetic}} = \sqrt{a_x^2 + a_y^2 + a_z^2}$) prevent normal $48\%$ stroke volume drops upon standing or sleeping in Left Lateral Recumbent position from triggering false alarms.
  * *Sub-Milliwatt Signal Quality Index (SQI)*: Real-time higher-order Kurtosis/Skewness, spectral band energy, and template matching run in $<100\ \mu\text{s}$ consuming $<35\ \mu\text{W}$. Multi-Tier Gated Degradation suppresses noisy alarms while maintaining emergency cardiac arrest sentry surveillance 24/7.
* **Suggested Visual**: Dual-IMU NLMS adaptive cancellation diagram showing wrist reference subtracting footstrike shockwaves from sternal SCG + 3-Tier SQI Gating flowchart.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to review candidate points and write finalized Block 7 text here ]
  ```

---

### BLOCK 8: Data Engineering, Edge AI & TinyML Pipeline (Phases 4, 5, 6)
* **Domain Lead**: Machine Learning / Edge AI
* **Status**: ✅ **COMPLETED RESEARCH (Phases 4, 5, 6 Fully Synthesized)**
* **Direct Evidence Links**:
  * 🟢 [Phase 4 Takeaways Suite](file:///c:/College/Ideathon/Research_Dossier/Takeaways/) (Q4.1 through Q4.6)
  * 🟢 [Phase 5 Takeaways Suite](file:///c:/College/Ideathon/Research_Dossier/Takeaways/) (Q5.1 through Q5.5)
  * 🟢 [Phase 6 Takeaways Suite](file:///c:/College/Ideathon/Research_Dossier/Takeaways/) (Q6.1 through Q6.5)
  * 🟡 [Product Translations Directory](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/)
  * 🔵 [Phase 4 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_04_Data_Engineering_Preprocessing/) | [Phase 5 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_05_Feature_Engineering_Biomarkers/) | [Phase 6 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_06_Edge_ML_Architecture/)
* **Suggested Candidate Bullet Points**:
  * *3-Stage Cross-Modal Transfer Learning*: Solves the "No Wet ECG Electrodes" challenge by pre-training temporal 1D-CNN encoders on >40,000 hospital patients (PTB-XL, European ST-T, MIMIC-IV) and fine-tuning on synchronized SCG datasets (CEBS & SCG-RHC) to detect mechanical Aortic Opening (AO) force decay.
  * *Edge AI Architecture*: Hybrid Temporal 1D-CNN + Bidirectional LSTM + Multi-Head Self-Attention model ($142\text{k}$ parameters) extracts multi-scale morphology, beat-to-beat mechanical jitter, and long-range trend degradation.
  * *Sub-Milliwatt TinyML Execution*: Post-Training Quantization (PTQ) to int8 via CMSIS-NN; runs on Nordic nRF5340 application core (Cortex-M33 @ 128 MHz) with $<42\text{ ms}$ inference latency, consuming just $1.64\text{ mA}$ burst current ($<180\text{ KB}$ Flash, $<64\text{ KB}$ RAM footprint).
  * *Zero-Data Leakage Guarantee*: Rejects flawed beat-wise splitting (which inflates accuracy to 99% before crashing to 52%). Uses Stratified Group 5-Fold validation by Patient ID combined with an adversarial Gradient Reversal Layer ($I(\mathbf{z}; S) \rightarrow 0$) that strips individual chest anatomical acoustic fingerprints.
  * *3-Zone Risk Engine + Countdown*: Quiescent ($>3\text{h}$), Incubation ($1\text{--}3\text{h}$, gentle haptic wrist tap), and Critical ($<60\text{m}$, audible tone + 911 dispatch) states with continuous DeepSurv pre-infarction countdown.
* **Suggested Visual**: Hybrid 1D-CNN-BiLSTM-Attention architecture diagram + Nordic nRF5340 dual-core IPC execution flow + 3-Zone clinical risk timeline.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to review candidate points and write finalized Block 8 text here ]
  ```

---

### BLOCK 9: Clinical False-Alarm Elimination Logic (Phase 1.4 & Phase 9.1)
* **Domain Lead**: Clinical / Firmware
* **Status**: ✅ **COMPLETED RESEARCH**
* **Direct Evidence Links**:
  * 🟢 [Q1.4 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_4_Takeaway.md) | [Q9.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q9_1_Takeaway.md)
  * 🟡 [Q1.4 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_4_Product_Translation.md) | [Q9.1 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q9_1_Product_Translation.md)
  * 🔵 [Phase 1.4 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.4_Differential_Diagnosis_Confounders/Q1_4_Differential_Diagnosis_Confounders.md) | [Phase 9.1 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_09_Clinical_Safety_Regulatory_Viability/9.1_Alarm_Fatigue_Calibration/Q9_1_Alarm_Fatigue_Calibration.md)
* **Suggested Candidate Bullet Points**:
  * *Solving Alarm Fatigue*: Over 72% of hospital telemetry alarms are false; single-biomarker wearables cry wolf on panic and workouts.
  * *Multi-Modal Decoupling Rules*:
    * *Panic Attacks*: Heart rate surges to $140\text{ bpm}$ with hyperventilation, but thoracic bio-impedance is dry ($Z_0$ normal), $SpO_2 \ge 99\%$, and SCG mechanical contractility is hyperdynamic ($\uparrow\text{AO}$) $\rightarrow$ Alarm suppressed.
    * *Intense Exercise*: High IMU cadence ($>120\text{ spm}$); wrist NLMS subtracts motion noise; cardiac contractility increases rather than decays $\rightarrow$ Alarm suppressed.
    * *Vasovagal Syncope*: Rapid bradycardia without mechanical stiffening or lung fluid $\rightarrow$ Classified as benign syncope.
  * *30-Second Patient Interlock*: Azoteq capacitive touch cancel slider on wristband allows conscious users to dismiss benign false alarms before external cellular dispatch.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select candidate points and write finalized Block 9 text here ]
  ```

---

## 🟨 FOOTER ROW: MARKET VIABILITY, REGULATORY & COMPETITIVE MOAT

### BLOCK 10: Head-to-Head Competitive Moat Matrix
* **Domain Lead**: Business / Market Strategy
* **Status**: ✅ **COMPLETED RESEARCH (Verified across all 12 Phases)**
* **Suggested Candidate Comparison Table**:
  | Feature | Sternal Sentry + PulseBand | Apple Watch Ultra 2 | Whoop 4.0 / Oura | Hospital Holter | iRhythm Zio Patch | ZOLL LifeVest |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | **Early Warning Window** | **1 to 6 Hours Pre-Infarction**| None (Hour 0) | None (Recovery) | None (Retrospective) | None (Retrospective) | None (Post-arrest shock) |
  | **Anatomical Site** | **Dual-Node: Sternum + Wrist** | Wrist only | Wrist / Finger | Multi-wire Chest | Left Pectoral | Heavy Chest Harness |
  | **Skin Adhesive / Glue** | ❌ **ZERO GLUE (Soft Cord/Dock)**| ❌ Strap (wrist only) | ❌ Band (wrist only) | ⚠️ Sticky Hydrogel Pads| ⚠️ Acrylic Adhesive Pad | ⚠️ Elastic Belt + Gel |
  | **Mechanical SCG (Pump Stiffening)**| ✅ **Yes (Aortic Opening Force)**| ❌ Impossible at wrist | ❌ No mechanical | ❌ No mechanical | ❌ No mechanical | ❌ No mechanical |
  | **Continuous Cuffless BP (PTT)**| ✅ **Yes (Sternal-to-Radial PTT)**| ❌ No PTT | ❌ No PTT | ❌ No PTT | ❌ No PTT | ❌ No PTT |
  | **Ischemia Perfusion Resilience** | ✅ **High (71.3% sternal flow)**| ❌ Fails (>95% wrist drop)| ❌ Fails (>95% drop) | ✅ High (wires) | ✅ High (chest) | ✅ High (dry pads) |
  | **Decision Latency & Action** | **<42 ms On-Chip $\rightarrow$ 911 SOS**| Arrhythmia alert only | Sleep recovery score | **2 to 7 Days (Mailed)** | **7 to 14 Days (Mailed)**| Defibrillates post-VF |
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select competitor comparison table and write finalized Block 10 text here ]
  ```

---

### BLOCK 11: Market Beachhead, Health Economics & Reimbursement (Phase 12)
* **Domain Lead**: Health Economics / Business
* **Status**: ✅ **COMPLETED RESEARCH (Phase 12: Q12.1, Q12.2, Q12.3 Fully Synthesized)**
* **Direct Evidence Links**:
  * 🟢 [Q12.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q12_1_Takeaway.md) | [Q12.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q12_2_Takeaway.md) | [Q12.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q12_3_Takeaway.md)
  * 🟡 [Q12.1 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q12_1_Product_Translation.md) | [Q12.2 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q12_2_Product_Translation.md) | [Q12.3 Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q12_3_Product_Translation.md)
  * 🔵 [Phase 12.1 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_12_Health_Economics_Market_Pitch/12.1_Health_Economics_Cost_Per_QALY/Q12_1_Cost_Per_QALY_Health_Economics.md) | [Phase 12.2 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_12_Health_Economics_Market_Pitch/12.2_Beachhead_Target_Market_TAM/Q12_2_Initial_Beachhead_Target_Market_TAM.md) | [Phase 12.3 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_12_Health_Economics_Market_Pitch/12.3_Unit_Economics_Business_Model/Q12_3_Sustainable_Unit_Economics_Business_Model.md)
* **Suggested Candidate Points**:
  * *Health Economics & Cost per QALY (Q12.1)*: Markov modeling demonstrates a **Dominant ICER ($-\$64,025/\text{QALY}$)**. Converting unannounced OHCA into elective catheterization saves **$\$437,400\text{ per patient}$** over 5 years and adds **$+6.45\text{ QALYs}$**. Medicare HRRP shield prevents $\$2.33\text{M}$ in 30-day readmission penalties ($10.9\times\text{ ROI}$) for a 400-bed hospital.
  * *Initial Beachhead TAM (Q12.2)*: Rejects the retail D2C consumer trap ($<0.1\%$ prevalence collapses PPV to $<2\%$). Focuses on 3 ultra-high-risk hospital discharge cohorts: (1) Post-PCI 30-day stent thrombosis peak (Days 3–14), (2) 40-to-90-day guideline-mandated ICD Waiting Gap ($2.1\%\text{--}4.5\%$ SCA risk in LVEF $\le 35\%$), and (3) Diabetic silent ischemia. Total Addressable Market: $\$144\text{B}$; Serviceable Addressable Market: $\$3.06\text{B}$ (6.8M annual patients); SOM Beachhead: $\$49.0\text{M ARR}$ in Year 3.
  * *Sustainable Unit Economics & Medicare Reimbursement (Q12.3)*: Kit BOM COGS is **$\$33.50$** (Pendant $\$18.50$, PulseBand $\$15.00$); reusable silicone allows 6 patient cycles, reducing hardware cost to **$\$5.58/\text{patient}$**. Billed under active 2024 Medicare RPM codes (CPT 99453 [\$19.65], CPT 99454 [\$46.50], CPT 99457 [\$48.13]) generating $\$114.28/\text{month}$. B2B2C turnkey fee of $\$65/\text{month}$ leaves prescribing clinics with **$\$49.28/\text{month}$ recurring profit per patient** ($43.1\%$ margin; $\$295\text{k/yr}$ for 500 patients).
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select market sizing and write finalized Block 11 text here ]
  ```

---

### BLOCK 12: Regulatory Clearance Strategy, Safe-State Architecture & Clinical Roadmap (Phases 9–11)
* **Domain Lead**: Clinical / Regulatory / Systems Reliability
* **Status**: ✅ **COMPLETED RESEARCH (Phases 9, 10, 11 Fully Synthesized)**
* **Direct Evidence Links**:
  * 🟢 [Phase 9 Takeaways](file:///c:/College/Ideathon/Research_Dossier/Takeaways/) | [Phase 10 Takeaways](file:///c:/College/Ideathon/Research_Dossier/Takeaways/) | [Phase 11 Takeaways](file:///c:/College/Ideathon/Research_Dossier/Takeaways/)
  * 🟡 [Product Translations Directory](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/)
  * 🔵 [Phase 9 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_09_Clinical_Safety_Regulatory_Viability/) | [Phase 10 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_10_Human_Factors_Ergonomics/) | [Phase 11 Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_11_Failure_Modes_Failsafes/)
* **Suggested Candidate Milestones & Safety Architecture**:
  * *Regulatory Pathway (Q9.2)*: US FDA Class II 510(k) Premarket Notification as Software as a Medical Device (SaMD), citing predicates iRhythm Zio (K121319) and ZOLL LifeVest (K140817); India CDSCO Class C Medical Device under MDR 2017.
  * *Patient Adherence & Ergonomics (Q10.1–Q10.3)*: 100% Zero-Glue silicone dock/pendant avoids the 15–25% MARSI skin tear rate; non-intrusive pendant form factor prevents cardiophobia and sleep disruption; Azoteq capacitive touch 30-second cancellation interface stops false 911 calls.
  * *Deterministic Safe-State Architecture (Q11.1–Q11.2)*: ISO 14971 / IEC 60812 FMEA, 9-clock I2C bus recovery, P-MOSFET sensor power cycling, IEC 62304 Class C TrustZone hardware security, 4.0s–8.0s Windowed Watchdog on independent 32.768 kHz LFRC, and zero-heap MISRA-C:2012 Rule 21.3 compliance.
  * *Supercapacitor "Dying Gasp" SOS (Q11.3)*: Murata 47 mF / 5.5V supercapacitor (DMF3Z5R5H474M3DTA0) stores $158.2\text{ mJ}$ ($10.18\times$ required margin); automatically isolates via P-FET upon battery drop, powering BLE 5.3 Coded PHY Long Range (+8 dBm) SOS beacon and 75 dB resonant acoustic buzzer even at 0% main battery.
  * *3-Phase Trial Roadmap (Q9.5)*:
    * Phase A (Months 1–6): In-silico validation on PTB-XL & MIMIC-IV ($N > 40,000$, target AUROC $> 0.92$).
    * Phase B (Months 7–12): 50-patient in-hospital Cardiac Care Unit (CCU) telemetry trial during balloon angioplasty.
    * Phase C (Months 13–24): 300-patient multi-center post-PCI ambulatory trial across US and Indian hospitals.
* **✍️ `[Team Final Poster Text - Fill / Customize Here]`**:
  ```markdown
  [ Team to select regulatory pathway and write finalized Block 12 text here ]
  ```

