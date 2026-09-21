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
│       ├── Q1_2_Non_Invasive_Physical_Outputs.md            # Non-Invasive Diagnostic Physics (53 Sources)
│       ├── Q1_4_Differential_Diagnosis_Confounders.md       # Multi-Biomarker Decoupling (58 Sources)
│       ├── Q1_5_Circadian_Sleep_Adaptations.md               # Chronobiology & Sleep Gating (41 Sources)
│       └── assets/                                          # Clinical diagrams & charts
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

### 3. [Phase 1, Question 1.4: Differential Diagnosis & Confounders](Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/Q1_4_Differential_Diagnosis_Confounders.md)
* **False-Alarm Eradication**: Eliminates alert fatigue by decoupling lethal cardiac events from benign confounders:
  * **Severe Panic Attack**: Hyperventilation blows off $CO_2$ (respiratory alkalosis), but $SpO_2$ remains locked at $98\%–100\%$. In ischemia, pulmonary congestion degrades $SpO_2$ ($90\%–94\%$) despite rapid breathing.
  * **Exercise Tachycardia**: Heart rate scales with IMU movement wattage; QRS is narrow ($<0.12\text{s}$). In VTach, heart rate is 170+ bpm at near-zero motion with wide QRS ($>0.14\text{s}$).
  * **Vasovagal Syncope**: Driven by a paradoxical parasympathetic storm (HF surge, bradycardia/asystole), the exact inverse of pre-SCA adrenergic surge.
  * **Epileptic Seizure**: Ictal tachycardia precedes motor convulsions by $\sim 5\text{s}$, followed by rhythmic 3-axis shaking.
* **Transfer Entropy ($T_{\text{SpO2} \rightarrow \text{HR}}$)**: Mathematical detection of systemic decomplexification.
* **Verification**: 58 peer-reviewed citations mapped to exact sections, figures, and tables.

### 4. [Phase 1, Question 1.5: Chronobiological Architecture & Sleep Decoupling](Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/Q1_5_Circadian_Sleep_Adaptations.md)
* **Morning Vulnerability**: PAI-1 peaks at ~6:30 AM, suppressing natural clot-dissolving fibrinolysis at the same time morning cortisol and catecholamines surge.
* **Streaming Cosinor Model**: Replaces rigid static thresholds with dynamic 24-hour sinusoidal baselines ($f(t) = M + A \cos(2\pi t / \tau + \phi)$) computed on-chip with $\mathcal{O}(N)$ linear complexity.
* **Sleep Gating**: Multitask learning classifies NREM vs. REM sleep; software gating widens rate thresholds during REM autonomic storms and shifts diagnostic weight to 1D-CNN ECG QRS morphology.
* **OSA Discrimination**: Cardiorespiratory Phase-Coupling (CPC) and Electrocardiogram-Derived Respiration (EDR) separate cyclical $0.01–0.04\text{ Hz}$ sleep apnea loops from monotonic ischemic collapse.
* **Verification**: 41 peer-reviewed citations mapped to exact sections, figures, and tables.

---

## 🛠️ Master Frameworks

* **[Master Research Questionnaire (12 Phases)](Master_Research_Questionnaire_Expanded.md)**: The end-to-end systems architecture roadmap covering biology, physics, noise DSP, machine learning, TinyML, wireless IoT, power budgets, regulatory (CDSCO/FDA), and pitch economics.
* **[Sensor Evaluation Deep Dive Framework](Sensor_Evaluation_Deep_Dive_Framework.md)**: Hardware scorecard evaluating communication protocols, clock synchronization (PAT), power budgets, and physical packaging for COTS components (ADS1292R, MAX86141, LSM6DSOX, TMP117).

---

## 👥 Authors & Project Context
* **Project**: Autonomous Sternal IoT Patch for Early Prediction of Sudden Cardiac Arrest (SCA) & Acute Ischemia
* **Lead Researcher**: Headhunte-121
* **Event**: College Ideathon Competition