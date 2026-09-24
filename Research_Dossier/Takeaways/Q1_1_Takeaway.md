# Question 1.1 Key Information: The 1-to-6-Hour Pre-Infarction Window
## Pathophysiological Timeline, Sensor Architecture, and Clinical Classification

---

> **Document Type**: Technical & Clinical Information Summary  
> **Source Research Dossier**: [`1.1_Pre_Infarction_Cascade/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md`](../Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md) *(86 Sources)*  
> **Clinical Context Dossier**: [`1.1_Pre_Infarction_Cascade/Clinical_Realities_Hospital_Barriers_and_MI_Types.md`](../Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Clinical_Realities_Hospital_Barriers_and_MI_Types.md)

---

## 1. Overview and Core Finding

Sudden Cardiac Arrest (SCA) and Acute Myocardial Infarction (AMI) are widely perceived as instantaneous medical events with zero advance warning. Clinical cardiology research demonstrates that this perception is medically inaccurate:

* **Etiological Reality**: 70% to 80% of sudden non-traumatic cardiac arrests in adults are directly triggered by underlying coronary artery disease and acute myocardial ischemia.
* **The Pre-Infarction Window**: Complete cellular death (necrosis) and fatal electrical arrhythmias do not happen simultaneously when blood flow is compromised. Instead, the human heart undergoes a documented, progressive biological countdown lasting between **1 and 6 hours** before irreversible cell destruction or electrical collapse occurs.
* **Significance for Sternal Sensing**: This multi-hour window provides a viable timeframe to detect physical, electrical, and hemodynamic changes non-invasively before cardiac tissue sustains permanent damage.

---

## 2. The 1-to-6-Hour Biological Progression

The heart is a continuous muscular pump supplied by coronary arteries running across its surface. When blood supply through a coronary artery becomes significantly compromised, heart muscle tissue undergoes a distinct five-phase physiological progression:

```
+--------------------------------------------------------------------------------------------------+
|                            THE 1-TO-6-HOUR PRE-INFARCTION PROGRESSION                            |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   PHASE 1 (T - 6 to 3 Hours): Coronary Narrowing & Cellular Oxygen Starvation                     |
|   - Atherosclerotic plaque disrupts, triggering localized platelet aggregation and thrombus.     |
|   - Blood flow to downstream myocardium decreases.                                               |
|   - Oxygen-deprived heart cells shift from aerobic metabolism to anaerobic glycolysis.           |
|   - Lactic acid accumulates in cardiac myocytes, lowering intracellular pH.                      |
|                                                                                                  |
|   PHASE 2 (T - 3 Hours): Autonomic Response & Sympathetic Surge                                  |
|   - Chemoreceptors and mechanoreceptors in ischemic tissue trigger the sympathetic nervous       |
|     system to release adrenaline and noradrenaline.                                              |
|   - Natural beat-to-beat variability (Heart Rate Variability / HRV) collapses under intense      |
|     sympathetic tone.                                                                            |
|                                                                                                  |
|   PHASE 3 (T - 2 Hours): Diastolic Relaxation Failure (Myocardial Stiffening)                    |
|   - Depletion of cellular ATP prevents calcium re-uptake, impairing active myocardial relaxation.|
|   - The ventricular wall becomes stiff during filling (diastolic dysfunction).                   |
|   - Mechanical contraction force drops by 30% to 50%, weakening chest-wall vibrations.           |
|   - Left ventricular end-diastolic pressure rises, creating backward pressure into the lungs.   |
|                                                                                                  |
|   PHASE 4 (T - 1 Hour): Pulmonary Congestion & Compensatory Tachypnea                            |
|   - Elevated left ventricular pressures cause fluid transudation into pulmonary microvasculature.|
|   - Respiratory rate increases (>20 breaths/min) to expel CO2 and compensate for lactic acidosis.|
|   - Microvascular pulmonary fluid reduces gas exchange efficiency, lowering blood oxygen (90-94%).|
|                                                                                                  |
|   PHASE 5 (Hour 0): Terminal Electrical Destabilization (Arrest / Necrosis)                      |
|   - Ion pump failure causes extracellular potassium accumulation, creating electrical reentry.   |
|   - Ventricular Tachycardia (VT) degenerates into chaotic Ventricular Fibrillation (VF).         |
|   - Coordinated cardiac output halts, resulting in hemodynamic collapse and loss of consciousness.|
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

---

## 3. Sensor and Hardware Mapping

The biological progression identifies the specific physical signals that must be captured and the corresponding sensor hardware required on a sternal patch:

| Physiological Event | Biological Mechanism | Physical Signal | Selected Hardware Component |
| :--- | :--- | :--- | :--- |
| **Sympathetic Adrenaline Surge** | Autonomic reflex abolishes parasympathetic vagal tone | Collapse of beat-to-beat RR interval variation (HRV) | **ADS1292R**: 24-bit Low-Power Biopotential Analog Front-End (ECG) |
| **Diastolic Stiffening** | Calcium clearance failure halts ventricular relaxation | Reduced mechanical vibration amplitude of S1/S2 heart sounds | **LSM6DSOX**: Ultra-low-power 3-axis accelerometer (Seismocardiography / SCG) |
| **Pulmonary Backpressure** | Left ventricular filling pressure rises; microvascular lung congestion | Respiratory rate elevation (>20 bpm) and SpO2 drop (90%–94%) | **MAX86141**: Dual-channel optical pulse oximeter / PPG sensor |
| **Electrodermal Stress** | Sympathetic discharge triggers sudomotor sweat gland activation | Sternal micro-conductance shifts prior to conscious sweating | **ADS1292R**: Impedance measurement channel (EDA / Bio-Z) |

---

## 4. Algorithmic Sequential Verification Logic

Single-parameter threshold alerts (e.g., triggering an alarm based solely on elevated heart rate or a single irregular beat) produce high false-alarm rates during routine daily exertion, posture changes, or emotional stress.

To ensure clinical specificity, the algorithmic architecture follows the chronological order of the biological cascade:

```
               [ Step 1: Autonomic Anomaly ]
          Collapse in Heart Rate Variability (HRV)
             Combined with Sympathetic Tone Surge
                             |
                             v
             [ Step 2: Mechanical Confirmation ]
         Drop in Sternal Acceleration Amplitude (SCG)
           Indicating Reduced Ventricular Compliance
           (Verified during low accelerometer motion)
                             |
                             v
            [ Step 3: Hemodynamic Compromise ]
           Compensatory Tachypnea (>20 breaths/min)
              Combined with Peripheral SpO2 Decline
                             |
                             v
           [ Tier-3 Pre-Infarction Warning Alert ]
        Dispatched 1 to 4 Hours Prior to Terminal VF
```

By requiring multi-sensor verification across separate physiological domains (electrical, mechanical, and optical) occurring in chronological alignment, the system filters out benign anomalies while maintaining high sensitivity to true ischemic events.

---

## 5. Clinical and Industry Context

### 5.1 Hospital Emergency Diagnostic Barriers
Hospitals rely primarily on blood tests for **Cardiac Troponin** (cTnI / cTnT) and 12-lead ECGs. This creates several structural limitations for early warning:
1. **Pre-Hospital Transit Delay**: Median time from symptom onset to hospital arrival ranges between 2 to 4 hours due to patient denial, transportation, and triage.
2. **Troponin Release Kinetics**: Troponin is an intracellular structural protein. It enters the bloodstream only *after* myocardial cell membranes rupture (cellular necrosis). Peak concentration occurs 12 to 24 hours post-infarction. Troponin confirms tissue death after it has occurred; it cannot serve as a pre-infarction predictor.
3. **Early False-Negative Troponin**: During the initial 1 to 3 hours of ischemia, high-sensitivity troponin levels are often below diagnostic thresholds, requiring serial blood draws spaced 1 to 3 hours apart.
4. **Alarm Fatigue**: Bedside monitors generate between 150 and 350 alarms per bed per day, over 85% to 99% of which are clinically non-actionable, leading to desensitization among clinical staff.

### 5.2 Wrist-Worn Consumer Device Limitations
Consumer smartwatches and fitness trackers are constrained by anatomy and sensing geometry:
1. **Anatomical Distance**: Wrist placement is approximately 70–80 cm away from the central heart valves, preventing direct measurement of cardiac mechanical vibrations (SCG) or heart sound acoustics (PCG).
2. **Motion Susceptibility**: Distal extremity motion (typing, gesturing, walking) introduces severe motion artifacts into photoplethysmography (PPG) signals.
3. **Peripheral Vasoconstriction**: In states of acute myocardial hypoperfusion or intense sympathetic activation, peripheral blood vessels constrict to shunt blood to vital organs, causing peripheral wrist PPG amplitude to degrade or drop out completely. Sternal monitoring maintains central perfusion access.

---

## 6. The 5 Types of Myocardial Infarction

According to the *Fourth Universal Definition of Myocardial Infarction* (ESC/ACC/AHA/WHF Expert Consensus), heart attacks are classified into five distinct clinical categories, in addition to non-obstructive presentations:

```
+--------------------------------------------------------------------------------------------------+
|                       THE 5 TYPES OF MYOCARDIAL INFARCTION (UNIVERSAL DEFINITION)                |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   TYPE 1: Spontaneous Plaque Rupture / Thrombosis (70% - 80% of clinical cases)                  |
|   - Coronary atherothrombosis caused by plaque rupture, ulceration, or erosion.                  |
|   - Forms an occlusive or sub-occlusive clot, leading directly to transmural or subendocardial   |
|     ischemia (STEMI / NSTEMI).                                                                   |
|                                                                                                  |
|   TYPE 2: Supply-Demand Mismatch Ischemia (Without Acute Atherothrombosis)                       |
|   - Myocardial necrosis caused by severe oxygen mismatch rather than a ruptured clot.            |
|   - Triggers include sustained tachyarrhythmias, severe shock/hypotension, severe anemia, or     |
|     extreme hypertensive crisis.                                                                 |
|                                                                                                  |
|   TYPE 3: Sudden Cardiac Death Preceding Biomarker Availability                                  |
|   - Cardiac death with symptoms suggestive of myocardial ischemia and presumed new ECG changes,  |
|     occurring before blood samples can be obtained or before cardiac biomarkers appear in blood. |
|                                                                                                  |
|   TYPE 4: Percutaneous Coronary Intervention (PCI) Related                                       |
|   - Type 4a: Myocardial injury associated with coronary catheterization/angioplasty.            |
|   - Type 4b: Documented stent thrombosis occurring after stent implantation.                     |
|                                                                                                  |
|   TYPE 5: Coronary Artery Bypass Graft (CABG) Related                                            |
|   - Myocardial injury occurring during or within 48 hours of open-heart coronary bypass surgery. |
|                                                                                                  |
|   MINOCA: Myocardial Infarction with Non-Obstructive Coronary Arteries                           |
|   - Clinical presentation of acute MI with angiographically normal or near-normal epicardial     |
|     arteries (<50% stenosis). High prevalence in females; driven by microvascular dysfunction,   |
|     epicardial coronary vasospasm, or spontaneous coronary artery dissection (SCAD).             |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

### Detection Relevance Across MI Types:
* **Type 1 (Atherothrombotic)**: Detectable via the progressive multi-sensor cascade as the thrombus evolves over 1 to 4 hours.
* **Type 2 (Supply-Demand Mismatch)**: Identified when elevated cardiac mechanical work and tachycardia occur concurrently with zero physical exertion (detected via static accelerometer motion state).
* **Type 3 (Sudden Death Preceding Labs)**: Represents the specific target population for ambulatory continuous monitoring, capturing pre-arrest destabilization outside hospital settings.
* **Type 4b (Stent Thrombosis)**: Applicable to 30-day post-discharge remote monitoring for high-risk patients following percutaneous coronary intervention.
* **MINOCA**: Overcomes the diagnostic limitation of standard 12-lead ECGs in microvascular disease by measuring direct mechanical relaxation deficits (SCG) and microvascular optical pulsatility.

---

## 7. Summary of Engineering Specifications Derived from Q1.1

1. **Target Alert Lead Time**: 60 to 240 minutes prior to gross myocardial necrosis or ventricular arrhythmia.
2. **Sensor Complement**: Dual-lead biopotential analog front-end (ECG/HRV), 3-axis sternal accelerometer (SCG), and dual-wavelength optical sensor (PPG/SpO2/RR).
3. **Signal Processing Constraint**: Algorithms must prioritize autonomic and mechanical relaxation parameters over static rate thresholds to mitigate false-positive alerts.
4. **Anatomical Placement**: Sternal bone fixation provides direct acoustic and mechanical coupling to cardiac structures, avoiding peripheral vasoconstriction artifacts common to distal wearable form factors.
