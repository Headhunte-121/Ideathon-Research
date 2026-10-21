# Team Proposal: Distributed Two-Node PPG & IMU Wearable Architecture
## Contributor Proposal: Asmita Manral (CSE, IIIT) — "CardioSense" Design Blueprint

---

> **Status**: Archived Team Proposal & Design Option  
> **Source**: Team Technical Discussion (Asmita Manral, 2026-09-24)  
> **Repository Path**: `c:/College/Ideathon/Product_Design/Asmita_Two_Node_PPG_IMU_Proposal.md`  
> **Related Documents**:
> * 📄 [Dual-Node Sentry Pendant & PulseBand Architecture](file:///c:/College/Ideathon/Product_Design/Dual_Node_Pendant_and_Wristband_Architecture.md)
> * 📄 [Master Fixed vs Flexible Architecture](file:///c:/College/Ideathon/Product_Design/Master_Fixed_vs_Flexible_Architecture.md)
> * 📄 [Form Factor Evaluation: Pendant vs Patch](file:///c:/College/Ideathon/Product_Design/Form_Factor_Evaluation_Pendant_vs_Patch.md)

---

## 1. Executive Summary & Design Rationale

This document archives the design proposal submitted by **Asmita Manral (CSE IIIT)** regarding a distributed, privacy-preserving two-node wearable Body Area Network (termed *"CardioSense"* in the team discussions). 

The proposal centers on completely eliminating wet adhesive ECG hydrogel patches to maximize patient compliance and eliminate skin irritation, distributing physiological sensing across a **self-fitting wrist slap-band** and a **clothing-clipped sternal locket**.

---

## 2. Design Trade-Off Analysis: IMU Clip vs. ECG Adhesive Patch

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CURRENT DESIGN (IMU Clip):             │ ECG ADHESIVE PATCH DESIGN:         │
├────────────────────────────────────────┼────────────────────────────────────┤
│ ✅ Perfect daily compliance             │ ✅ Gold-standard arrhythmia         │
│ ✅ Zero skin irritation                 │ ✅ ST-segment ischemia flag         │
│ ✅ Works through clothing               │ ✅ Clinically superior HRV          │
│ ✅ Simple I2C hardware                  │ ✅ EDR breathing (validated)        │
│ ⚠️ Indirect breathing only             │ ❌ Daily adhesive reapply           │
│ ✅ Built-in fall detection             │ ❌ Skin irritation risk              │
│ ✅ Ultra-low BOM (~₹130 IMU stage)     │ ❌ Complex AFE circuit               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Sensing Modality Comparison: ECG vs. PPG

| Physiological Feature | Electrocardiography (ECG) | Photoplethysmography (PPG) | Team Clinical Assessment |
| :--- | :--- | :--- | :--- |
| **What it measures** | Cardiac electrical biopotentials (mV) | Arterial blood volume oscillations (optical) | ECG reflects electrical conduction; PPG reflects peripheral pulse hydraulics. |
| **Heart Rate (BPM)** | ✅ **Extremely Precise** (from R-R peak intervals) | ✅ **Good** (from AC pulsatile peak detection) | Both adequate at rest; PPG susceptible to peripheral motion. |
| **Heart Rate Variability (HRV)**| ✅ **Gold Standard** (sub-millisecond R-peak timing) | ⚠️ **Good but noisier** (pulse arrival jitter & motion) | PRV approximates HRV well in resting supine states. |
| **Blood Oxygen ($SpO_2$)** | ❌ **Impossible** (measures electricity, not light absorption) | ✅ **Yes** (dual-wavelength Red 660nm / IR 940nm ratio-of-ratios) | PPG is essential for hypoxia and respiratory failure tracking. |
| **Arrhythmia Classification (VT/AF)**| ✅ **Definitive** (P-wave, QRS duration, ST morphology) | ⚠️ **Partial** (rhythm irregularity only, no waveform morphology)| PPG detects pulse deficit, but cannot differentiate VT from aberrancy. |
| **ST-Segment Ischemia Detection** | ✅ **Gold Standard clinical diagnostic** | ❌ **Impossible** (no electrical voltage waveform) | Crucial reason why mechanical SCG or multi-modal surrogates are needed if ECG is dropped. |
| **QT Interval (VF Risk Marker)**| ✅ **Directly measurable** | ❌ **Not available** | Requires electrical repolarization tracking. |
| **Atrial Fibrillation (AF) Detection** | ✅ **Definitive** (loss of P-waves, irregular QRS) | ✅ **Clinically Validated** (irregular pulse interval tachogram)| Optical PPG is FDA-cleared for AFib screening in consumer smartwatches. |

---

## 4. Asmita's Full Proposed Abstract & Specification

### Title:
**CardioSense: A Distributed Two-Node Embedded AI Wearable for Pre-Arrest Cardiac Anomaly Detection via Multi-Modal Sensor Fusion and Motion-Gated Edge Inference**

### Proposed Abstract:
> *"Out-of-hospital Sudden Cardiac Arrest (SCA) claims over 350,000 lives annually with an out-of-hospital survival rate below 5% in developing regions like India, where emergency transit times average 20–40 minutes—far exceeding the 4-minute biological brain-death window. Existing consumer smartwatches only alert after complete pulse loss (post-collapse), which is biologically futile, while suffering from pervasive motion-induced false alarms. Furthermore, single-wrist wearables cannot measure thoracic respiration mechanics and miss multi-system autonomic precursors.
>
> We propose CardioSense, a distributed, privacy-preserving two-node embedded AI wearable designed to exploit the 15-to-30 minute precursor window before cardiac collapse. The system decouples sensing anatomically: a self-fitting wrist slap-band monitors radial optical PPG (Heart Rate, SpO2) and palmar galvanic skin response (autonomic cold-sweat diaphoresis); while a clothing-clipped sternum locket monitors chest-wall respiration rate/depth through clothing and detects mechanical collapse (free-fall to impact to stillness) via an MPU6050 accelerometer.
>
> Both nodes stream synchronized telemetry at 20 Hz via Bluetooth Low Energy to an on-device dual-core ESP32 microcontroller running an unsupervised TinyML Autoencoder anomaly detection model (8→4→2→4→8). Rather than requiring rare catastrophic cardiac-event training data, the model learns each wearer's healthy resting baseline across all fused signals. A kinetic motion gate dynamically scales anomaly thresholds against sternal Signal Vector Magnitude (SVM), distinguishing genuine cardiac distress from vigorous exercise.
>
> On detecting sustained multi-signal discordance at rest, a deterministic fail-safe initiates a 30-second local haptic and audible countdown, allowing conscious wearers to abort false alarms via a physical tactile button. If uncancelled, the system autonomously escalates to an 85 dB local siren, dispatches a location-tagged emergency SMS with Google Maps coordinates via a SIM800L cellular modem, and dials an automated caregiver telephone call with DTMF emergency tones.
>
> The architecture incorporates a Dual-Tier AI framework: Tier 1 operates 100% offline on-device in under 18 µs for deterministic detection, while Tier 2 translates received telemetry into a standardized clinical SBAR (Situation, Background, Assessment, Recommendation) trauma brief for hospital emergency staff and launches an automated bystander voice coach pacing CPR chest compressions at 110 BPM.
>
> In accordance with pre-clinical research ethics, the system was validated via in-silico computational simulation on physiological trajectories modeled after clinical bounds from the MIMIC-III database. In simulation, the TinyML Autoencoder achieved 100% precursor sensitivity and 99.0% baseline specificity (71.09x reconstruction error amplification). With a 376-byte model footprint running on ESP32 FreeRTOS and a total prototype BOM under ₹3,150 ($37), CardioSense delivers an accessible, offline, privacy-preserving cardiac early-warning ecosystem."*

---

## 5. Architectural Breakdown & Hardware Topology

```
===================================================================================================================
                             ASMITA'S PROPOSED TWO-NODE EMBEDDED TOPOLOGY
===================================================================================================================

       [ NODE 1: STERNAL CLOTHING-CLIPPED LOCKET ]             [ NODE 2: SELF-FITTING WRIST SLAP-BAND ]
    ─────────────────────────────────────────────           ──────────────────────────────────────────────
     Location: Over Sternum (Clipped to clothing)            Location: Non-dominant Wrist & Palm
     Form: Lightweight Locket / Brooch Clip                  Form: Self-fitting Slap-Band
     Skin Contact: Zero (Works through fabric)               Skin Contact: Direct optical & palmar contact
     
     SENSORS & TRANSDUCERS:                                  SENSORS & TRANSDUCERS:
     • 6-Axis Accelerometer (MPU6050)                        • Optical PPG (Heart Rate, SpO2)
       - Chest-wall respiratory rate & depth through fabric  • Palmar Galvanic Skin Response (GSR)
       - Free-fall detection (airborne phase)                  - Autonomic cold-sweat diaphoresis
       - Impact force transient measurement                 • Physical Tactile Cancel Button
       - Post-impact motionless state detection              • Local Haptic Buzzer
                           │                                                       │
                           └───────────────── BLE 20 Hz STREAM ───────────────────┘
                                                      │
                                                      ▼
                                       [ ESP32 DUAL-CORE BASE PROCESSING ]
                                       • Unsupervised TinyML Autoencoder (8→4→2→4→8)
                                       • Kinetic Motion Gate (Sternal SVM Scaling)
                                       • Latency: <18 µs per inference (376-byte footprint)
                                                      │
                                   ┌──────────────────┴──────────────────┐
                                   ▼                                     ▼
                      [ TIER 1: DETERMINISTIC ESCALATION ]    [ TIER 2: CLINICAL HANDOFF ]
                      • 30-Second Abort Countdown             • Standardized SBAR Trauma Brief
                      • 85 dB Local Siren                     • Bystander Voice Coach (110 BPM CPR)
                      • SIM800L GSM/GPRS Cellular Modem
                        - Location SMS with Google Maps link
                        - Caregiver voice call + DTMF tones
===================================================================================================================
```

---

## 6. Integration Notes & Synthesis with Master Research Dossier

1. **Alignment on Zero-Adhesive Philosophy**:
   * Asmita's proposal reinforces the core team decision to eliminate wet Ag/AgCl hydrogel electrodes, avoiding the Day-5 desiccation wall and medical adhesive-related skin injuries (MARSI).
2. **Key Innovations to Incorporate**:
   * **Palmar GSR for Autonomic Diaphoresis**: Cold sweat is a classic clinical precursor of acute coronary syndrome and cardiogenic shock. Adding skin conductance to the wristband provides an invaluable non-invasive autonomic marker.
   * **Clothing-Clipped Mounting**: Clipping to an undershirt or shirt pocket eliminates all skin adhesives.
   * **Unsupervised Baseline Autoencoder**: Training an on-device autoencoder on individual resting baselines solves the scarcity of catastrophic arrest training data.
   * **Bystander CPR Voice Coach (110 BPM)**: An outstanding ideathon feature that actively bridges the 4-minute brain-death gap before paramedics arrive.
   * **Standardized SBAR Brief**: Delivering an actionable clinical summary directly to incoming emergency room staff.
3. **Engineering Considerations for Next Phase**:
   * **Acoustic Coupling vs. Fabric**: While gross respiration and fall impact transmit well through clothing, subtle mechanical micro-g heart vibrations (Seismocardiography / aortic opening recoil) require direct physical contact with the breastbone (via soft tension cord or elastic preload).
   * **Validation Framing**: When presenting at the ideathon, computational simulations on MIMIC-III should be framed as the *planned evaluation methodology* rather than completed clinical validation.
