# Master Pitch & Poster Guide: Presentation Strategy & Judge Defense
## Team Ownership, Script Blueprints & Knockout Q&A Defense for Ideathon Judges

---

> **Purpose**: This guide provides the competitive delivery strategy, domain ownership assignments, 3-minute pitch script options, and the knockout judge defense cheat sheet for the College Medical IoT Ideathon.  
> **Team Protocol**: Like the rest of the repository, script blocks and domain roles are structured as customizable blueprints so each team member can own their presentation section.  
> **Repository Path**: `c:/College/Ideathon/Ideathon_Poster_and_Pitch/Master_Pitch_and_Poster_Guide.md`

---

## 👥 SECTION 1: Team Domain Ownership & Defense Matrix

Ideathon judges evaluate team chemistry and cross-disciplinary mastery. When a question is asked, the designated domain lead should answer directly with authority rather than looking at each other:

| Domain | Assigned Lead | Core Responsibilities in Presentation | Key Files to Master Before Pitch |
| :--- | :--- | :--- | :--- |
| **Domain 1: Clinical Cardiology & Pathophysiology** | `[ Team Member 1 ]` | Opens the pitch with the 60-second clinical hook; explains the 1-to-6-hour cascade; answers questions on ischemia vs arrest, diabetic silent ischemia, and false-alarm physiology. | [Q1.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_1_Takeaway.md)<br>[Q1.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_3_Takeaway.md)<br>[Q1.4 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q1_4_Takeaway.md) |
| **Domain 2: Sensor Hardware, Physics & Placement** | `[ Team Member 2 ]` | Explains the physical device, sternal bone acoustic window, COTS sensor chips, 24-bit ADC, and magnetic snap-to-skin lifestyle dock. | [Q2.1 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_1_Takeaway.md)<br>[Q2.2 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_2_Takeaway.md)<br>[Q2.3 Takeaway](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_3_Takeaway.md)<br>[Form Factor Study](file:///c:/College/Ideathon/Product_Design/Form_Factor_Evaluation_Pendant_vs_Patch.md) |
| **Domain 3: Firmware, DSP & Edge AI** | `[ Team Member 3 ]` | Explains the 3-Tier Hierarchical Sentry pipeline, hardware FIFO MCU deep sleep, motion artifact denoising, and on-chip TinyML execution. | [Q2.3 Product Translation](file:///c:/College/Ideathon/Research_Dossier/Product_Translations/Q2_3_Product_Translation.md)<br>[Master Architecture](file:///c:/College/Ideathon/Product_Design/Master_Fixed_vs_Flexible_Architecture.md) |
| **Domain 4: Business, Health Economics & Regulatory** | `[ Team Member 4 ]` | Closes the pitch with market beachhead (Post-PCI discharge), US Medicare RPM CPT codes, hospital readmission ROI, and FDA 510(k) pathway. | [Master Hub Pillar 7 & 8](file:///c:/College/Ideathon/MASTER_PRODUCT_AND_RESEARCH_HUB.md) |

---

## 🎙️ SECTION 2: 3-Minute Competition Pitch Script Blueprints

### Blueprint A: The "Countdown to Collapse" Narrative (Recommended)

#### Part 1: The Hook (0:00 – 0:45) — *Presented by Clinical Lead*
> *"Judges, imagine waking up tomorrow morning feeling slightly tired, with a dull ache in your shoulder that you dismiss as sleeping wrong. Four hours later, while sitting at your desk, your heart electrically collapses. You hit the floor. In 4 minutes, your brain begins to die. That is Sudden Cardiac Arrest. It kills over 350,000 Americans and 700,000 people in India every single year.
> 
> Here is the clinical tragedy: cardiac arrest is almost never an accident. In 70% to 80% of cases, it is caused by acute myocardial ischemia—a blocked coronary artery starving the heart of oxygen. And for 1 to 6 hours before that fatal collapse, the human body screams for help. Autonomic nerves fail, the heart muscle stiffens and loses over 50% of its mechanical pumping force, and fluid begins leaking backwards into the lungs.
> 
> Right now, healthcare has a fatal blind spot. Hospitals can unblock arteries, but patients arrive 2 to 4 hours post-infarction—after the heart muscle is permanently dead. Smartwatches claim to protect us, but the laws of physics prevent them: blood vessels in the wrist clamp shut during shock, and mechanical heart vibrations cannot travel down arm bones. A watch only alarms after you are already unconscious."*

#### Part 2: The Solution & Biophysics (0:45 – 1:45) — *Presented by Hardware & Firmware Leads*
> *"We built **The Autonomous Sternal Sentry**.
> 
> It is an autonomous biowearable that looks like a sleek lifestyle pendant, but magnetically docks flush against a micro-thin, concealed silicone dock on the breastbone. Positioned directly over the heart's natural acoustic sounding board, it measures 5 synchronized physical signals: electrical ECG, mechanical valve recoil via seismocardiography, optical microvascular perfusion, acoustic gallop sounds, and thoracic lung fluid.
> 
> To achieve medical-grade precision without draining battery life, we engineered a 3-tier event-driven pipeline. 95% of the day, the main processor sleeps while an ultra-low-power front-end monitors baseline ECG and an IMU hardware classifier monitors movement drawing only 4 micro-amps. 
> 
> When resting autonomic HRV collapses, the device wakes up for a 60-second diagnostic burst to verify mechanical contractility decay and pulmonary impedance drop. If a panic attack strikes, it knows your lungs are dry and suppresses the alarm. But when true ischemia strikes, it alerts the patient and transmits emergency telemetry 2 hours before electrical collapse."*

#### Part 3: The Market, Economics & Close (1:45 – 3:00) — *Presented by Business Lead*
> *"We are not targeting healthy gym-goers. Our beachhead is the 1.8 million patients discharged from hospitals each year following stent surgery—where 30% of sudden re-infarctions strike in the first 30 days.
> 
> Our business model utilizes existing, active US Medicare Remote Patient Monitoring CPT codes—specifically CPT 99453, 99454, and 99457. Prescribing cardiologists earn over $100 per patient every month for monitoring post-stent patients, creating a frictionless adoption pathway. Furthermore, under the Hospital Readmissions Reduction Program, hospitals face millions in penalties if patients return within 30 days. By preventing just 5 emergency ICU readmissions per 100 patients, we save a hospital over $250,000.
> 
> With a COTS component bill of materials under $40, an FDA Class II 510(k) pathway, and patent-pending magnetic dock mechanics, the Sternal Sentry transforms cardiac medicine from reactive post-mortem witnessing into proactive, life-saving prevention. Thank you."*

---

## 🥊 SECTION 3: The Knockout Judge Defense Cheat Sheet

Judges will try to find holes in your clinical logic, physics, battery, and economics. Rehearse these knockout answers:

### Question 1: *"Isn't sudden cardiac arrest unpredictable? Aren't you confusing a heart attack with a cardiac arrest?"*
* **Target Speaker**: Clinical / Pathophysiology Lead
* **Knockout Answer**:
  > *"That is a common clinical misconception, but peer-reviewed cardiology proves otherwise. 70% to 80% of adult sudden cardiac arrests stem directly from acute myocardial ischemia. Ischemia is not a sudden lightning bolt; it is an ordered 1-to-6-hour biological countdown. When a coronary artery occludes, ATP depletion causes diastolic stiffening within minutes, followed by systolic pumping force decay (>50%), and localized acidosis. This localized injury creates microvolt repolarization gradients and T-wave alternans that directly trigger the terminal ventricular fibrillation. We are intercepting the ischemic root cause that triggers 80% of all sudden arrests."*
* **Evidence Reference**: [Phase 1.1 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.1_Pre_Infarction_Cascade/Q1_1_Pre_Infarction_Cascade_1_to_6_Hours.md) (Section 1.1 & 1.2).

### Question 2: *"Smartwatches already have ECG and pulse oximetry. Why do we need a new device on the chest?"*
* **Target Speaker**: Hardware & Biophysics Lead
* **Knockout Answer**:
  > *"Because of immutable laws of anatomy and physics that no software update can bypass. 
  > First, wrist optical PPG fails during cardiogenic shock: the sympathetic nervous system clamps down peripheral arterioles to preserve core organs, dropping wrist pulse amplitude by over 95%, while sternal vessels retain 71% perfusion. 
  > Second, mechanical valve recoil (SCG) and lung fluid transudation (Bio-Z) physically cannot propagate down arm bones to the wrist. 
  > Third, wrist ECG requires touching the watch bezel with the opposite hand for 30 seconds—completely impossible if a patient is asleep, dizzy, or experiencing acute syncope. You must be on the sternum."*
* **Evidence Reference**: [Phase 2.2 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.2_Anatomical_Sweet_Spots/Q2_2_Anatomical_Sweet_Spots.md) & [Form Factor Analysis](file:///c:/College/Ideathon/Product_Design/Form_Factor_Evaluation_Pendant_vs_Patch.md).

### Question 3: *"Doctors hate false alarms. If your device cries wolf, cardiologists will delete the app in two days. How do you prevent alarm fatigue?"*
* **Target Speaker**: Firmware / Clinical Lead
* **Knockout Answer**:
  > *"We do not rely on single-biomarker thresholds like heart rate. We implement Multi-Modal Decoupling Rules. 
  > For example, during a severe panic attack, a patient exhibits racing tachycardia, hyperventilation, and cold sweats—symptoms identical to an MI on the surface. But our device checks thoracic bio-impedance and blood oxygen: in panic, the lungs are completely dry (impedance is stable) and SpO2 is 99% to 100%. In a true ischemic event, backward filling pressures cause pulmonary fluid leakage and desaturation. 
  > Furthermore, we include a 30-second patient tactile cancellation interlock so conscious users can easily dismiss harmless alerts before any emergency dispatch occurs."*
* **Evidence Reference**: [Phase 1.4 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_01_Pathophysiology_and_Biomarkers/1.4_Differential_Diagnosis_Confounders/Q1_4_Differential_Diagnosis_Confounders.md).

### Question 4: *"Continuous multi-modal sensing, 500 Hz sampling, and AI will drain your battery in 4 hours. How does this survive a week?"*
* **Target Speaker**: Firmware / Embedded Systems Lead
* **Knockout Answer**:
  > *"We do not stream raw data or run continuous neural networks. We engineered a Hierarchical Sentry pipeline with hardware FIFO batching. 
  > 95% of the day, the nRF5340 microcontroller rests in deep System ON sleep drawing under 1.5 microamps, while the low-power analog front-end reads single-lead ECG and the IMU's hardware machine learning core monitors motion drawing only 4 microamps. 
  > Data is buffered into on-chip FIFOs and transferred via 2 ms DMA bursts, reducing MCU wake time by 99%. Only when resting autonomic HRV collapses does the system fire a 60-second diagnostic burst to verify mechanical contractility. This achieves 7 to 14 days of continuous operation on a small 150 mAh cell."*
* **Evidence Reference**: [Phase 2.3 Deep Research Dossier](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.3_Sampling_Frequencies_Bit_Resolutions/Q2_3_Quantitative_Digitization_Architecture.md) (Section 2.3.4 & FIFO Architecture).

### Question 5: *"Who actually pays for this device, and why would a hospital adopt it?"*
* **Target Speaker**: Business & Health Economics Lead
* **Knockout Answer**:
  > *"We don't rely on out-of-pocket consumer sales; we utilize a proven B2B2C clinical reimbursement model under existing US Medicare Remote Patient Monitoring CPT codes: CPT 99453 for initial onboarding, CPT 99454 for monthly telemetry, and CPT 99457 for clinical review. Prescribing cardiologists bill approximately $107 to $148 per patient every month for monitoring post-PCI patients, creating a substantial recurring revenue stream for cardiology practices.
  > Simultaneously, hospitals adopt our system because under Medicare's Hospital Readmissions Reduction Program, hospitals are heavily penalized for 30-day readmissions. Preventing just 5 emergency readmissions per 100 post-stent patients saves the institution over $250,000 in uncompensated ICU care."*
* **Evidence Reference**: [Master Hub Pillar 7](file:///c:/College/Ideathon/MASTER_PRODUCT_AND_RESEARCH_HUB.md) & [Master Systems Questionnaire Phase 12](file:///c:/College/Ideathon/Master_Research_Questionnaire_Expanded.md).
