# Autonomous Medical IoT Sternal Patch: Early Prediction of Sudden Cardiac Arrest (SCA) & Acute Ischemia

> **Ideathon Research & Systems Architecture Knowledge Base**  
> An exhaustive, judge-ready, peer-reviewed engineering dossier designing an autonomous wearable system for the **1-to-6-hour pre-infarction ischemic window**.

---

## 📌 Project Overview
Sudden Cardiac Arrest (SCA) and Acute Myocardial Infarction (AMI) are rarely instantaneous events. In the 1 to 6 hours preceding total coronary occlusion, the human body undergoes a deterministic series of metabolic, autonomic, and hemodynamic shifts known as the **Ischemic Cascade**.

This repository contains the complete systems engineering blueprint, clinical pathophysiological research, multi-biomarker decoupling rules, and hardware evaluation framework for an autonomous medical IoT device.

---

## 📂 Repository Structure

```
.
├── Master_Research_Questionnaire_Expanded.md  # 12-Phase Master Systems Architecture Framework
├── Sensor_Evaluation_Deep_Dive_Framework.md   # Component-level Hardware Scorecard & COTS Comparison
├── Research_Dossier/                          # Peer-Reviewed Modular Research Knowledge Base
│   ├── README.md                              # Master Tracking Registry for all 12 Phases
│   └── Phase_01_Pathophysiology_and_Biomarkers/
│       ├── Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md      # 1-to-6-Hour Cascade (86 Sources)
│       │   └── Q1_1_Key_Takeaways.md                        # Plain-English Takeaways
│       ├── Q1_2_Non_Invasive_Physical_Outputs.md            # Non-Invasive Diagnostic Physics (53 Sources)
│       ├── Q1_3_Demographic_Variations.md                   # Demographics & Comorbidities (72 Sources)
│       ├── Q1_4_Differential_Diagnosis_Confounders.md       # Multi-Biomarker Decoupling (58 Sources)
│       ├── Q1_5_Circadian_Sleep_Adaptations.md               # Chronobiology & Sleep Gating (41 Sources)
│       ├── Phase_01_Executive_Summary_Plain_English.md      # Plain-English Synthesis (310 Sources)
│       └── assets/                                          # Clinical diagrams & charts
│   └── Phase_02_Signal_Acquisition_Physics/
│       ├── Q2_1_Sensing_Modalities_Biomarker_Mapping.md     # Transduction Physics (50 Sources)
│       └── assets/                                          # Hardware schematics
└── README.md                                  # This project overview
```

---

## 🔬 Key Research Modules Completed

### 1. [Phase 1, Question 1.1: The 1-to-6-Hour Pre-Infarction Cascade](Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md)
* **Biological Proof**: Disproves the myth that heart attacks happen without warning.
* **Timeline**: Maps the sequential progression: Plaque destabilization $\rightarrow$ Autonomic storm ($T-3\text{h}$, SDNN $< 50\text{ ms}$) $\rightarrow$ Metabolic acidosis & lusitropic stiffening ($T-2\text{h}$) $\rightarrow$ Compensatory Tachypnea ($RR > 20\text{ bpm}$) $\rightarrow$ Subendocardial ECG shifts ($T-1\text{h}$).
* **Biomarkers**: Proves traditional Troponin is a late necrosis marker, while early pre-necrotic markers (IMA, GPBB, H-FABP) elevate within 10 to 60 minutes.
* **Verification**: 86 peer-reviewed citations mapped to exact sections, figures, and tables.

### 2. [Phase 1, Question 1.2: Non-Invasive Diagnostic Physics](Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/Q1_2_Non_Invasive_Physical_Outputs.md)
* **Surface Transduction**: Maps visceral ischemia into 5 external physical domains:
  * **Electrodynamics**: Injury currents causing ST-depression and T-wave inversion; SDNN $< 50\text{ ms}$ autonomic collapse; EDR uncoupling.
  * **Kinematics & Micro-Vibrations (SCG / GCG)**: Diastolic stiffness attenuates Seismocardiographic Aortic Opening (AO) amplitude by $>50\%$ (higher sensitivity than exercise ECG: 61.1% vs 44.2%) and amplifies Rapid Filling (RF) waves by $>20\%$.
  * **Opto-Vascular (PPG)**: UK Biobank (114,884 subjects) validates systolic area flattening; Respiratory Modulation Response ($\text{RMR} < 30\%$) predicts significant CAD with 93% Positive Predictive Value.
  * **Transdermal Infrared Spectrophotometry (ISS)**: Bloodless wrist optical hs-cTnI detection (AUC 0.90–0.92 in 5 min; OR 4.69 for stenosis); sweat STAMBP proteomics.
  * **Sudomotor & Thermal**: Cholinergic diaphoresis triggers Galvanic Skin Response (GSR) phasic SCR spikes (1–3s rise time); asymmetrical facial cooling and left jaw thermal drop (+13% diagnostic accuracy).
* **Verification**: 53 peer-reviewed citations mapped to exact sections, figures, and tables.

### 3. [Phase 1, Question 1.3: Demographic & Comorbidity Variations](Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/Q1_3_Demographic_Variations.md)
* **Senescent Cardiovascular System**: Arterial stiffening ($PWV > 10\text{ m/s}$) accelerates wave reflections and shortens reflection time, blunting the PPG dicrotic notch. Linear HRV metrics collapse ($SDNN < 40\text{ ms}$), but non-linear fractal scaling (DFA $\alpha_1 \approx 1.0$) is preserved in healthy aging; acute ischemia breaks this scaling ($\alpha_1 \rightarrow 0.5$). Renal clearance decay shifts resting H-FABP baselines upwards, requiring dynamic derivative thresholding ($\frac{d[\text{Biomarker}]}{dt}$).
* **Diabetic Silent Myocardial Ischemia (SMI)**: Cardiac Autonomic Neuropathy (CAN) destroys unmyelinated C-fibers, abolishing angina pectoris (4x MACE risk) and postganglionic sudomotor sweat surges (flat GSR). Decoupling is intercepted via QTc dispersion ($>460\text{ ms}$), microvolt T-Wave Alternans (TWA), and blunted Heart Rate Recovery ($HRR < 12\text{ bpm}$).
* **Structural Arrhythmias & Remodeling**: Atrial Fibrillation (AFib) causes beat-to-beat mechanical chaos, obliterating single-beat Seismocardiography (SCG) fiducials; resolved via R-R cycle length binning and 40-beat ensemble averaging. Hypertension/LVH strains produce baseline ST-T deviations and S4 acoustic gallops ($20–40\text{ Hz}$). Heart failure elevates filling pressures, producing S3 gallops ($15–30\text{ Hz}$). Dual-sensor PTT ($\text{PTT}_{\text{true}} = t_{\text{PPG}} - t_{\text{SCG\_AO}}$) eliminates the Pre-Ejection Period (PEP) confounder.
* **Fairness & Edge Personalization**: Mitigates AI bias against females and minorities using SMOTE oversampling, Adversarial Gradient Reversal debiasing, Demographic Parity, and Equalized Odds. On-device TinyML builds individualized 72-hour rolling $Z$-score baselines ($Z = \frac{x - \mu}{\sigma}$), eliminating generalized population bias on-chip.
* **Verification**: 72 peer-reviewed citations mapped to exact sections, figures, and tables.

### 4. [Phase 1, Question 1.4: Differential Diagnosis & Confounders](Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/Q1_4_Differential_Diagnosis_Confounders.md)
* **False-Alarm Eradication**: Eliminates alert fatigue by decoupling lethal cardiac events from benign confounders:
  * **Severe Panic Attack**: Hyperventilation blows off $CO_2$ (respiratory alkalosis), but $SpO_2$ remains locked at $98\%–100\%$. In ischemia, pulmonary congestion degrades $SpO_2$ ($90\%–94\%$) despite rapid breathing.
  * **Exercise Tachycardia**: Heart rate scales with IMU movement wattage; QRS is narrow ($<0.12\text{s}$). In VTach, heart rate is 170+ bpm at near-zero motion with wide QRS ($>0.14\text{s}$).
  * **Vasovagal Syncope**: Driven by a paradoxical parasympathetic storm (HF surge, bradycardia/asystole), the exact inverse of pre-SCA adrenergic surge.
  * **Epileptic Seizure**: Ictal tachycardia precedes motor convulsions by $\sim 5\text{s}$, followed by rhythmic 3-axis shaking.
* **Transfer Entropy ($T_{\text{SpO2} \rightarrow \text{HR}}$)**: Mathematical detection of systemic decomplexification.
* **Verification**: 58 peer-reviewed citations mapped to exact sections, figures, and tables.

### 5. [Phase 1, Question 1.5: Chronobiological Architecture & Sleep Decoupling](Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/Q1_5_Circadian_Sleep_Adaptations.md)
* **Morning Vulnerability**: PAI-1 peaks at ~6:30 AM, suppressing natural clot-dissolving fibrinolysis at the same time morning cortisol and catecholamines surge.
* **Streaming Cosinor Model**: Replaces rigid static thresholds with dynamic 24-hour sinusoidal baselines ($f(t) = M + A \cos(2\pi t / \tau + \phi)$) computed on-chip with $\mathcal{O}(N)$ linear complexity.
* **Sleep Gating**: Multitask learning classifies NREM vs. REM sleep; software gating widens rate thresholds during REM autonomic storms and shifts diagnostic weight to 1D-CNN ECG QRS morphology.
* **OSA Discrimination**: Cardiorespiratory Phase-Coupling (CPC) and Electrocardiogram-Derived Respiration (EDR) separate cyclical $0.01–0.04\text{ Hz}$ sleep apnea loops from monotonic ischemic collapse.
* **Verification**: 41 peer-reviewed citations mapped to exact sections, figures, and tables.

### 6. [Phase 2, Question 2.1: Physical Sensing Modalities & Biomarker Mapping](Research_Dossier/Phase_02_Signal_Acquisition_Physics/Q2_1_Sensing_Modalities_Biomarker_Mapping.md)
* **Zero-Blindspot Transduction**: Maps the 5 core physical sensing modalities directly to Phase 1's visceral biomarkers:
  * **Electrical (Biopotential & EDA)**: TI ADS1292R ($500\text{ Hz}, 24\text{-bit}$) captures microvolt ST injury currents and T-wave alternans (TWA, $5–20\ \mu\text{V}$); dry sternal electrodes measure sudomotor cold sweats ($1–3\text{s}$ rise time).
  * **Mechanical (SCG & GCG)**: ST LSM6DSOX 6-axis IMU ($200\text{ Hz}$) detects lusitropic pump failure (Aortic Opening [AO] amplitude drop $>50\%$) and provides the kinematic motion denominator.
  * **Optical (Multi-Wavelength PPG)**: ADI MAX86141 Red/IR/Green ($100\text{ Hz}$) detects microvascular stiffening ($\text{RMR} < 30\%$) and hypoxic desaturations ($SpO_2$).
  * **Acoustic (Phonocardiography)**: PVDF piezoelectric film transducers capture sub-audible S3 ($15–30\text{ Hz}$) and S4 ($20–40\text{ Hz}$) gallops, marking elevated left ventricular filling pressure ($\text{LVEDP} > 20\text{ mmHg}$).
  * **Bio-Impedance (Thoracic Bio-Z)**: High-frequency tetrapolar current injection ($50–100\text{ kHz}$) detects base impedance ($Z_0$) decay from pulmonary capillary fluid accumulation and tracks breath-by-breath tachypnea ($\Delta Z_{\text{resp}}$).
* **PEP-Free True PTT**: Fuses mechanical SCG AO with optical PPG foot arrival ($\text{PTT}_{\text{true}} = t_{\text{PPG}} - t_{\text{SCG\_AO}}$), completely eliminating Pre-Ejection Period (PEP) error.
* **Verification**: 50 peer-reviewed citations mapped to exact sections, figures, and tables.

---

## 🛠️ Master Frameworks

* **[Master Research Questionnaire (12 Phases)](Master_Research_Questionnaire_Expanded.md)**: The end-to-end systems architecture roadmap covering biology, physics, noise DSP, machine learning, TinyML, wireless IoT, power budgets, regulatory (CDSCO/FDA), and pitch economics.
* **[Sensor Evaluation Deep Dive Framework](Sensor_Evaluation_Deep_Dive_Framework.md)**: Hardware scorecard evaluating communication protocols, clock synchronization (PAT), power budgets, and physical packaging for COTS components (ADS1292R, MAX86141, LSM6DSOX, TMP117).

---

## 👥 Authors & Project Context
* **Project**: Autonomous Sternal IoT Patch for Early Prediction of Sudden Cardiac Arrest (SCA) & Acute Ischemia
* **Lead Researcher**: Headhunte-121
* **Event**: College Ideathon Competition