# Master Product & Research Hub: Ideathon Systems Guide
## Autonomous Sternal Medical IoT Wearable for Early Prediction of Sudden Cardiac Arrest (SCA) & Acute Ischemia

---

> **Purpose**: This Master Hub is the central architectural roadmap, navigation guide, and decision framework for our College Medical IoT Ideathon project.  
> **Core Instruction**: This document **does not** assume or lock in final decisions for the team. Instead, it provides the universal ideathon evaluation rubric at the top, guides the team to the exact research files and candidate evidence already compiled across our 4-tier repository, and leaves modular blanks so team members can fill in and customize each component domain by domain.  
> **Repository Path**: `c:/College/Ideathon/`  
> **Last Synchronized**: 2026-09-24

---

## 🏆 SECTION 1: What Ideathons Are Usually Judged On
*(The Universal Medical IoT Evaluation Rubric & Judge Psychology)*

Medical IoT and healthcare engineering ideathons are typically evaluated by a multidisciplinary panel comprising **cardiologists/physicians, embedded hardware engineers, biomedical researchers, and venture capital/health economists**. 

Understanding their evaluation criteria and scoring weights ensures the team allocates its focus where competitions are won or lost:

```
===================================================================================================================
                                IDEATHON EVALUATION SCORING WEIGHTS & CRITERIA
===================================================================================================================

  [1. CLINICAL NEED & PROBLEM IMPACT] ────────► 20% - 25%   (The Severity of the Unmet Need & Clinical Gap)
  [2. NOVELTY & COMPETITIVE MOAT]     ────────► 20% - 25%   (Why Existing Wearables & Hospitals Physically Fail)
  [3. TECHNICAL FEASIBILITY & ARCH]   ────────► 20% - 25%   (Biophysics, Sensor Choice, False Alarms & Power)
  [4. BUSINESS MODEL & HEALTH ECON]   ────────► 15% - 20%   (Reimbursement CPT Codes, Beachhead Market & ROI)
  [5. PRESENTATION & Q&A DEFENSE]     ────────► 10% - 15%   (Pitch Clarity, Domain Ownership & Handling Skepticism)

===================================================================================================================
```

### 1. Clinical Need & Problem Impact (20% – 25% Weight)
* **What Judges Look For**:
  * Is this an urgent, life-threatening problem or a trivial "nice-to-have" fitness feature?
  * The magnitude of societal mortality, morbidity, and healthcare costs.
  * **The "Why Now?" & The Care Gap**: What specific gap exists between when the biological catastrophe begins and when current medicine responds?
* **Common Pitfalls**:
  * Targeting general wellness or vague anxiety rather than a clearly defined lethal clinical endpoint.
  * Quoting generic statistics without identifying the specific anatomical breakdown.

### 2. Novelty, Uniqueness & The Competitive Moat (20% – 25% Weight)
* **What Judges Look For**:
  * Is this a true scientific/engineering breakthrough, or just another generic smartwatch clone?
  * **The Defensibility / Physics Moat**: Why can't Apple, Samsung, Whoop, or hospital Holters simply release a software update to do what you do? (e.g., wrist vasoconstriction during shock, lack of bone transmission for mechanical recoil, absence of thoracic fluid measurement).
  * Unique intellectual contribution (e.g., intercepting the 1-to-6-hour pre-infarction ischemic countdown before electrical collapse).
* **Common Pitfalls**:
  * Claiming *"We have no competitors"* (judges instantly penalize this).
  * Failing to explain why wrist wearables physically cannot replace chest-placed sensing.

### 3. Technical Feasibility & Systems Architecture (20% – 25% Weight)
* **What Judges Look For**:
  * Is the proposed solution physically and biologically plausible, or is it hand-waving science fiction?
  * Real Commercial Off-The-Shelf (COTS) chips vs hypothetical components.
  * **False-Alarm Rejection & Clinical Reliability**: How does the system avoid "alarm fatigue"? How does it decouple panic attacks, exercise, and sleep transitions from true heart attacks?
  * **Embedded Realism**: Sampling rates, ADC bit resolutions, microcontroller sleep states, and battery life calculations.
* **Common Pitfalls**:
  * Hand-waving: *"We'll just feed all sensor data into an AI in the cloud"* (ignoring latency, cellular dead zones, battery drain, and motion noise).
  * Ignoring motion artifacts and half-cell skin battery potentials.

### 4. Market Viability, Business Model & Health Economics (15% – 20% Weight)
* **What Judges Look For**:
  * **The Beachhead Market**: A tightly defined, high-risk patient group (e.g., 30-day post-stent discharge) rather than a vague "everyone over 50".
  * **Who Actually Pays?**: Clear reimbursement mechanics (e.g., existing US Medicare Remote Patient Monitoring CPT codes) rather than expecting patients to pay out-of-pocket.
  * **Hospital ROI**: How adopting this device saves hospitals money under readmission penalties (e.g., HRRP).
* **Common Pitfalls**:
  * Assuming insurance will immediately cover an unproven consumer gadget.
  * Projecting unrealistic consumer adoption without physician prescription pathways.

### 5. Presentation Clarity, Domain Ownership & Q&A Defense (10% – 15% Weight)
* **What Judges Look For**:
  * Can the team deliver a gripping, jargon-free hook within the first 60 seconds?
  * Clear domain ownership: Does each team member master their respective domain (Hardware, Firmware/AI, Clinical, Business) during judge questioning?
  * Confident, respectful defense backed by peer-reviewed evidence when judges try to poke holes in the idea.
* **Common Pitfalls**:
  * One team member answering all questions while others stand silent.
  * Getting defensive or evasive when a judge points out a technical trade-off.

---

## 🧭 SECTION 2: Repository Architecture & How to Use This Hub

This repository is organized into a **4-Tier Information Architecture** so team members can move seamlessly from quick 5-minute overviews down to raw clinical citations:

```
c:/College/Ideathon/
├── MASTER_PRODUCT_AND_RESEARCH_HUB.md   <-- 🌟 TIER 1: Master Navigation Guide & Ideathon Scaffold (This File)
│
├── Research_Dossier/
│   ├── Takeaways/                       <-- 🟢 TIER 2: Fast Plain-English Summaries (5-Min Reads)
│   │   ├── Q1_1_Takeaway.md
│   │   ├── Q1_2_Takeaway.md
│   │   └── ... (All completed questions)
│   │
│   ├── Product_Translations/            <-- 🟡 TIER 2.5: Product Implementation & Engineering "How & Why"
│   │   ├── Q1_1_Product_Translation.md
│   │   ├── Q1_2_Product_Translation.md
│   │   └── ... (All completed questions)
│   │
│   ├── Phase_01_Pathophysiology.../     <-- 🔵 TIER 3: Deep Research Vault (Equations, Trials, Citations)
│   │   ├── 1.1_Pre_Infarction_Cascade/
│   │   └── ...
│   └── Phase_02_Signal_Acquisition.../
│       ├── 2.1_Sensing_Modalities.../
│       ├── 2.2_Anatomical_Sweet_Spots/
│       ├── 2.3_Sampling_Frequencies.../
│       └── assets/                      <-- Schematics, anatomical diagrams, FIFO architectures
│
├── Product_Design/                      <-- 💡 Product Concepts, Trade-Off Studies & Fixed vs Flexible Rules
│   ├── Master_Fixed_vs_Flexible_Architecture.md
│   └── Form_Factor_Evaluation_Pendant_vs_Patch.md
│
└── Master_Research_Questionnaire_Expanded.md <-- Master 12-Phase Roadmap (All Questions)
```

### Team Navigation Rules:
1. **Never Assume — Fill One by One**: Sections below are structured into modular blocks. For researched areas, we provide the candidate findings and direct links to our dossiers; the team selects what to use. For unresearched phases, questions are queued for future research.
2. **Assign Domains**: Divide the modules among team members based on background (Biomedical, Embedded Hardware, Data Science/AI, Business/Pitch).
3. **Reference Layering**:
   - Need a quick high-level understanding? Read the **Tier 2 Takeaway** (`Takeaways/`).
   - Need to know how we implement it in hardware/code? Read the **Tier 2.5 Product Translation** (`Product_Translations/`).
   - Need exact numbers, formulas, or papers to defend against a skeptical judge? Read the **Tier 3 Deep Research** (`Phase_XX/`).

---

## 📋 SECTION 3: Ideathon Product Modules & Navigation Directory

---

### MODULE 1: The Clinical Crisis, Care Gap & Biological Countdown
* **Ideathon Evaluation Role**: Hooks judges in the first 60 seconds (Pillar 1: Clinical Need & Impact).
* **Research Phase**: **Phase 1 (Pathophysiology & Biomarker Discovery)**
* **Current Status**: **COMPLETED RESEARCH (Available on Disk)**

#### 📁 Direct File Reference Links:
* **The 1-to-6-Hour Pre-Infarction Countdown (Q1.1)**:
  * 🟢 Plain-English Takeaway: [`Q1_1_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_1_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q1_1_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_1_Product_Translation.md)
  * 🔵 Deep Clinical Vault: [`Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md)
  * 📄 Clinical Context Addendum: [`Clinical_Realities_Hospital_Barriers_and_MI_Types.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Clinical_Realities_Hospital_Barriers_and_MI_Types.md)
* **Non-Invasive Physical Outputs & Measurable Biometrics (Q1.2)**:
  * 🟢 Plain-English Takeaway: [`Q1_2_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_2_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q1_2_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_2_Product_Translation.md)
  * 🔵 Deep Clinical Vault: [`Q1_2_Non_Invasive_Physical_Outputs.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.2_Non_Invasive_Physical_Outputs/Q1_2_Non_Invasive_Physical_Outputs.md)

#### 🔬 Candidate Evidence & Key Insights Available for the Team:
* **The Clinical Problem**: 70% to 80% of sudden non-traumatic cardiac arrests in adults stem directly from acute myocardial ischemia (coronary blood starvation). 90% of out-of-hospital arrests die before reaching help; permanent anoxic brain death starts in 4 minutes.
* **The Healthcare Blind Spot**:
  * Smartwatches only detect events *after* electrical collapse (Hour 0), when the patient is already unconscious.
  * Hospitals can clear blocked arteries, but patients arrive 2 to 4 hours post-infarction—after irreversible cellular necrosis has occurred.
* **The 1-to-6-Hour Physiological Cascade**:
  * *Hour 6 to 3*: Sympathetic autonomic surge $\rightarrow$ Loss of Heart Rate Variability (HRV), cold diaphoresis (sweating).
  * *Hour 3 to 1*: Myocardial ATP depletion $\rightarrow$ Diastolic & systolic mechanical contractility drops $>50\%$ (measurable via Seismocardiography).
  * *Hour 2 to 0.5*: Left-ventricular backward pressure $\rightarrow$ Pulmonary interstitial edema (measurable via Thoracic Bio-Impedance).
  * *Hour 1 to 0*: Microvolt ST-segment depression/elevation, T-wave alternans $\rightarrow$ Ventricular Fibrillation (SCA).

#### ✍️ `[Team Decision & Customization Slot - Module 1]`:
*(Team members handling Clinical Need: Select which statistics, timeline diagrams, and opening hook phrases to place on the competition poster and pitch slide.)*
* **Selected Problem Statement**: `[ Team to fill / customize ]`
* **Selected Statistics for Poster Hook**: `[ Team to fill / customize ]`
* **Selected Timeline Graphic**: `[ Team to fill / customize ]`

---

### MODULE 2: The Physical Solution, Anatomical Site & Form Factor
* **Ideathon Evaluation Role**: Introduces the device concept and defends anatomical placement (Pillars 2 & 3: Novelty & Feasibility).
* **Research Phase**: **Phase 2 (Signal Acquisition) + Product Design**
* **Current Status**: **COMPLETED RESEARCH (Available on Disk)**

#### 📁 Direct File Reference Links:
* **Anatomical Sweet Spots & Sternal Physics (Q2.2)**:
  * 🟢 Plain-English Takeaway: [`Q2_2_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_2_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q2_2_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_2_Product_Translation.md)
  * 🔵 Deep Physics Vault: [`Q2_2_Anatomical_Sweet_Spots.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.2_Anatomical_Sweet_Spots/Q2_2_Anatomical_Sweet_Spots.md)
  * 📄 Anatomical Optimization Addendum: [`Anatomical_Optimization_for_Cardiovascular_Telemetry.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.2_Anatomical_Sweet_Spots/Anatomical_Optimization_for_Cardiovascular_Telemetry.md)
  * 🖼️ Anatomical Diagram Asset: [`optimal_anatomical_landmarks_telemetry.png`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/assets/optimal_anatomical_landmarks_telemetry.png)
* **Form Factor Trade-Offs & Architecture Rules**:
  * 🌟 **Team Architecture Blueprint**: [`Dual_Node_Pendant_and_Wristband_Architecture.md`](file:///c:/College/Ideathon/Product_Design/Dual_Node_Pendant_and_Wristband_Architecture.md) *(Locked Team Selection)*
  * 💡 Pendant vs Adhesive Patch Analysis: [`Form_Factor_Evaluation_Pendant_vs_Patch.md`](file:///c:/College/Ideathon/Product_Design/Form_Factor_Evaluation_Pendant_vs_Patch.md)
  * 🔒 Locked Science vs Open Choices: [`Master_Fixed_vs_Flexible_Architecture.md`](file:///c:/College/Ideathon/Product_Design/Master_Fixed_vs_Flexible_Architecture.md)

#### 🔬 Candidate Evidence & Key Insights Available for the Team:
* **The Selected Dual-Node Ecosystem (Pendant + PulseBand)**:
  * **Chest Node**: 38 mm Sentry Pendant mounted on an adjustable tension cord (100% GLUE-FREE, ZERO ECG electrodes). Houses ultra-low-noise 6-axis IMU (LSM6DSOX) for Seismocardiography (SCG) mechanical contractility and Aortic Opening (AO) force tracking.
  * **Wrist Node**: Companion PulseBand with optical PPG (MAX30102 / MAX86141) measuring $SpO_2$, pulse rate, PRV, arm-motion filtering, and a haptic display interface.
  * **Dual-Node PTT**: Time difference between sternal aortic valve opening ($t_{\text{AO}}$) and radial pulse arrival ($t_{\text{wrist}}$) delivers continuous cuffless arterial stiffness.
* **Why Traditional Hospital Patches Fail**: Low adherence—patients hate wearing large, itchy, white adhesive medical tape in social/work settings.
* **The Anatomical Sweet Spot**: Mid-to-lower sternal body (4th Intercostal Space / LLSB) directly over the right ventricle and aortic root; offers maximal bone acoustic transmission.

#### ✍️ `[Team Decision & Customization Slot - Module 2]`:
* **Device Form Factor Decision**: **OFFICIALLY SELECTED**: Dual-Node Body Area Network (Sentry Pendant + Companion PulseBand, No ECG, Zero Glue).
* **Industrial Design / Material Choices**: `[ Team to fill: Titanium rim vs Zirconia ceramic vs Polycarbonate ]`
* **Anatomical Placement Diagram for Poster**: `[ Team to select ]`

---

### MODULE 3: Multi-Modal Sensing, Digitization & Hardware Architecture
* **Ideathon Evaluation Role**: Proves technical feasibility and engineering rigor (Pillar 3: Technical Feasibility).
* **Research Phase**: **Phase 2 (Signal Acquisition Modalities)**
* **Current Status**: **COMPLETED RESEARCH (Available on Disk)**

#### 📁 Direct File Reference Links:
* **COTS Sensor Component Selection (Q2.1)**:
  * 🟢 Plain-English Takeaway: [`Q2_1_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_1_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q2_1_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_1_Product_Translation.md)
  * 🔵 Deep Engineering Vault: [`Q2_1_Sensing_Modalities_Biomarker_Mapping.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.1_Sensing_Modalities_Biomarker_Mapping/Q2_1_Sensing_Modalities_Biomarker_Mapping.md)
  * 🖼️ Modalities Matrix Asset: [`sensing_modalities_viability_matrix.png`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/assets/sensing_modalities_viability_matrix.png)
* **Sampling Frequencies, Bit Resolutions & Hardware FIFO (Q2.3)**:
  * 🟢 Plain-English Takeaway: [`Q2_3_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_3_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q2_3_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_3_Product_Translation.md)
  * 🔵 Deep Digitization Vault: [`Q2_3_Quantitative_Digitization_Architecture.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.3_Sampling_Frequencies_Bit_Resolutions/Q2_3_Quantitative_Digitization_Architecture.md)
  * 🖼️ FIFO & DMA Architecture Asset: [`embedded_event_driven_fifo_architecture.png`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/assets/embedded_event_driven_fifo_architecture.png)
* **Optical Skin Tone & Melanin Inclusivity across Fitzpatrick Types I-VI (Q2.4)**:
  * 🟢 Plain-English Takeaway: [`Q2_4_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_4_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q2_4_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_4_Product_Translation.md)
  * 🔵 Deep Optical Physics Vault: [`Q2_4_Optical_Skin_Tone_Melanin_Inclusivity.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.4_Optical_Skin_Tone_Melanin_Inclusivity/Q2_4_Optical_Skin_Tone_Melanin_Inclusivity.md)
* **Skin-Electrode Interface Physics & Impedance Drift (Q2.5)**:
  * 🟢 Plain-English Takeaway: [`Q2_5_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_5_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q2_5_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_5_Product_Translation.md)
  * 🔵 Deep Interface Physics Vault: [`Q2_5_Skin_Electrode_Interface_Impedance.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.5_Skin_Electrode_Interface_Impedance/Q2_5_Skin_Electrode_Interface_Impedance.md)

#### 🔬 Candidate Evidence & Key Insights Available for the Team:
* **The 5 Synchronized Sensing Channels**:
  1. *Electrical (ECG)*: Texas Instruments **ADS1292R** (24-bit $\Delta\Sigma$ ADC, low-power AFE). Resolves $5\ \mu\text{V}$ ischemia against $\pm 300\text{ mV}$ half-cell skin battery offset.
  2. *Mechanical Kinematics (SCG)*: STMicroelectronics **LSM6DSOX** (6-axis IMU, $60\ \mu\text{g}/\sqrt{\text{Hz}}$ ultra-low noise). Captures Aortic Opening (AO) force decay and Pre-Ejection Period (PEP).
  3. *Optical Microvascular (PPG / $SpO_2$)*: Analog Devices **MAX86141** (19-bit ADC, $>90\text{ dB}$ ambient light rejection, dual-wavelength Red/IR).
  4. *Acoustic Heart Sounds (PCG)*: Knowles **SPH0645LM4H** (Digital MEMS microphone, direct 24-bit I2S output). Captures $S_3/S_4$ ischemic gallops.
  5. *Thoracic Fluid (Bio-Z)*: Integrated tetrapolar impedance engine in **ADS1292R** ($55\text{ mm}$ spacing, measuring base thoracic impedance $Z_0$).
* **Digitization & Embedded Timing Physics**:
  * 500 Hz sampling on ECG/PPG provides sub-millisecond fiducial precision (preventing $>2.1\text{ m/s}$ errors in Pulse Wave Velocity arterial stiffness).
  * Hardware FIFOs buffer data so the Nordic **nRF5340** MCU sleeps in System ON ($<1.5\ \mu\text{A}$) 99% of the time, waking for 2 ms DMA bursts—cutting power by 60% and enabling 7-14 day battery life.

#### ✍️ `[Team Decision & Customization Slot - Module 3]`:
*(Team members handling Embedded Hardware: Select BOM components, system block diagram, and power optimization claims for presentation.)*
* **Selected Component BOM**: `[ Team to confirm / customize ]`
* **System Hardware Block Diagram**: `[ Team to finalize ]`
* **Power Budget & Battery Life Target**: `[ Team to fill / customize ]`

---

### MODULE 4: Clinical Inclusivity, Demographics & Circadian Intelligence
* **Ideathon Evaluation Role**: Shows clinical depth and personalized medicine (Pillar 1: Clinical Need & Impact).
* **Research Phase**: **Phase 1 (Pathophysiology & Biomarker Discovery)**
* **Current Status**: **COMPLETED RESEARCH (Available on Disk)**

#### 📁 Direct File Reference Links:
* **Demographic Variations — Diabetics, Elderly, Sex Differences (Q1.3)**:
  * 🟢 Plain-English Takeaway: [`Q1_3_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_3_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q1_3_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_3_Product_Translation.md)
  * 🔵 Deep Clinical Vault: [`Q1_3_Demographic_Variations.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.3_Demographic_Variations/Q1_3_Demographic_Variations.md)
* **Circadian Vulnerability & Sleep-Stage Adaptations (Q1.5)**:
  * 🟢 Plain-English Takeaway: [`Q1_5_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_5_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q1_5_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_5_Product_Translation.md)
  * 🔵 Deep Chronobiology Vault: [`Q1_5_Circadian_Sleep_Adaptations.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.5_Circadian_Sleep_Adaptations/Q1_5_Circadian_Sleep_Adaptations.md)

#### 🔬 Candidate Evidence & Key Insights Available for the Team:
* **The Diabetic "Silent Ischemia" Moat**: Autonomic cardiac neuropathy blunts pain nerves in 30% to 40% of diabetic patients; they experience painless heart attacks. Single-sensor devices fail them. Our device uses mechanical contractility loss (SCG) and lung fluid backpressure (Bio-Z) to detect silent ischemia without relying on patient symptoms.
* **Elderly & Baseline Adaptation**: Stiff arteries and low baseline HRV in older adults fool static algorithms. We implement dynamic personalized baselines using rolling 72-hour $Z$-score normalization.
* **Circadian Morning Vulnerability (6:00 AM – 12:00 PM)**: Peak time for sudden cardiac deaths due to cortisol awakening surge, blood pressure elevation, and platelet hyper-reactivity. System dynamically adjusts sensitivity thresholds during this window.
* **Sleep-Stage Discrimination**: Decouples benign REM-dream tachycardia from nocturnal ischemia and obstructive sleep apnea desaturations.

#### ✍️ `[Team Decision & Customization Slot - Module 4]`:
*(Team members handling Clinical / Algorithm Design: Select demographic features to emphasize on poster/pitch.)*
* **Selected Demographic Highlight**: `[ Team to select: Diabetic Silent Ischemia vs Circadian Morning Peak ]`
* **Personalization Algorithm Description**: `[ Team to fill / customize ]`

---

### MODULE 5: Clinical Reliability & False-Alarm Rejection Logic
* **Ideathon Evaluation Role**: Proves to physician judges that the device will not cause "alarm fatigue" (Pillars 3 & 5: Feasibility & Defense).
* **Research Phase**: **Phase 1 (Pathophysiology) + Phase 3 (Signal Processing)**
* **Current Status**: **COMPLETED RESEARCH (Available on Disk)**

#### 📁 Direct File Reference Links:
* **Differential Diagnosis & Confounder Decoupling Rules (Q1.4)**:
  * 🟢 Plain-English Takeaway: [`Q1_4_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_4_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q1_4_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_4_Product_Translation.md)
  * 🔵 Deep Clinical Vault: [`Q1_4_Differential_Diagnosis_Confounders.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.4_Differential_Diagnosis_Confounders/Q1_4_Differential_Diagnosis_Confounders.md)

#### 🔬 Candidate Evidence & Key Insights Available for the Team:
* **The Alarm Fatigue Crisis**: Over 72% of hospital telemetry alarms are clinically non-actionable; consumer wearables cry wolf on anxiety, causing users to silence or delete apps.
* **Multi-Modal Decoupling Rules**:
  * *Severe Panic Attack*: Heart rate and breathing spike, but lungs remain completely dry ($Z_0$ stable) and $SpO_2 \ge 99\%$. Mechanical contractility remains hyperdynamic. Device suppresses ischemic alarm.
  * *Vigorous Exercise*: Corroborated by dual-IMU motion ($>1.5\text{ g}$ cadence). Myocardial contractility increases rather than decays; no pulmonary backpressure.
  * *Vasovagal Syncope*: Sudden vagal bradycardia, but zero ischemic ST-deviation, dry lungs, and prompt recovery once supine.
* **Safety Net**: 30-second tactile/haptic patient cancellation interlock prevents inappropriate emergency dispatch for conscious patients.

#### ✍️ `[Team Decision & Customization Slot - Module 5]`:
*(Team members handling Firmware / Clinical UX: Finalize false-alarm suppression logic and cancellation workflow.)*
* **Selected Decoupling Rules for Presentation**: `[ Team to fill / customize ]`
* **Patient Interlock Protocol**: `[ Team to confirm / customize ]`

---

### MODULE 6: Head-to-Head Competitive Moat Matrix
* **Ideathon Evaluation Role**: Proves distinct technological and clinical defensibility against giants (Pillar 2: Novelty & Moat).
* **Research Phase**: **Synthesized across Phases 1 & 2**
* **Current Status**: **COMPLETED RESEARCH (Available on Disk)**

#### 📁 Direct File Reference Links:
* 💡 Master Fixed vs Flexible Architecture: [`Master_Fixed_vs_Flexible_Architecture.md`](file:///c:/College/Ideathon/Product_Design/Master_Fixed_vs_Flexible_Architecture.md)
* 💡 Form Factor Evaluation: [`Form_Factor_Evaluation_Pendant_vs_Patch.md`](file:///c:/College/Ideathon/Product_Design/Form_Factor_Evaluation_Pendant_vs_Patch.md)
* 🔵 Relevant Deep Research Dossiers: [`Phase 1.1`](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md) | [`Phase 1.2`](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.2_Non_Invasive_Physical_Outputs/Q1_2_Non_Invasive_Physical_Outputs.md) | [`Phase 2.1`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.1_Sensing_Modalities_Biomarker_Mapping/Q2_1_Sensing_Modalities_Biomarker_Mapping.md) | [`Phase 2.2`](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.2_Anatomical_Sweet_Spots/Q2_2_Anatomical_Sweet_Spots.md)

#### 🔬 Candidate Evidence & Key Insights Available for the Team:
* **Why Apple Watch Ultra 2 / Galaxy Watch Fail**:
  * Wrist vasoconstriction during cardiogenic shock drops peripheral pulse signals by $>95\%$.
  * Mechanical heart recoil (SCG) and lung fluid backpressure (Bio-Z) cannot physically travel down arm bones to the wrist.
  * ECG requires touching the bezel with the opposite hand for 30 seconds—impossible during sleep, syncope, or collapse.
* **Why Whoop 4.0 / Oura Ring 3 Fail**:
  * Purely lifestyle recovery trackers; zero diagnostic ECG biopotentials, zero mechanical sensors, zero real-time emergency dispatch.
* **Why Hospital Holters & iRhythm Zio Patch Fail**:
  * Retrospective diagnostic devices: data is analyzed 2 to 14 days later by a lab technician after the patch is mailed back. Completely useless for stopping a sudden arrest occurring today.
* **Why Zoll LifeVest (Wearable Defibrillator) Fails**:
  * Bulky 1.8 kg thoracic harness, severe patient non-compliance, only acts *after* full ventricular arrest occurs (reactive shock).

#### ✍️ `[Team Decision & Customization Slot - Module 6]`:
*(Team members handling Market & Strategy: Select which competitors to highlight on the poster table.)*
* **Candidate Competitor Comparison Table**: `[ Team to review and customize for A0 poster ]`
* **Core Moat One-Liner**: `[ Team to fill / customize ]`

---

### MODULE 7: Signal Processing, Noise & Motion Artifacts (Phase 3)
* **Ideathon Evaluation Role**: Explains how clean waveforms are extracted during real-world walking and motion (Pillar 3: Feasibility).
* **Research Phase**: **Phase 3 (Analog & Digital Signal Processing)**
* **Current Status**: **IN PROGRESS — Q3.1, Q3.2, Q3.3 & Q3.4 COMPLETED (Available on Disk)**

#### 📁 Direct File Reference Links:
* **Sources of Signal Degradation & Motion Artifacts (Q3.1)**:
  * 🟢 Plain-English Takeaway: [`Q3_1_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_1_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q3_1_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_1_Product_Translation.md)
  * 🔵 Deep Noise & Physics Vault: [`Q3_1_Signal_Degradation_Sources.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.1_Signal_Degradation_Sources/Q3_1_Signal_Degradation_Sources.md)
* **Mandatory Analog Front-End (AFE) Filtering (Q3.2)**:
  * 🟢 Plain-English Takeaway: [`Q3_2_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_2_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q3_2_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_2_Product_Translation.md)
  * 🔵 Deep AFE Filtering Vault: [`Q3_2_Mandatory_Analog_Filtering_AFE.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.2_Mandatory_Analog_Filtering_AFE/Q3_2_Mandatory_Analog_Filtering_AFE.md)
* **Digital Signal Processing Algorithms — NLMS vs RLS vs Wavelets (Q3.3)**:
  * 🟢 Plain-English Takeaway: [`Q3_3_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_3_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q3_3_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_3_Product_Translation.md)
  * 🔵 Deep Algorithmic Vault: [`Q3_3_Digital_Signal_Processing_Algorithms.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.3_Digital_Signal_Processing_Algorithms/Q3_3_Digital_Signal_Processing_Algorithms.md)
* **Morphological vs Positional Artifact Discrimination (Q3.4)**:
  * 🟢 Plain-English Takeaway: [`Q3_4_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_4_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q3_4_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_4_Product_Translation.md)
* **Real-Time Sub-Milliwatt Signal Quality Index (SQI) Architecture (Q3.5)**:
  * 🟢 Plain-English Takeaway: [`Q3_5_Takeaway.md`](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_5_Takeaway.md)
  * 🟡 Product Translation (How & Why): [`Q3_5_Product_Translation.md`](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_5_Product_Translation.md)
  * 🔵 Deep Real-Time SQI Vault: [`Q3_5_Real_Time_Signal_Quality_Index.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.5_Real_Time_Signal_Quality_Index/Q3_5_Real_Time_Signal_Quality_Index.md)
* **Phase 3 Status**: **100% COMPLETE (All 5 Questions Fully Researched & Validated)**

#### 🔬 Candidate Evidence & Key Insights Available for the Team:
* **Selected Route 1+3 Architecture**: Modern Digital DSP on MCU + Dual-Node Adaptive Motion Subtraction.
* **The Walking Noise Reality**: Heel-strikes generate $1.5\text{ to }3.0\text{ g}$ shockwaves at $1\text{--}2\text{ Hz}$, swamping the heart's tiny $0.01\text{--}0.05\text{ g}$ mechanical pumping vibration ($SNR = -20\text{ dB}$).
* **Dual-IMU Cancellation**: Wristband IMU captures pure arm swings and footstep cadence; on-device NLMS adaptive filter subtracts this reference from the sternal IMU, boosting SNR by $>26\text{ dB}$.
* **On-Chip Front-End Rejection**: On-chip hardware anti-aliasing in ST LSM6DSOX ($400\text{ Hz}$ LPF) and ambient light cancellation in MAX86141 ($>90\text{ dB}$) strip out high-frequency static and 100/120 Hz lamp flicker before code execution.
* **Postural Normalization**: Gravity vector tracking ($0.05\text{ Hz}$) prevents normal $48\%$ stroke volume drops upon standing from triggering false alarms.

#### ✍️ `[Team Decision & Customization Slot - Module 7]`:
* **Selected Filtering Architecture**: **OFFICIALLY LOCKED TO ROUTE 1+3** (Digital DSP + Dual-Node Motion Cancellation).
* **Assigned Team Member / Domain**: `[ Team to assign: DSP / Firmware Engineer ]`

---

### MODULE 8: Data Engineering, AI Models & TinyML (Phases 4, 5, 6)
* **Ideathon Evaluation Role**: Details the machine learning architecture, training data, and on-chip edge optimization (Pillar 3: Feasibility).
* **Research Phases**: **Phase 4 (Data Engineering), Phase 5 (ML Architecture), Phase 6 (Edge Computing / TinyML)**
* **Current Status**: ⏳ **QUEUED FOR RESEARCH (Questions Mapped in Questionnaire)**

#### 🎯 Upcoming Research Scope & Questions to Tackle:
* **Phase 4 (The Data)**: Open clinical databases (PhysioNet PTB-XL, European ST-T, MIMIC-III), pre-event window labeling protocols, and patient-wise data leakage prevention.
* **Phase 5 (The Brain)**: Multivariate time-series neural networks (1D-CNN, Temporal Convolutional Networks, Transformers), multimodal feature fusion, and severe class imbalance loss functions.
* **Phase 6 (The Edge Limits)**: INT8 quantization, SRAM/Flash budgeting on Cortex-M33, and the multi-tier Hierarchical Sentry pipeline.

#### ✍️ `[Team Decision & Customization Slot - Module 8]`:
* **Target Research File Locations**: `Phase_04_Data_Engineering/`, `Phase_05_Machine_Learning/`, `Phase_06_Edge_Computing/`
* **Assigned Team Member / Domain**: `[ Team to assign: Machine Learning / AI Lead ]`
* **Content Status**: `[ Blank - To be researched and filled ]`

---

### MODULE 9: IoT Networking, Cloud & Emergency Dispatch (Phase 7)
* **Ideathon Evaluation Role**: Details automated cellular failover and zero-touch emergency response (Pillars 3 & 4: Feasibility & Value).
* **Research Phase**: **Phase 7 (IoT Communications & Cloud Infrastructure)**
* **Current Status**: ⏳ **QUEUED FOR RESEARCH (Questions Mapped in Questionnaire)**

#### 🎯 Upcoming Research Scope & Questions to Tackle:
* Distributed edge-to-phone-to-cloud architecture, Bluetooth Low Energy (BLE 5.3) power states, automated 911 / emergency dispatcher geolocation APIs, and end-to-end HIPAA/GDPR encryption.

#### ✍️ `[Team Decision & Customization Slot - Module 9]`:
* **Target Research File Location**: `Research_Dossier/Phase_07_IoT_Communications_Networking/`
* **Assigned Team Member / Domain**: `[ Team to assign: Cloud & IoT Engineer ]`
* **Content Status**: `[ Blank - To be researched and filled ]`

---

### MODULE 10: Power Budget, Battery & Biocompatible Enclosure (Phases 8, 10, 11)
* **Ideathon Evaluation Role**: Demonstrates real-world wearable viability, patient comfort, and failure safety (Pillars 3 & 5).
* **Research Phases**: **Phase 8 (Power & Mechanical), Phase 10 (Human Factors), Phase 11 (Failure Modes & FMEA)**
* **Current Status**: ⏳ **QUEUED FOR RESEARCH (Questions Mapped in Questionnaire)**

#### 🎯 Upcoming Research Scope & Questions to Tackle:
* LiPo battery capacity vs thickness trade-offs, IP67 waterproofing, medical-grade silicone skin compatibility (ISO 10993), hardware watchdog timers, and reserve capacitor energy for emergency transmission.

#### ✍️ `[Team Decision & Customization Slot - Module 10]`:
* **Target Research File Locations**: `Phase_08_Power_Management/`, `Phase_10_Human_Factors/`, `Phase_11_Failure_Modes/`
* **Assigned Team Member / Domain**: `[ Team to assign: Mechanical & Quality Engineer ]`
* **Content Status**: `[ Blank - To be researched and filled ]`

---

### MODULE 11: Market Beachhead, Health Economics & Business Model (Phase 12)
* **Ideathon Evaluation Role**: Answers the critical judge question: *"Who pays for this, and why will hospitals adopt it?"* (Pillar 4: Market & Health Economics).
* **Research Phase**: **Phase 12 (Health Economics, Market Strategy & Ideathon Pitch)**
* **Current Status**: ⏳ **CANDIDATE FRAMEWORKS COMPILED / OPEN FOR TEAM DECISION**

#### 🔬 Candidate Market & Business Models Available for the Team:
* **The Beachhead Market**: Post-PCI (post-stent) discharge patients (1.8M patients/year in US). 30% of acute re-infarctions occur within the first 30 days post-discharge.
* **The Payer Mechanics (Reimbursement)**:
  * Reimbursed under active US Medicare **Remote Patient Monitoring (RPM) CPT Codes**:
    * **CPT 99453**: Initial device set-up and patient education ($19 one-time).
    * **CPT 99454**: Monthly transmission of daily biometric telemetry (~$56/month).
    * **CPT 99457**: First 20 minutes of clinical review time (~$51/month).
    * Prescribing cardiologists generate **$107 to $148 per patient/month** in recurring clinic revenue.
* **The Hospital ROI (The HRRP Penalty Avoidance)**:
  * Under Medicare's Hospital Readmissions Reduction Program (HRRP), hospitals face severe financial penalties if cardiac patients are readmitted within 30 days.
  * Preventing just 5 emergency readmissions per 100 patients saves an institution over **$250,000** in uncompensated ICU care.

#### ✍️ `[Team Decision & Customization Slot - Module 11]`:
*(Team members handling Business / Economics: Select target market sizing, pricing model, and pitch ROI figures.)*
* **Selected Beachhead Market**: `[ Team to confirm: Post-PCI Stent Discharge vs High-Risk CAD ]`
* **Pricing & Revenue Model**: `[ Team to select: B2B Hospital Lease vs RPM Billing vs Direct-to-Consumer ]`
* **Financial Metrics for Pitch**: `[ Team to fill / customize ]`

---

### MODULE 12: Regulatory Strategy & Clinical Roadmap (Phase 9)
* **Ideathon Evaluation Role**: Proves to judges that the team understands FDA/CDSCO medical device approval pathways (Pillar 4: Viability).
* **Research Phase**: **Phase 9 (Clinical Safety & Regulatory Viability)**
* **Current Status**: ⏳ **CANDIDATE FRAMEWORKS COMPILED / OPEN FOR TEAM DECISION**

#### 🔬 Candidate Regulatory Pathways Available for the Team:
* **United States (FDA)**: Class II Medical Device via **510(k) Premarket Notification** (Demonstrating substantial equivalence to predicates: iRhythm Zio Patch [K121319] and Bardy Diagnostics CAM [K172883]). Regulated as **Software as a Medical Device (SaMD)**.
* **India (CDSCO)**: Class C Medical Device under Medical Device Rules (MDR 2017).
* **Applicable Standards**: ISO 13485 (QMS), IEC 62304 (Software Lifecycle), IEC 60601-1 (Electrical Safety), IEC 60601-2-47 (Ambulatory ECG), ISO 10993 (Biocompatibility).

#### ✍️ `[Team Decision & Customization Slot - Module 12]`:
*(Team members handling Regulatory / Clinical: Select regulatory roadmap milestones for poster.)*
* **Regulatory Clearance Route**: `[ Team to confirm ]`
* **Clinical Trial Milestones**: `[ Team to fill / customize ]`

---

### MODULE 13: Presentation Pitch Deck, Poster Copy & Judge Defense
* **Ideathon Evaluation Role**: Winning the live competition presentation and Q&A cross-examination (Pillar 5: Presentation & Q&A).
* **Research Phase**: **Ideathon Pitch & Poster Deliverables**
* **Current Status**: ⏳ **OPEN FOR TEAM COLLABORATION**

#### 📁 Direct File Reference Links:
* 🎯 Master Systems Questionnaire: [`Master_Research_Questionnaire_Expanded.md`](file:///c:/College/Ideathon/Master_Research_Questionnaire_Expanded.md)
* 🎯 Hardware Component Scorecard: [`Sensor_Evaluation_Deep_Dive_Framework.md`](file:///c:/College/Ideathon/Sensor_Evaluation_Deep_Dive_Framework.md)
* 🎯 Modular Poster Canvas: `Ideathon_Poster_and_Pitch/A0_Poster_Modular_Canvas.md` *(Modular blocks covering all 12 phases)*
* 🎯 Master Pitch & Poster Guide: `Ideathon_Poster_and_Pitch/Master_Pitch_and_Poster_Guide.md` *(Domain ownership & knockout Q&A defense scripts)*

#### 🔬 Typical Tough Judge Questions to Prepare For:
1. *"Isn't sudden cardiac arrest unpredictable? Aren't you confusing an arrhythmia with a heart attack?"*
2. *"Smartwatches already have ECG and optical sensors. Why do we need another device on the chest?"*
3. *"Cardiologists hate false alarms. How do you prevent your device from crying wolf on panic attacks or workouts?"*
4. *"How can your battery survive multi-modal continuous sensing and AI without dying in 4 hours?"*
5. *"Who actually pays for this device, and how does a hospital make money adopting it?"*

#### ✍️ `[Team Decision & Customization Slot - Module 13]`:
*(Team members: Assign presentation speaking roles and rehearse knockout defense scripts.)*
* **Pitch Speaker Roles**:
  * *Clinical Hook & Impact*: `[ Team Member 1 Name ]`
  * *Hardware, Physics & Form Factor*: `[ Team Member 2 Name ]`
  * *Firmware, AI & False-Alarm Rejection*: `[ Team Member 3 Name ]`
  * *Market, Health Economics & Q&A Lead*: `[ Team Member 4 Name ]`
* **Selected 3-Minute Pitch Script Draft**: `[ Team to review and customize ]`

---

## 🗺️ SECTION 4: Master Cross-Reference Knowledge Map

Every completed question across our repository is hyperlinked below across its 3 layers (Tier 2 Takeaway, Tier 2.5 Product Translation, Tier 3 Deep Vault) alongside its recommended team domain:

| Phase | Question ID & Domain | Recommended Domain Lead | Plain Takeaway (Tier 2) | Product Translation (Tier 2.5) | Deep Research Vault (Tier 3) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Q1.1: 1-to-6-Hour Cascade** | Clinical / Physiology | [Q1.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_1_Takeaway.md) | [Q1.1 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_1_Product_Translation.md) | [Phase 1.1 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md) |
| **Phase 1** | **Q1.2: Physical Outputs** | Biomedical / Sensors | [Q1.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_2_Takeaway.md) | [Q1.2 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_2_Product_Translation.md) | [Phase 1.2 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.2_Non_Invasive_Physical_Outputs/Q1_2_Non_Invasive_Physical_Outputs.md) |
| **Phase 1** | **Q1.3: Demographics** | Clinical / AI | [Q1.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_3_Takeaway.md) | [Q1.3 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_3_Product_Translation.md) | [Phase 1.3 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.3_Demographic_Variations/Q1_3_Demographic_Variations.md) |
| **Phase 1** | **Q1.4: Confounder Decoupling** | Clinical / Firmware | [Q1.4 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_4_Takeaway.md) | [Q1.4 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_4_Product_Translation.md) | [Phase 1.4 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.4_Differential_Diagnosis_Confounders/Q1_4_Differential_Diagnosis_Confounders.md) |
| **Phase 1** | **Q1.5: Circadian & Sleep** | Physiology / Algorithms| [Q1.5 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_5_Takeaway.md) | [Q1.5 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q1_5_Product_Translation.md) | [Phase 1.5 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.5_Circadian_Sleep_Adaptations/Q1_5_Circadian_Sleep_Adaptations.md) |
| **Phase 2** | **Q2.1: Sensor Modalities** | Embedded Hardware | [Q2.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_1_Takeaway.md) | [Q2.1 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_1_Product_Translation.md) | [Phase 2.1 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.1_Sensing_Modalities_Biomarker_Mapping/Q2_1_Sensing_Modalities_Biomarker_Mapping.md) |
| **Phase 2** | **Q2.2: Anatomical Sweet Spots**| Biomedical / Mechanical| [Q2.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_2_Takeaway.md) | [Q2.2 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_2_Product_Translation.md) | [Phase 2.2 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.2_Anatomical_Sweet_Spots/Q2_2_Anatomical_Sweet_Spots.md) |
| **Phase 2** | **Q2.3: Digitization & FIFO** | Firmware / Embedded | [Q2.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_3_Takeaway.md) | [Q2.3 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_3_Product_Translation.md) | [Phase 2.3 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.3_Sampling_Frequencies_Bit_Resolutions/Q2_3_Quantitative_Digitization_Architecture.md) |
| **Phase 2** | **Q2.4: Optical Skin Tone** | Optical / Biomedical | [Q2.4 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_4_Takeaway.md) | [Q2.4 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_4_Product_Translation.md) | [Phase 2.4 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.4_Optical_Skin_Tone_Melanin_Inclusivity/Q2_4_Optical_Skin_Tone_Melanin_Inclusivity.md) |
| **Phase 2** | **Q2.5: Skin-Electrode Interface** | Materials / Hardware | [Q2.5 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_5_Takeaway.md) | [Q2.5 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_5_Product_Translation.md) | [Phase 2.5 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.5_Skin_Electrode_Interface_Impedance/Q2_5_Skin_Electrode_Interface_Impedance.md) |
| **Phase 3** | **Q3.1: Signal Degradation** | DSP / Firmware | [Q3.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_1_Takeaway.md) | [Q3.1 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_1_Product_Translation.md) | [Phase 3.1 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.1_Signal_Degradation_Sources/Q3_1_Signal_Degradation_Sources.md) |
| **Phase 3** | **Q3.2: Mandatory Analog Filtering** | Hardware / Circuits | [Q3.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_2_Takeaway.md) | [Q3.2 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_2_Product_Translation.md) | [Phase 3.2 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.2_Mandatory_Analog_Filtering_AFE/Q3_2_Mandatory_Analog_Filtering_AFE.md) |
| **Phase 3** | **Q3.3: DSP Algorithms (NLMS/RLS/DWT)**| DSP / Firmware | [Q3.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_3_Takeaway.md) | [Q3.3 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_3_Product_Translation.md) | [Phase 3.3 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.3_Digital_Signal_Processing_Algorithms/Q3_3_Digital_Signal_Processing_Algorithms.md) |
| **Phase 3** | **Q3.4: Postural Disambiguation** | Biomechanics / DSP | [Q3.4 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_4_Takeaway.md) | [Q3.4 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_4_Product_Translation.md) | [Phase 3.4 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.4_Morphological_vs_Positional_Artifact_Discrimination/Q3_4_Morphological_vs_Positional_Artifact_Discrimination.md) |
| **Phase 3** | **Q3.5: Real-Time Sub-mW SQI** | Embedded / Algorithms | [Q3.5 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_5_Takeaway.md) | [Q3.5 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q3_5_Product_Translation.md) | [Phase 3.5 Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_03_Analog_Digital_Signal_Processing/3.5_Real_Time_Signal_Quality_Index/Q3_5_Real_Time_Signal_Quality_Index.md) |
| **Phases 4–12**| **Upcoming Research Roadmap** | All Team Members | [Master Questionnaire](file:///c:/College/Ideathon/Master_Research_Questionnaire_Expanded.md) | [Sensor Evaluation Scorecard](file:///c:/College/Ideathon/Sensor_Evaluation_Deep_Dive_Framework.md) | [Research Dossier Directory](file:///c:/College/Ideathon/Research_Dossier/) |
