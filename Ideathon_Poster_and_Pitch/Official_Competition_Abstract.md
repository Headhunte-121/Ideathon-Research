# Official Ideathon Competition Abstract & Submission Dossier
## Pre-Arrest Cardiac Anomaly Detection via Multi-Modal Two-Node Wearable Body Area Network

---

> **Status**: Official Competition Deliverable  
> **Target Event**: College Medical IoT Ideathon  
> **Development Stage**: Conceptual Proposal & Systems Engineering Architecture (Validation Planned / Proposed)  
> **Repository Path**: `c:/College/Ideathon/Ideathon_Poster_and_Pitch/Official_Competition_Abstract.md`  
> **Related Documents**:
> * 📄 [A0 Modular Poster Canvas](file:///c:/College/Ideathon/Ideathon_Poster_and_Pitch/A0_Poster_Modular_Canvas.md)
> * 📄 [Master Pitch & Poster Guide](file:///c:/College/Ideathon/Ideathon_Poster_and_Pitch/Master_Pitch_and_Poster_Guide.md)
> * 📄 [Asmita Two-Node PPG & IMU Proposal](file:///c:/College/Ideathon/Product_Design/Asmita_Two_Node_PPG_IMU_Proposal.md)

---

## 📄 Primary Submission Version (Official Abstract — Brand-Neutral & Stage-Accurate)

### Title:
**A Distributed Two-Node Embedded Wearable for Pre-Arrest Cardiac Anomaly Detection via Multi-Modal Sensor Fusion and Motion-Gated Edge Inference**

### Abstract (430 Words):
Out-of-hospital Sudden Cardiac Arrest (SCA) claims over 350,000 lives annually with an out-of-hospital survival rate below 5% in regions like India, where emergency transit times average 20 to 40 minutes—far exceeding the 4-minute biological window before irreversible anoxic brain injury. Current monitoring paradigms exhibit critical clinical limitations: consumer smartwatches sound alarms only after complete pulse cessation occurs post-collapse, which is biologically futile, while suffering from pervasive motion-induced false alarms and an inability to track respiration. Conversely, clinical Holter monitors and adhesive ECG patches rely on wet hydrogel electrodes that require daily reapplication, cause contact dermatitis, and suffer from poor long-term patient compliance.

To address these challenges, we propose a distributed, privacy-preserving two-node wearable Body Area Network designed to intercept the pre-infarction countdown before cardiac collapse without single-use skin adhesives. The system decouples physiological sensing across two ergonomic body locations: a companion wristband monitors radial optical photoplethysmography alongside palmar galvanic skin response to capture autonomic cold-sweat diaphoresis; simultaneously, a modular 2-in-1 Sentry Pod resting over the lower sternum captures continuous on-contact dry 316L stainless steel precordial ECG synchronized with seismocardiographic (SCG) mechanical vibrations to calculate Pre-Ejection Period (PEP) contractility delay, while enabling a clothing-clip casual mode with 30-second finger spot-check ECG.

The proposed architecture streams synchronized telemetry over Bluetooth 5.3 Low Energy to an on-device Nordic Semiconductor nRF5340 dual-core ARM Cortex-M33 microcontroller. The firmware executes a 28-microsecond hybrid NLMS adaptive filter and discrete wavelet transform pipeline to strip motion artifacts, feeding a pre-trained foundational CNN-LSTM paired with an unsupervised on-device autoencoder that calibrates to the wearer’s individual healthy resting baseline across all fused signals.

Upon detecting sustained multi-signal ischemic discordance during rest, a deterministic fail-safe initiates a 30-second local haptic and visual countdown, enabling conscious wearers to abort false alarms via a physical tactile button with hardware fall lockout. If uncancelled, the system routes high-priority emergency telemetry through a paired smartphone gateway to dispatch location-tagged emergency SMS alerts, dial emergency medical services, and stream ECG buffers to hospital portals. For verified physical collapse, the device activates a syncope-gated 85 dB siren and 110 BPM bystander CPR voice coach.

Planned evaluations combine in-silico computational simulations using public clinical databases (PTB-XL, MIMIC-III) to establish precursor sensitivity and motion-rejection bounds, followed by benchtop hardware integration. By combining glue-free electro-mechanical sensing, personalized baseline anomaly detection, and autonomous escalation, this proposed platform offers an accessible, practical early-warning ecosystem for pre-arrest cardiac intervention.

---

## 📋 Short Executive Summary (Exact 100-Word Portal Submission)

### ⭐ Recommended Balanced Version (Clean, High-Credibility, Zero Jargon Clutter)
> "Sudden Cardiac Arrest claims over 350,000 lives annually, yet smartwatches only alert wearers after the heart electrically stops. We developed a two-node wearable system providing modular clothing-clip, skin-adhesive, or glue-free wear to intercept heart attacks hours before collapse. A lightweight sternal pod captures dry-contact ECG rhythms and mechanical heart vibrations, while a companion wristband tracks optical blood pulses and sudden cold sweats. On-device AI filters out walking movement to eliminate false alarms and learns the wearer's resting baseline. Upon emergency collapse, the system provides a 30-second cancellation window, dispatches smartphone alerts, and activates an 85 dB bystander CPR voice coach."

### Option 2: Ultra-Plain Everyday English
> "Sudden Cardiac Arrest kills over 350,000 people every year because smartwatches only detect an event after the heart stops. We engineered a glue-free, two-device wearable system to warn patients hours before a heart attack happens. A small chest pod feels the heart's physical pumping vibrations and electrical rhythms without sticky pads, while a comfortable companion wristband tracks blood flow and sudden cold sweats. Smart on-device software filters out walking motion to prevent false alarms. If a real collapse occurs, the system gives 30 seconds to cancel, automatically calls emergency services, and guides bystanders with a loud, step-by-step CPR voice coach."

### Option 3: Deep Technical Specification (For Biomedical Engineers)
> "Sudden Cardiac Arrest kills over 350,000 people annually, with smartwatches sounding alarms only after post-collapse electrical arrest. We propose an adhesive-free, two-node Body Area Network to intercept the 1-to-6-hour pre-infarction countdown. A modular sternal pod captures on-contact dry ECG and mechanical SCG vibrations, calculating Pre-Ejection Period contractility decay, while a companion wristband tracks optical pulse and palmar cold-sweat diaphoresis. Telemetry streams via BLE 5.3 to a dual-core Nordic nRF5340 microcontroller running hybrid wavelet denoising and personalized edge AI autoencoders. Emergency alerts feature a 30-second tactile abort button, smartphone dispatch, a syncope-gated 85 dB siren, and 110 BPM bystander CPR coaching."

---

## 📑 Team Reference: Asmita's Original Draft ("CardioSense" Title)

### Title:
**CardioSense: A Distributed Two-Node Embedded AI Wearable for Pre-Arrest Cardiac Anomaly Detection via Multi-Modal Sensor Fusion and Motion-Gated Edge Inference**

*(Full source text, feature comparison matrix, and engineering notes preserved in [`Product_Design/Asmita_Two_Node_PPG_IMU_Proposal.md`](file:///c:/College/Ideathon/Product_Design/Asmita_Two_Node_PPG_IMU_Proposal.md))*
