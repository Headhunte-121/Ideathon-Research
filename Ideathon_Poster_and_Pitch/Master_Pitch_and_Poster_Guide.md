# Master Pitch & Poster Guide: Presentation Strategy & Judge Defense
## Team Ownership, Script Blueprints & Knockout Q&A Defense for Ideathon Judges

---

> **Purpose**: This guide provides the competitive delivery strategy, domain ownership assignments, 3-minute pitch script options, and the knockout judge defense cheat sheet for the College Medical IoT Ideathon.  
> **Team Protocol**: Like the rest of the repository, script blocks and domain roles are structured as customizable blueprints so each team member can own their presentation section.  
> **Repository Path**: `c:/College/Ideathon/Ideathon_Poster_and_Pitch/Master_Pitch_and_Poster_Guide.md`

---

## 👥 SECTION 1: Team Domain Ownership & Defense Matrix

Ideathon judges evaluate team chemistry, technical depth, and cross-disciplinary mastery. When a question is asked, the designated domain lead should answer directly with crisp authority rather than looking around:

| Domain | Assigned Lead | Core Responsibilities in Presentation | Key Files to Master Before Pitch |
| :--- | :--- | :--- | :--- |
| **Domain 1: Clinical Cardiology & Pathophysiology** | `[ Team Member 1 ]` | Opens the pitch with the 60-second clinical hook; explains the 1-to-6-hour pre-infarction ischemic cascade; explains why smartwatches fail (peripheral vasoconstriction); defends diabetic silent ischemia and clinical confounder decoupling. | [Q1.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_1_Takeaway.md)<br>[Q1.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_2_Takeaway.md)<br>[Q1.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_3_Takeaway.md)<br>[Q1.4 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_4_Takeaway.md)<br>[Phase 1 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/) |
| **Domain 2: Sensor Hardware, Biophysics & Dual-Node BAN** | `[ Team Member 2 ]` | Explains the physical Dual-Node architecture (Sentry Pendant + PulseBand); sternal bone acoustic window; solid-state SCG ($F = m \cdot a$); zero-glue biological justification (avoiding MARSI & Day-5 hydrogel desiccation); COTS sensor chips (LSM6DSOX, MAX86141, Knowles mic); continuous PTT cuffless blood pressure. | [Q2.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_1_Takeaway.md)<br>[Q2.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_2_Takeaway.md)<br>[Q2.4 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_4_Takeaway.md)<br>[Q2.5 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_5_Takeaway.md)<br>[Dual-Node Blueprint](file:///c:/College/Ideathon/Product_Design/Dual_Node_Pendant_and_Wristband_Architecture.md) |
| **Domain 3: Firmware, DSP, Edge AI & Systems Reliability** | `[ Team Member 3 ]` | Explains Dual-Node NLMS motion cancellation; 3-Stage Transfer Learning; int8 TinyML on Nordic nRF5340 (<42 ms latency, 1.64 mA); hardware FIFO DMA sleep; IEC 62304 Class C TrustZone isolation; Windowed Watchdogs; Murata supercapacitor emergency dying-gasp SOS. | [Q3.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q3_2_Takeaway.md)<br>[Q6.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q6_1_Takeaway.md)<br>[Q11.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q11_1_Takeaway.md)<br>[Q11.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q11_2_Takeaway.md)<br>[Q11.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q11_3_Takeaway.md) |
| **Domain 4: Health Economics, Market Strategy & Reimbursement** | `[ Team Member 4 ]` | Closes the pitch with Dominant ICER ($-\$64,025/\text{QALY}$); $\$437,400$ 5-year savings/patient; HRRP $10.9\times$ hospital ROI; 3 Beachhead Cohorts (Post-PCI, ICD Waiting Gap, Diabetics); Kit COGS $\$33.50$ / $\$5.58$ per patient; Medicare RPM codes yielding $\$49.28/\text{month}$ clinic profit; FDA Class II 510(k) SaMD pathway. | [Q12.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q12_1_Takeaway.md)<br>[Q12.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q12_2_Takeaway.md)<br>[Q12.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q12_3_Takeaway.md)<br>[Q9.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q9_2_Takeaway.md)<br>[Phase 12 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_12_Health_Economics_Market_Pitch/) |

---

## 🎙️ SECTION 2: 3-Minute Competition Pitch Script Blueprints

### Blueprint A: The "Countdown to Collapse" Narrative (Recommended Master Script)

#### Part 1: The Hook & The Problem (0:00 – 0:45) — *Presented by Clinical Lead*
> *"Judges, imagine waking up tomorrow morning feeling slightly tired, with a dull ache in your shoulder that you dismiss as sleeping awkwardly. Four hours later, while sitting at your desk, your heart electrically collapses into ventricular fibrillation. You hit the floor. In 4 minutes, your brain begins irreversible cell death. That is Sudden Cardiac Arrest. It kills over 350,000 Americans and 700,000 people in India every single year—with an out-of-hospital survival rate under 10%.
> 
> Here is the clinical tragedy: cardiac arrest is almost never an unannounced accident. In 70% to 80% of adult cases, it is caused by acute myocardial ischemia—a coronary artery starvation event. And for an ordered 1 to 6 hours before that fatal collapse, the heart screams for help. Cellular ATP depletes within seconds, the myocardium stiffens, mechanical contractility collapses by over 50%, and blood backs up into the lungs.
> 
> Yet current healthcare has a catastrophic blind spot. Hospitals are reactive facilities where patients arrive 2 to 4 hours post-infarction—after irreversible necrosis has already occurred. Smartwatches claim to protect us, but the laws of biophysics prevent them: during ischemic distress, sympathetic vasoconstriction shunts blood away from the wrist, dropping peripheral optical pulse amplitude by over 95%, while mechanical heart vibrations physically cannot travel down arm bones. A watch only alarms after you are already unconscious on the floor."*

#### Part 2: The Solution & Biophysical Innovation (0:45 – 1:45) — *Presented by Hardware & Firmware Leads*
> *"To solve this, we engineered **The Autonomous Sternal Sentry**—a zero-adhesive, dual-node Body Area Network.
> 
> Instead of wet, sticky ECG hydrogel pads that dry out in 5 days and cause painful skin tears in 20% of elderly patients, our **Sentry Pendant** rests gently against the lower sternal bone via an ergonomic tension cord or undershirt pocket. Using an ST LSM6DSOX 6-axis IMU and a Knowles digital MEMS acoustic microphone, it continuously measures mechanical Seismocardiography—directly capturing the micro-g recoil force of the aortic valve opening and left ventricular ejection time.
> 
> Synchronized via BLE 5.3 with our wrist-worn **Companion PulseBand**, the system calculates sub-millisecond Pulse Transit Time—yielding continuous, cuffless blood pressure. To eliminate motion noise during walking, the wrist IMU acts as an adaptive reference, running an on-device Normalized Least Mean Squares filter that cancels footstep shockwaves and boosts sternal signal clarity by 26 decibels.
> 
> On the Nordic nRF5340 dual-core processor, an int8 TinyML neural network executes in under 42 milliseconds, drawing just 1.6 milliamps. If a panic attack occurs, the device detects dry lungs and normal contractility, suppressing the alarm. But when true pre-infarction contractility decay strikes, it activates a 3-zone clinical alert and dispatches emergency telemetry up to 2 hours before electrical collapse."*

#### Part 3: Market Beachhead, Health Economics & Sustainable Model (1:45 – 3:00) — *Presented by Business Lead*
> *"We do not fall into the consumer retail trap where low disease prevalence causes false-alarm collapse. Our beachhead targets 3 ultra-high-risk clinical cohorts: 1.8 million annual post-stent PCI discharges facing a 30-day thrombosis peak, patients in the guideline-mandated 40-to-90-day ICD waiting gap who have high sudden death risk but zero protection, and diabetic patients with silent ischemia.
> 
> The health economics are overwhelming. Formal Markov state modeling demonstrates that our device achieves a **Dominant ICER of -$64,025 per QALY saved**, generating net 5-year healthcare savings of **$437,400 per patient** by converting catastrophic ICU cardiac arrests into uncomplicated early catheterization. For a 400-bed cardiology center, shielding against Medicare HRRP 30-day readmission penalties delivers a **$2.33 million net value—a 10.9x ROI**.
> 
> Our unit economics are fully sustainable: our complete dual-node kit BOM is just **$33.50**, and because our medical silicone requires zero adhesives, hardware is refurbished across 6 patient cycles, dropping physical equipment cost to just **$5.58 per patient**.
> 
> We monetize through active 2024 US Medicare Remote Patient Monitoring codes—CPT 99453, 99454, and 99457—which reimburse $114.28 per patient per month. We provide the complete turnkey platform for $65, leaving prescribing cardiology practices with **$49.28 per patient per month in pure recurring profit**—generating over $295,000 annually for a 500-patient clinic.
> 
> With an FDA Class II 510(k) SaMD pathway, IEC 62304 memory safety, and an emergency supercapacitor reserve that guarantees SOS dispatch even at 0% battery, the Sternal Sentry transforms cardiac medicine from reactive post-mortem witnessing into proactive, life-saving prevention. Thank you."*

---

## 🥊 SECTION 3: The Knockout Judge Defense Cheat Sheet

Judges will rigorously stress-test your clinical physiology, biophysics, battery life, memory safety, and unit economics. Rehearse these knockout answers:

### Question 1: *"Isn't sudden cardiac arrest unpredictable? Aren't you confusing a heart attack with a cardiac arrest?"*
* **Target Speaker**: Clinical / Pathophysiology Lead
* **Knockout Answer**:
  > *"That is a common clinical misconception, but peer-reviewed cardiology proves otherwise. 70% to 80% of adult sudden cardiac arrests stem directly from acute myocardial ischemia. Ischemia is not a sudden lightning bolt; it is an ordered 1-to-6-hour biological countdown. When a coronary artery occludes, ATP depletion causes diastolic stiffening within minutes, followed by systolic pumping force decay (>50%), and localized acidosis. This localized injury creates microvolt repolarization gradients and T-wave alternans that directly trigger the terminal ventricular fibrillation. We are intercepting the ischemic root cause that triggers 80% of all sudden arrests."*
* **Evidence Reference**: [Phase 1.1 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md).

### Question 2: *"Smartwatches already have ECG and pulse oximetry. Why do we need a new device on the chest?"*
* **Target Speaker**: Hardware & Biophysics Lead
* **Knockout Answer**:
  > *"Because of immutable laws of anatomy and biophysics that no software update can bypass. 
  > First, wrist optical PPG fails during acute ischemic shock: the sympathetic nervous system clamps down peripheral arterioles to preserve core organs, dropping wrist pulse amplitude by over 95%, while sternal microvascular vessels retain 71% perfusion. 
  > Second, mechanical aortic valve recoil (SCG) and lung fluid backpressure (Bio-Z) physically cannot propagate down arm bones to the wrist. 
  > Third, wrist ECG requires touching the watch bezel with the opposite hand for 30 seconds—completely impossible if a patient is asleep, dizzy, or experiencing acute syncope. You must be on the sternum."*
* **Evidence Reference**: [Phase 2.2 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.2_Anatomical_Sweet_Spots/Q2_2_Anatomical_Sweet_Spots.md) & [Dual-Node Blueprint](file:///c:/College/Ideathon/Product_Design/Dual_Node_Pendant_and_Wristband_Architecture.md).

### Question 3: *"Why did you eliminate wet ECG electrodes and adhesives entirely? Won't you lose electrical data?"*
* **Target Speaker**: Hardware & Materials Lead
* **Knockout Answer**:
  > *"Because clinical data reveals that wet hydrogel ECG patches hit the 'Day-5 Desiccation Wall.' As gel water evaporates, skin contact impedance spikes from 10 kΩ to over 500 kΩ, causing CMRR to collapse below 65 dB and producing severe baseline wander. Furthermore, in post-PCI and elderly cardiac patients, medical adhesives produce a 15% to 25% incidence of MARSI skin tears and contact dermatitis, leading to 40% patient dropout.
  > By pivoting to solid-state sternal Seismocardiography via the ST LSM6DSOX accelerometer, we measure Newton's law: Force equals mass times acceleration ($F = m \cdot a$). Solid-state silicon never dries out, never irritates skin, and achieves >94% patient adherence over 30 days without a single drop of glue."*
* **Evidence Reference**: [Phase 2.5 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.5_Skin_Electrode_Interface_Impedance/Q2_5_Skin_Electrode_Interface_Impedance.md) & [Q10.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q10_1_Takeaway.md).

### Question 4: *"Doctors hate false alarms. If your device cries wolf on panic attacks or workouts, cardiologists will abandon it. How do you prevent alarm fatigue?"*
* **Target Speaker**: Firmware / Clinical Lead
* **Knockout Answer**:
  > *"We do not rely on single-biomarker thresholds like heart rate. We implement Multi-Modal Decoupling Rules across synchronized channels. 
  > During a severe panic attack, a patient exhibits tachycardia, hyperventilation, and cold sweats—symptoms identical to an MI on the surface. But our device checks thoracic bio-impedance and blood oxygen: in panic, the lungs are completely dry (impedance is stable), SpO2 is 99% to 100%, and SCG mechanical contractility is hyperdynamic. In true ischemia, contractility decays and backward filling pressures cause pulmonary fluid leakage. 
  > During intense workouts, high wrist IMU cadence proves exercise, and our NLMS filter subtracts motion noise.
  > Furthermore, our wristband includes an Azoteq capacitive touch 30-second cancellation slider so conscious users can dismiss benign alerts before external emergency dispatch."*
* **Evidence Reference**: [Phase 1.4 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.4_Differential_Diagnosis_Confounders/Q1_4_Differential_Diagnosis_Confounders.md) & [Phase 9.1 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_09_Clinical_Safety_Regulatory_Viability/9.1_Alarm_Fatigue_Calibration/Q9_1_Alarm_Fatigue_Calibration.md).

### Question 5: *"Continuous multi-modal sensing, 500 Hz sampling, and AI will drain your battery in hours. How does this achieve multi-week battery life?"*
* **Target Speaker**: Embedded Hardware & Firmware Lead
* **Knockout Answer**:
  > *"We do not stream raw data or continuously run heavy neural networks. We engineered an Event-Driven Hierarchical Sentry pipeline with hardware FIFO batching. 
  > 95% of the day, the Nordic nRF5340 microcontroller rests in deep System ON sleep drawing under 1.5 microamps, while the ST LSM6DSOX sensor's internal Machine Learning Core and FIFO buffer data drawing only 4 microamps.
  > The MCU wakes up only for 2-millisecond DMA burst transfers, slashing active duty cycle by 99%. Our quantized int8 TinyML model executes in just 41.8 milliseconds drawing 1.64 mA. This yields over 30 days of continuous monitoring on a compact, rechargeable 150 mAh pouch cell."*
* **Evidence Reference**: [Phase 2.3 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.3_Sampling_Frequencies_Bit_Resolutions/Q2_3_Quantitative_Digitization_Architecture.md) & [Phase 8.1 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_08_Power_Management_Mechanical_Design/8.1_Duty_Cycling_Biometric_Optimization/Q8_1_Duty_Cycling_Biometric_Optimization.md).

### Question 6: *"What happens if the microcontroller firmware crashes or memory corrupts during an active heart attack?"*
* **Target Speaker**: Systems Reliability & Safety Lead
* **Knockout Answer**:
  > *"We engineered a deterministic safe-state architecture compliant with IEC 62304 Class C medical software standards. 
  > First, we enforce zero-heap dynamic memory allocation (MISRA-C:2012 Rule 21.3); all buffers are statically allocated at compile time, eliminating memory fragmentation and out-of-memory panics. 
  > Second, ARM TrustZone hardware divides the system into Secure and Non-Secure domains, with hardware `MSPLIM` stack limit registers preventing stack-overflow corruption.
  > Third, a dedicated hardware Windowed Watchdog Timer (WDT) runs on an independent, isolated 32.768 kHz internal RC oscillator. If firmware fails to service the watchdog between 4.0 and 8.0 seconds—or tries to pet it too early during an abnormal loop—the WDT fires an immediate hard reset, logs an assembly crash dump to non-volatile ferroelectric RAM, and enters Safe-State Tier 2 in under 12 milliseconds."*
* **Evidence Reference**: [Phase 11.2 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_11_Failure_Modes_Failsafes/11.2_Memory_Corruption_MCU_Lockup/Q11_2_Memory_Corruption_MCU_Lockup.md).

### Question 7: *"What if the patient forgets to charge the device and has a cardiac arrest when the battery hits 0%?"*
* **Target Speaker**: Power Electronics & Safety Lead
* **Knockout Answer**:
  > *"We designed a dedicated Power Supply Hierarchy with an emergency 'Dying Gasp' energy reserve. 
  > As the battery discharges, the PMIC executes progressive graceful degradation: non-essential BLE sync drops at 15%, and logging freezes at 5%. 
  > When the main battery voltage hits the 3.0V cut-off, a P-MOSFET disconnect switch isolates an onboard Murata 47 mF / 5.5V supercapacitor (DMF3Z5R5H474M3DTA0) in under 15 microseconds. This supercapacitor holds 158.2 millijoules of reserve energy—a 10.18x safety margin over our required 15.54 millijoules.
  > Even with a completely dead lithium cell, this emergency reserve powers an autonomous BLE 5.3 Coded PHY Long-Range (+8 dBm) SOS beacon to nearby smartphones and sounds a 75 dB resonant acoustic buzzer, ensuring the patient is never left stranded."*
* **Evidence Reference**: [Phase 11.3 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_11_Failure_Modes_Failsafes/11.3_Reserve_Capacitor_Power_Hierarchy/Q11_3_Reserve_Capacitor_Power_Hierarchy.md).

### Question 8: *"Who actually pays for this device, and how do you prove it isn't an expensive burden on the healthcare system?"*
* **Target Speaker**: Business & Health Economics Lead
* **Knockout Answer**:
  > *"We don't rely on out-of-pocket retail sales; we built our business on established 2024 US Medicare Remote Patient Monitoring (RPM) codes: CPT 99453 for patient onboarding, CPT 99454 for monthly transmission, and CPT 99457 for clinical data review. This reimburses $114.28 per patient every month. We charge cardiology clinics a $65 monthly platform fee, leaving the clinic with $49.28 per patient per month in pure recurring profit—that's over $295,000 annually for a 500-patient practice. Because our battery lasts over 30 days, we maintain a 94% transmission adherence rate, far exceeding Medicare's 16-day billing threshold.
  > From a health economics standpoint, our Markov state-transition model proves a **Dominant ICER of -$64,025 per QALY saved**. Preventing an out-of-hospital cardiac arrest saves $139,430 in acute hospitalization costs and eliminates anoxic encephalopathy brain damage, producing net 5-year savings of $437,400 per patient. Furthermore, shielding hospitals against Medicare HRRP 30-day readmission penalties delivers a $2.33 million net value—a 10.9x ROI for a 400-bed hospital."*
* **Evidence Reference**: [Phase 12.1 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_12_Health_Economics_Market_Pitch/12.1_Health_Economics_Cost_Per_QALY/Q12_1_Cost_Per_QALY_Health_Economics.md) & [Phase 12.3 Deep Vault](file:///c:/College/Ideathon/Research_Dossier/Phase_12_Health_Economics_Market_Pitch/12.3_Unit_Economics_Business_Model/Q12_3_Sustainable_Unit_Economics_Business_Model.md).
