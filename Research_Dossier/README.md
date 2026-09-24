# Medical IoT Ideathon Research Dossier
## Master Knowledge Base & Clinical Systems Architecture Registry

---

> **Project**: Autonomous Sternal IoT Patch for Early Prediction of Sudden Cardiac Arrest (SCA) & Acute Ischemia  
> **Master Framework**: [Master_Research_Questionnaire_Expanded.md](../Master_Research_Questionnaire_Expanded.md)  
> **Hardware Scorecard**: [Sensor_Evaluation_Deep_Dive_Framework.md](../Sensor_Evaluation_Deep_Dive_Framework.md)  
> **Architecture Blueprint**: [Cardiac_Arrest_Detection_Master_Architecture.md](../Cardiac_Arrest_Detection_Master_Architecture.md)

---

### Research Progress & Question Registry

Every question from your expanded master questionnaire is systematically documented in this directory tree. Each document contains:
1. Full peer-reviewed clinical / systems synthesis.
2. Verified figures, diagrams, and data tables.
3. Explicit **Section-to-Source Verification Index** mapping every statement to exact academic sources.
4. Annotated Bibliography with direct source hyperlinks.

| Phase | Domain | Question ID & Topic | Status | File Link |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Pathophysiology & Biomarkers** | **Q1.1**: 1-to-6-Hour Pre-Infarction Cascade | **COMPLETED** (86 Sources) | [Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md](./Phase_01_Pathophysiology_and_Biomarkers/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md) |
| Phase 1 | Pathophysiology & Biomarkers | **Q1.2**: Non-Invasive Physical Outputs | **COMPLETED** (53 Sources) | [Q1_2_Non_Invasive_Physical_Outputs.md](./Phase_01_Pathophysiology_and_Biomarkers/Q1_2_Non_Invasive_Physical_Outputs.md) |
| Phase 1 | Pathophysiology & Biomarkers | **Q1.3**: Demographic Variations (Age/Sex/Diabetes) | **COMPLETED** (72 Sources) | [Q1_3_Demographic_Variations.md](./Phase_01_Pathophysiology_and_Biomarkers/Q1_3_Demographic_Variations.md) |
| Phase 1 | Pathophysiology & Biomarkers | **Q1.4**: Differential Diagnosis & Confounders | **COMPLETED** (58 Sources) | [Q1_4_Differential_Diagnosis_Confounders.md](./Phase_01_Pathophysiology_and_Biomarkers/Q1_4_Differential_Diagnosis_Confounders.md) |
| Phase 1 | Pathophysiology & Biomarkers | **Q1.5**: Circadian & Sleep Stage Adaptations | **COMPLETED** (41 Sources) | [Q1_5_Circadian_Sleep_Adaptations.md](./Phase_01_Pathophysiology_and_Biomarkers/Q1_5_Circadian_Sleep_Adaptations.md) |
| **Phase 1** | **Pathophysiology & Biomarkers** | **Phase 1 Executive Summary (Plain English)** | **COMPLETE SYNTHESIS** (310 Sources) | [Phase_01_Executive_Summary_Plain_English.md](./Phase_01_Pathophysiology_and_Biomarkers/Phase_01_Executive_Summary_Plain_English.md) |
| **Phase 2** | **Signal Acquisition (Physics)** | **Q2.1 - Q2.5**: Sensing Modalities, Sweet Spots, Sampling Rates | *Ready for Input* | `./Phase_02_Signal_Acquisition_Physics/` |
| **Phase 3** | **Signal Processing (Noise)** | **Q3.1 - Q3.5**: Analog AFE, Wavelet DSP, NLMS Adaptive Filters | *Ready for Input* | `./Phase_03_Analog_Digital_Signal_Processing/` |
| **Phase 4** | **Data Engineering** | **Q4.1 - Q4.6**: Clinical Databases, Pre-Event Labeling, Leakage Prevention | *Ready for Input* | `./Phase_04_Data_Engineering_Preprocessing/` |
| **Phase 5** | **Machine Learning Architecture** | **Q5.1 - Q5.6**: Multivariate Forecasting, Multimodal Fusion, Explainable AI | *Ready for Input* | `./Phase_05_Machine_Learning_Architecture/` |
| **Phase 6** | **Edge Computing & TinyML** | **Q6.1 - Q6.5**: INT8 Quantization, SRAM Bottlenecks, Sentry Pipeline | *Ready for Input* | `./Phase_06_Edge_Computing_TinyML/` |
| **Phase 7** | **IoT Communications** | **Q7.1 - Q7.5**: Distributed Architecture, BLE 5.3, Zero-Touch Escalation | *Ready for Input* | `./Phase_07_IoT_Communications_Networking/` |
| **Phase 8** | **Power & Mechanical Design** | **Q8.1 - Q8.5**: Duty Cycling, LiPo Budget, Waterproofing, Thermal Limits | *Ready for Input* | `./Phase_08_Power_Management_Mechanical_Design/` |
| **Phase 9** | **Clinical Safety & Regulatory** | **Q9.1 - Q9.5**: Alarm Fatigue, CDSCO / FDA SaMD, Cryptography | *Ready for Input* | `./Phase_09_Clinical_Safety_Regulatory_Viability/` |
| **Phase 10**| **Human Factors (UX)** | **Q10.1 - Q10.3**: Patient Adherence, Cardiophobia, Cancel-Alarm UX | *Ready for Input* | `./Phase_10_Human_Factors_Ergonomics/` |
| **Phase 11**| **Failure Modes & Safe-States**| **Q11.1 - Q11.3**: FMEA, Hardware Watchdogs, Reserve Capacitor Energy | *Ready for Input* | `./Phase_11_Failure_Modes_Failsafes/` |
| **Phase 12**| **Health Economics & Pitch** | **Q12.1 - Q12.3**: Cost/QALY, Post-PCI Beachhead TAM, Razor-Blade Model | *Ready for Input* | `./Phase_12_Health_Economics_Market_Pitch/` |

---

### File Organization Protocol for Upcoming Questions

To keep your research repository clean, standardized, and immediately presentable to judges:

1. **Folder per Phase**: Each phase has a dedicated directory (e.g., `Phase_01_Pathophysiology_and_Biomarkers`).
2. **Assets Subfolder**: Store all charts, graphs, and schematic diagrams inside an `assets/` subfolder within each phase.
3. **Question Filename Convention**: Name files by phase and question number: `Q<Phase>_<Question>_<Short_Topic_Name>.md`.
4. **Mandatory Sections in Every File**:
   - High-Level Summary Timeline / Diagram.
   - Core Scientific / Engineering Text.
   - Cross-Reference Verification Matrix (Section $\leftrightarrow$ Source $\leftrightarrow$ Core Claim).
   - Complete Annotated Bibliography with direct URLs.
