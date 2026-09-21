# Master Research Questionnaire: Systems Architecture for Wearable Cardiac Arrest Prediction
### Ideathon & Medical IoT Product Development Blueprint

---

> **Purpose**: This questionnaire maps the complete lifecycle of a medical-grade IoT wearable designed for early detection and prediction of Sudden Cardiac Arrest (SCA). It incorporates the original 9 engineering phases, deepens each with critical systems-level expansion questions, and introduces 3 missing structural phases (Human Factors, Failure States/Failsafes, and Health Economics/Ideathon Pitch Strategy) to eliminate technical blind spots before judges and clinical evaluators.

---

## Phase 1: Pathophysiology & Biomarker Discovery (The Biology)
**Objective**: Understand the exact timeline, cellular mechanisms, and physiological signatures of a failing heart.

* **Q1.1**: What is the precise cascade of physiological, chemical, and autonomic nervous system changes that occur in the human body 1 to 6 hours before acute myocardial ischemia or infarction?
* **Q1.2**: Which of these pre-event changes produce physical outputs (e.g., electrical, mechanical, thermal, or circulatory) that can be measured non-invasively?
* **Q1.3**: Do these biomarkers present themselves differently based on demographics (e.g., age, gender, preexisting conditions)?
* **Q1.4 [EXPANSION - Differential Diagnosis & Confounders]**: How does the physiological cascade of impending Sudden Cardiac Arrest (SCA) biologically differ from non-lethal benign confounders—such as severe panic attacks, intense exercise-induced tachycardia, vasovagal syncope, or epileptic seizures? What specific multi-biomarker decoupling rules separate an emotional surge from true myocardial ischemia?
* **Q1.5 [EXPANSION - Circadian & Chronobiological Triggers]**: Given that epidemiological data indicates a major peak of sudden cardiac deaths between 6:00 AM and 12:00 PM (associated with morning cortisol spikes, platelet hyper-reactivity, and sympathetic awakening), how should the biomarker baseline adapt dynamically to circadian rhythms and sleep-stage transitions (e.g., REM sleep heart rate surges vs. obstructive sleep apnea desaturations)?

---

## Phase 2: Signal Acquisition Modalities (The Physics)
**Objective**: Determine the best physical methods and sensor interfaces to capture the underlying biology.

* **Q2.1**: What physical sensing modalities (optical, electrical, acoustic, bio-impedance, mechanical) map to each of the biomarkers identified in Phase 1?
* **Q2.2**: For each potential sensing modality, what is the anatomical "sweet spot" on the human body to achieve the highest Signal-to-Noise Ratio (SNR)?
* **Q2.3**: What are the minimum required sampling frequencies and bit resolutions to achieve diagnostic-grade readings for each respective modality?
* **Q2.4 [EXPANSION - Optical Skin Tone & Melanin Inclusivity]**: How does skin pigmentation (Fitzpatrick skin phototypes I through VI) alter the optical absorption coefficients of Green (525nm), Amber (590nm), Red (660nm), and Infrared (940nm) PPG wavelengths? What dynamic optical front-end adjustments (such as automatic LED current modulation and programmable transimpedance gain) are mandatory to avoid clinical bias across diverse demographic populations?
* **Q2.5 [EXPANSION - Long-Term Skin-Electrode Interface Physics]**: How does the skin-electrode contact impedance ($Z_{contact}$) drift over 7 to 14 days of continuous wear due to epidermal stratum corneum hydration, sweat buildup, and natural epidermal shedding? What electrode chemistries (e.g., solid hydrogel, silver/silver chloride (Ag/AgCl), carbon-loaded conductive polymers, or dry microneedle arrays) maintain stable half-cell potential without inducing contact dermatitis?

---

## Phase 3: Analog & Digital Signal Processing (The Noise)
**Objective**: Isolate true biological signals from mechanical, environmental, and electrical noise.

* **Q3.1**: What are the most common sources of signal degradation (e.g., motion artifact, ambient light, electromagnetic interference, skin temperature fluctuations) for body-worn sensors?
* **Q3.2**: What hardware-level analog filtering components are mandatory before a biological signal is converted into digital data?
* **Q3.3**: What software-level digital signal processing (DSP) algorithms are most effective for dynamically removing unpredictable motion noise from continuous biometric waveforms?
* **Q3.4 [EXPANSION - Morphological vs. Positional Artifact Discrimination]**: How does the DSP pipeline distinguish between genuine ischemic ST-segment shifts and benign baseline wander caused by postural transitions (e.g., a patient rolling from their back onto their left lateral recumbent position, shifting the heart's anatomical axis relative to the electrodes)?
* **Q3.5 [EXPANSION - Real-Time Signal Quality Index (SQI) Architecture]**: What quantitative metrics (e.g., spectral distribution ratio, higher-order kurtosis, template cross-correlation) can run in real-time with sub-milliwatt power draw to generate a continuous confidence score, preventing downstream AI models from processing corrupted signal frames?

---

## Phase 4: Data Engineering & Preprocessing (The Data)
**Objective**: Build a clean, leak-free, representative dataset pipeline to train predictive AI models.

* **Q4.1**: Which open-source, peer-reviewed clinical databases contain continuous, multi-parameter waveform data leading up to—and during—cardiac events?
* **Q4.2**: How do data scientists mathematically label a "pre-event window" (e.g., labeling the data 45 minutes prior to the event) so the model learns to forecast rather than just detect?
* **Q4.3**: How do you time-synchronize and align data streams that have completely different sampling frequencies (e.g., combining a 250Hz wave with a 10Hz wave)?
* **Q4.4**: How should the system handle missing data or "dropped packets" (e.g., if a sensor temporarily loses skin contact for 5 seconds)?
* **Q4.5 [EXPANSION - Patient-Wise Splitting & Data Leakage Prevention]**: What validation protocols (e.g., Leave-One-Subject-Out Cross-Validation vs. Stratified Group K-Fold) are non-negotiable to prevent data leakage between beats belonging to the same individual? How do you mathematically guarantee that the model is learning generalized ischemic disease patterns rather than patient-specific morphological signatures?
* **Q4.6 [EXPANSION - Label Noise & Inter-Annotator Variability]**: In clinical databases, cardiologists frequently disagree on the precise onset time of ischemia or border boundaries of microvolt T-wave alternans. How does the data pipeline address label ambiguity (e.g., using label smoothing, soft probabilistic targets, or consensus-voting matrices)?

---

## Phase 5: Machine Learning Architecture (The Brain)
**Objective**: Define the mathematical structure that predicts future cardiac events with high fidelity.

* **Q5.1**: What classes of neural networks or machine learning models are explicitly designed for multivariate, continuous time-series forecasting?
* **Q5.2**: What is the mathematical difference between Data-Level Fusion, Feature-Level Fusion, and Decision-Level Fusion, and which is safest for medical diagnostics?
* **Q5.3**: Because cardiac events are rare, datasets are highly imbalanced. What specific loss functions, weighting, or synthetic augmentation techniques prevent the AI from defaulting to a "Normal/Healthy" prediction?
* **Q5.4**: What evaluation metrics beyond pure "accuracy" (e.g., Sensitivity, Specificity, F1-Score, Area Under Precision-Recall Curve) must be used to prove a medical model's viability?
* **Q5.5 [EXPANSION - Explainability & Clinical Interpretability (XAI)]**: Given that black-box models are widely rejected by cardiologists and medical regulatory bodies, how does the architecture expose its decision pathway (e.g., via Integrated Gradients, Attention Rollout maps, or counterfactual time-series explanations) to highlight the exact ECG segments or autonomic indices driving an alert?
* **Q5.6 [EXPANSION - Out-of-Distribution (OOD) & Epistemic Uncertainty Estimation]**: How does the machine learning engine estimate its own confidence (e.g., via Monte Carlo Dropout, Evidential Deep Learning, or conformal prediction)? If an elderly patient with an undocumented pacemaker or severe bundle branch block wears the device, how does the model recognize that it cannot evaluate this rhythm reliably and flag a warning instead of making a wrong prediction?

---

## Phase 6: Edge Computing & TinyML (The Embedded Logic)
**Objective**: Execute deep learning inference locally on ultra-low-power microcontrollers without cloud dependency.

* **Q6.1**: What post-training mathematical techniques (e.g., Quantization, Pruning, Weight Clustering) are used to shrink a deep learning model's memory footprint without destroying its predictive power?
* **Q6.2**: What are the primary computational bottlenecks (e.g., SRAM capacity, Flash storage, Multiply-Accumulate operations) when running time-series inferences on deeply constrained microcontrollers?
* **Q6.3**: What specific microcontroller hardware features (e.g., Neural Processing Units, Vector Extensions, hardware FPUs) drastically reduce the time it takes to run an AI inference?
* **Q6.4 [EXPANSION - Hierarchical "Sentry" Pipeline vs. Monolithic Inference]**: Why is running a large neural network continuously on an MCU unsustainable for battery life, and how is an event-driven multi-stage pipeline designed (e.g., Stage 0: analog threshold $\rightarrow$ Stage 1: lightweight DSP feature gate $\rightarrow$ Stage 2: quantized TinyML neural inference)?
* **Q6.5 [EXPANSION - Secure Over-the-Air (OTA) Model Updating & Rollback]**: How are updated model weights and firmware delivered to an edge device over low-bandwidth BLE connections without bricking the device or exposing it to model poisoning attacks?

---

## Phase 7: IoT System Architecture & Communications (The Network)
**Objective**: Ensure zero-latency, fail-safe communication of life-critical alerts to the outside world.

* **Q7.1**: If a system requires multiple physical sensing nodes on the body, what are the trade-offs between distributed processing (each node runs AI) versus centralized processing (nodes send raw data to one master brain)?
* **Q7.2**: What Body Area Network (BAN) wireless protocols provide the optimal balance between high continuous data throughput and ultra-low power consumption?
* **Q7.3**: How is an emergency alert securely escalated from a local Bluetooth connection to a cellular network without requiring active user intervention?
* **Q7.4 [EXPANSION - Store-and-Forward Architecture in Network Dead Zones]**: If a user experiences an impending cardiac arrest in a shielded environment (e.g., an underground metro station, high-altitude flight, or remote area with zero cellular/Wi-Fi coverage), how does the system queue, buffer, and prioritize telemetry packets, and what localized fallback actions (e.g., high-decibel acoustic beacon, emergency beacon broadcast) are triggered?
* **Q7.5 [EXPANSION - Bystander & Automated External Defibrillator (AED) Integration]**: How can the emergency escalation architecture interface with crowd-sourced emergency response networks (e.g., GoodSAM, PulsePoint) and nearby smart IoT AED cabinets to guide bystanders to the victim before irreversible brain damage occurs (the 4-minute window)?

---

## Phase 8: Power Management & Mechanical Design (The Hardware Reality)
**Objective**: Guarantee multi-day continuous wearability, skin safety, and thermal integrity in real-world conditions.

* **Q8.1**: What is the concept of "Duty Cycling" in embedded systems, and how can it be optimized for continuous biometric monitoring without missing critical events?
* **Q8.2**: Based on the continuous power draw of sensors, MCUs, and radios, what battery chemistries and capacities are viable for a form factor worn continuously?
* **Q8.3**: How does physical form factor (e.g., rigid watch, flexible patch, smart ring) affect sensor-to-skin coupling and long-term user compliance?
* **Q8.4 [EXPANSION - Ingress Protection (IP Rating) & Shower/Sweat Durability]**: How can a wearable patch achieve IP67 or IP68 water resistance to withstand daily hot showers and vigorous sweat excretion while maintaining a breathable microporous membrane to prevent skin maceration?
* **Q8.5 [EXPANSION - Thermal Safety & Tissue Heating Limits]**: Under medical standard IEC 60601-1, body-contact surfaces must not exceed $41^\circ\text{C}$ to prevent thermal skin damage over extended wear. How must power dissipation across optical LEDs, PMICs, and processing cores be managed under peak compute conditions?

---

## Phase 9: Clinical Safety & Regulatory Viability (The Reality Check)
**Objective**: Navigate medical certification, safety standards, and patient data privacy frameworks.

* **Q9.1**: What are the catastrophic clinical risks of "Alarm Fatigue" caused by false positives, and how must a predictive algorithm be calibrated to mitigate this?
* **Q9.2**: In India (or globally), how is software that generates a predictive medical alert classified by regulatory bodies (e.g., CDSCO Software as a Medical Device / SaMD guidelines)?
* **Q9.3**: What encryption and on-device data anonymization standards are required when handling continuous biometric data to protect patient privacy?
* **Q9.4 [EXPANSION - Legal Liability & "Good Samaritan" Emergency Actions]**: What are the legal and liability boundaries if:
  1. The device experiences a False Negative (fails to predict an event and the patient dies)?
  2. The device triggers a False Positive that leads to unwarranted emergency interventions (e.g., an unnecessary defibrillator shock or bystander chest compressions causing fractured ribs)?
* **Q9.5 [EXPANSION - Clinical Trial Protocol & Prospective Validation]**: What phase-gated clinical trial protocol (retrospective database benchmarking $\rightarrow$ simulated in-hospital telemetry validation $\rightarrow$ prospective multi-center ambulatory clinical trials) is required to establish statistical equivalence or superiority against standard hospital telemetry monitors?

---

## Phase 10: Human Factors & Ergonomic Behavioral Engineering (The Human)
**Objective**: Address user psychology, long-term adherence, and behavioral barriers to continuous wear.

* **Q10.1 [NEW]**: What are the primary reasons patients discontinue wearing cardiac monitors (e.g., skin itching, adhesive pain upon removal, device bulk under clothing, stigma, battery charging anxiety), and how can the mechanical design solve each?
* **Q10.2 [NEW]**: How does receiving continuous cardiac risk predictions affect a patient’s mental health (e.g., triggering "cardiophobia" or chronic panic attacks), and how should the user interface (UI/UX) present predictive health data to avoid inducing iatrogenic anxiety?
* **Q10.3 [NEW]**: How is a fail-safe "Cancel Alarm" interaction designed for elderly or non-tech-savvy users who may panic during a false-alarm countdown? What physical interactions (e.g., double-tap confirmation, voice command, physical button press) prevent accidental cancellations while keeping the barrier low for conscious users?

---

## Phase 11: Failure Modes, Redundancy & Safe-State Architecture (The Failsafe)
**Objective**: Formulate the engineering responses to component breakdowns and edge-case errors.

* **Q11.1 [NEW]**: What is the formal Failure Mode and Effects Analysis (FMEA) for the patch? If the optical sensor fails, the battery undergoes sudden capacity drop, or an electrode peels off, how does the system transition into a deterministic "Fail-Safe" state rather than giving silent failures?
* **Q11.2 [NEW]**: How does the embedded software architecture prevent memory corruption or MCU lockup (e.g., hardware watchdog timers, non-maskable interrupt routines, cyclic redundancy checks (CRC) on configuration registers)?
* **Q11.3 [NEW]**: If the patient suffers sudden cardiac arrest at the exact moment the device battery drops below minimum operating voltage, how does the power supply hierarchy guarantee sufficient reserve capacitor energy to transmit an emergency SOS beacon before full power collapse?

---

## Phase 12: Health Economics, Market Strategy & Ideathon Pitch Architecture (The Business & Impact)
**Objective**: Build a compelling commercial, logistical, and economic argument to convince Ideathon judges and venture investors.

* **Q12.1 [NEW]**: What is the Health Economics justification (Cost per Quality-Adjusted Life Year / QALY saved)? How does early prediction of SCA reduce the astronomical costs of intensive care unit (ICU) hospital stays, anoxic brain damage rehabilitation, and emergency medical transports?
* **Q12.2 [NEW]**: What is the initial beachhead Target Addressable Market (TAM)? Rather than marketing to the general public, how can the product target ultra-high-risk cohorts first (e.g., post-PCI/CABG discharge patients during their 30-day recovery window, heart failure patients with Left Ventricular Ejection Fraction $\text{LVEF} < 35\%$ awaiting ICD implantation)?
* **Q12.3 [NEW]**: What is the sustainable unit economics and business model? Does the product follow a "Razor-and-Blade" model (a reusable, sterilizable electronic hub with low-cost disposable adhesive sensor patches) or a subscription-based Remote Patient Monitoring (RPM) model reimbursed under medical insurance codes?

---

## Ideathon Judge Defense Checklist: Anticipated Questions & Defense Angles

| Category | Typical Hard Question From Ideathon Judges | How This Expanded Questionnaire Equips You to Defend |
| :--- | :--- | :--- |
| **Medical Validity** | *"Isn't sudden cardiac arrest unpredictable? Aren't you conflating a heart attack with an arrest?"* | **Phases 1 & 12**: You explain the 70–80% ischemic trigger cascade, the electrophysiological action potential alternans, and focus strictly on high-risk clinical populations. |
| **Signal Physics** | *"Smartwatches already do ECG and PPG. Why do you need a new device?"* | **Phases 2 & 8**: You highlight the physics: wrist ECG requires two hands (impossible during syncope/collapse), wrist PPG has high motion noise, and only a precordial chest patch captures Seismocardiography (SCG) and true ST vectors. |
| **AI Reliability** | *"How can I trust your 99% accuracy if you only have 20 arrest cases in your dataset?"* | **Phases 4 & 5**: You demonstrate mastery over patient-wise cross-validation, PR-AUC over AUROC, out-of-distribution uncertainty, and explainable AI (XAI). |
| **Engineering Reality** | *"Your deep learning model will kill the battery in 4 hours."* | **Phases 6 & 8**: You present the Hierarchical Sentry pipeline (analog comparator $\rightarrow$ tiny DSP $\rightarrow$ INT8 quantized TinyML), showing sub-1mA current draw and 10+ day battery life. |
| **Clinical Adoption** | *"Doctors hate false alarms. Your app will be deleted in 2 days."* | **Phases 3, 9 & 10**: You present the 2-tier SQI-gated multi-modal corroboration rule, the 30-second patient cancellation interlock, and human factor ergonomics. |
| **Regulatory & Business** | *"How will you ever get this approved by CDSCO / FDA?"* | **Phases 9 & 12**: You outline the exact SaMD Class C / Class II De Novo pathway, ISO 13485 / IEC 62304 standards, and the post-hospital discharge beachhead market. |

---

# Part II: Component-Level Sensor Deep-Dive Framework (Systems Integrator Perspective)
> Detailed standalone reference also available at: [Sensor_Evaluation_Deep_Dive_Framework.md](file:///c:/College/Ideathon/Sensor_Evaluation_Deep_Dive_Framework.md)

### Category 1: Communication & Interface (How it talks to the Brain)
* **Q1.1**: Does this specific sensor output an Analog signal (requiring the microcontroller's ADC to read it) or a Digital signal?
* **Q1.2**: If it is digital, what communication protocol does it use (e.g., I2C, SPI, or UART)?
* **Q1.3**: Does this sensor require dedicated interrupt pins (to wake the microchip up only when a threshold is met), and how does that affect the wiring diagram?
* **Q1.4 [EXPANSION - Bus Contention & Fixed I2C Address Collisions]**: If multiple digital sensors share the same I2C bus, do their 7-bit device addresses collide (e.g., fixed address `0x57` on many optical sensors)? Does the system require a dual I2C peripheral, an I2C multiplexer (e.g., TCA9548A), or a transition to SPI with dedicated Chip-Select (`CS`) lines?
* **Q1.5 [EXPANSION - Multi-Sensor Clock Synchronization (Jitter Prevention)]**: To calculate cross-modal metrics like Pulse Arrival Time (PAT), sensor clocks must not drift. Does the sensor accept an external clock pin (`CLKIN`) or hardware synchronization trigger pin (`SYNC`), or must the MCU software timestamp samples using hardware input-capture timers?
* **Q1.6 [EXPANSION - Bus Bandwidth & Max Bus Speed]**: What is the maximum bus speed supported (e.g., I2C 400 kHz vs SPI 10–20 MHz)? At your target multi-channel sampling rate, what percentage of the bus bandwidth is consumed?

### Category 2: Power Consumption & Voltage (The Battery Budget)
* **Q2.1**: What is the operating voltage range of this sensor (e.g., 1.8V, 3.3V, 5V), and does it match the logic level of the microcontroller without needing a level-shifter?
* **Q2.2**: What is the exact current draw (measured in mA or µA) when the sensor is actively taking a measurement?
* **Q2.3**: Does this sensor feature an ultra-low-power "Standby" or "Sleep" mode, and what is the current draw during that state?
* **Q2.4 [EXPANSION - Power Rail Sequencing & Latch-Up Vulnerability]**: Does the IC require separate analog ($V_{DD\_ANA}$) and digital ($V_{DD\_IO}$) rails? Is there a strict power-up sequencing requirement to prevent destructive parasitic thyristor latch-up?
* **Q2.5 [EXPANSION - Peak Pulsed Current vs. Average Current]**: Optical LEDs draw short high-energy pulses (e.g., 20–50 mA for 20 µs). Can onboard decoupling capacitors and LDOs supply these transient peaks without causing internal voltage droop that triggers an MCU brownout reset?
* **Q2.6 [EXPANSION - Startup & Stabilization Latency]**: How long does the sensor take to boot and settle its analog front-end (wake-up time from Deep Sleep to valid data)? If a sensor draws 10 µA in sleep but requires 150 ms of 5 mA draw just to stabilize internal references, frequent duty cycling may consume more energy than continuous low-power operation.

### Category 3: Data Quality & Built-in Processing (What it actually gives the AI)
* **Q3.1**: What is the ADC resolution (e.g., 12-bit, 16-bit, 24-bit) of this sensor, and is it high enough to capture the micro-changes required by the AI?
* **Q3.2**: Does this sensor contain its own integrated Digital Signal Processing (DSP) or hardware filters (e.g., built-in ambient light rejection or motion-artifact cancellation), or does the microcontroller have to do all the math?
* **Q3.3**: What is the maximum sampling rate (Hz) this sensor can achieve, and does it possess a hardware FIFO (First-In-First-Out) buffer to store data temporarily so the microcontroller can sleep longer?
* **Q3.4 [EXPANSION - FIFO Watermark & Burst DMA Transfers]**: What is the depth of the internal FIFO buffer (e.g., 32 samples vs 512 bytes)? Does the sensor support a programmable "Watermark Interrupt" that wakes the MCU only when the FIFO is 80% full, allowing high-speed burst reading via Direct Memory Access (DMA) while the MCU core sleeps 95% of the time?
* **Q3.5 [EXPANSION - Dynamic Range, Programmable Gain & Saturation Recovery]**: Does the sensor feature a Programmable Gain Amplifier (PGA)? If a sudden motion artifact saturates the ADC (clipping at rail voltage), what is the recovery time before the analog front-end returns to its linear operating region?

### Category 4: Physical Constraints & Wearability (How it touches the human)
* **Q4.1**: What are the physical dimensions (footprint) of the IC or the sensor module?
* **Q4.2**: What are the exact physical coupling requirements for this sensor to work (e.g., does it require wet conductive gel, dry electrodes, precise optical pressure, or direct skin contact)?
* **Q4.3**: Does this sensor require baseline calibration for every new user, or does it work out-of-the-box universally?
* **Q4.4 [EXPANSION - PCB Packaging & Solderability for Prototyping]**: What is the physical IC package type (e.g., QFN, SOIC, LGA, or Wafer-Level Chip-Scale Package / WLCSP)? Can the team prototype with QFN/LGA packages or breakout boards, given that WLCSP requires expensive HDI PCBs with laser microvias and cannot be hand-soldered?
* **Q4.5 [EXPANSION - Contact Pressure Sensitivity & Motion Coupling]**: How sensitive is the sensor to variations in contact pressure? (e.g., in PPG, too little pressure allows ambient light leakage, while too much pressure occludes microcapillaries). How does the mechanical enclosure maintain constant coupling pressure?
* **Q4.6 [EXPANSION - Biocompatibility & Sweat Corrosion]**: Are exposed contacts, optical windows, or electrode surfaces chemically resistant to saline sweat ($NaCl$), sebum oils, and cleaning alcohol? Will gold plating, stainless steel (316L), or medical silicone degrade over 14 days of continuous wear?

### Category 5: Economic Feasibility (Is it a viable product?)
* **Q5.1**: Is this sensor a standard COTS (Commercial Off-The-Shelf) component, or is it a proprietary/experimental lab component?
* **Q5.2**: What is the average unit cost of this sensor at scale (e.g., buying 1,000 units)?
* **Q5.3 [EXPANSION - Global Stock Availability & Lead Time Risk]**: What is the active lifecycle status of the IC (Active, NRND, or EOL)? Are distributor stocks available immediately on DigiKey/Mouser/LCSC, or is there an 18-to-52 week supply chain lead time?
* **Q5.4 [EXPANSION - Second-Source Pin-to-Pin Compatibility]**: If this primary component experiences a global shortage, does an alternative pin-compatible second source exist, or will the company be forced to redesign the PCB?

### Category 6 [EXPANSION]: Firmware Ecosystem & Driver Availability (Software Reality)
* **Q6.1 [NEW]**: Does the sensor vendor provide an official, production-ready C/C++ driver or embedded SDK (e.g., for Zephyr RTOS, FreeRTOS, or ARM CMSIS-Driver architectures)?
* **Q6.2 [NEW]**: Does an off-the-shelf Evaluation Kit (EVK) or standard breakout board exist (e.g., SparkFun, Adafruit, or MikroElektronika Click Board) for immediate proof-of-concept breadboard testing before custom PCB fabrication?
* **Q6.3 [NEW]**: How complex is the sensor's register initialization map? (Does it require writing 80 undocumented magic register hex values, or does it feature a clean, self-contained configuration API with reliable interrupt behavior)?

