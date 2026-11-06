# Independent Review & Gap Analysis (2026-11-04)
Scope: all top-level docs, Product_Design/, Ideathon_Poster_and_Pitch/, decisions log, hub, and spot-checks of the Research_Dossier. Event: MakeInSilicon 2026, Track 1 (Smart Healthcare), 13-15 Nov 2026.

## 1. What the project is
A two-node wearable (lower-sternum "Sentry Pod": dry 316L ECG + SCG via LSM6DSOX + MEMS mic; wrist "PulseBand": PPG + palmar GSR) with an nRF5340, hybrid NLMS+DWT denoising, a pre-trained CNN-LSTM plus on-device autoencoder, a 30 s cancel window, phone-based dispatch, and a syncope-gated siren / CPR coach. Beachhead: 30-day post-PCI discharge, then the 40-90 day pre-ICD gap. 11 decisions are locked; the 12-phase dossier is complete (about 4.2 MB of markdown).

## 2. Strengths
- Strong, specific clinical hook. Marijon et al. (Ann Intern Med 2016): 51% of SCA victims had warning symptoms; in 80% of those, symptoms began more than 1 h before arrest. Only 19% called EMS. India OHCA survival is reported at about 2-10%.
- Sensing idea is real science: wearable SCG gives PEP (Inan lab, Georgia Tech); SCG changes during ischemia are documented (exercise-test studies).
- Good realism habits: COTS parts, power budget, FMEA, regulatory and reimbursement thinking, a tiered false-alarm design.
- The abstract is honestly labelled "conceptual / validation planned".

## 3. Biggest risks (ranked)
1. **Training-data gap (central claim).** Decision 6 says the model is pre-trained on >40,000 patients to learn PEP lengthening and aortic recoil collapse. Your own Q4.1 notes that PTB-XL (21,801 ECGs / 18,869 subjects) has no SCG/PPG and MIMIC-IV waveforms have no SCG. CEBS is 20 healthy volunteers; SCG-RHC is 73 heart-failure patients under catheterisation. No public dataset has SCG + ECG + PPG + GSR leading up to an ischemic event. Pitch it as "ECG/PPG foundation + small SCG datasets + planned prospective data", not "learned from 40,000 patients".
2. **The 1-6 h countdown is a hypothesis, not a "LOCKED" fact.** Symptoms preceding SCA are supported; a specific, rest-detectable, wearable-measurable sequence (SCG AO drop >50%, Z0 drop 15-35%, etc.) is not shown in the prospective literature. SCG-ischemia evidence is mostly exercise-stress testing. Downgrade to "hypothesis supported by X, to be tested".
3. **Competitor landscape is missing from the repo.** Searching the files finds Cardiosense/HeartBeam only in Asmita's draft. Cardiosense's CardioTag (FDA 510(k) 2025) is a single chest patch measuring ECG + PPG + SCG, aimed at heart-failure filling pressure, and it is not a heart-attack alarm. HeartBeam (FDA-cleared Dec 2025 for arrhythmia) is running a heart-attack detection pilot. Expect a judge to ask. Your differentiation: pre-arrest alerting, glue-free wear, wrist GSR and an escalation workflow, not "nobody has SCG".
4. **Internal contradictions a judge can find in minutes**
   - Wrist battery: 240 mAh x 0.85 / 2.52 mA = about 81 h (3.4 days); pod: 150 x 0.85 / 1.23 = about 104 h (4.3 days). Decision 9 and the poster claim a "synchronized 7-day / full week" recharge, and Decision 3 says 7-14 days.
   - Cost subtotals: pod lines sum to $16.60 (stated $16.20); band lines sum to $14.00 (stated $13.70). The $33.50 total is right only because the errors offset. The BOM excludes tooling, certification, software/cloud and reprocessing.
   - Pod coupling: your "fixed" science says a loosely hanging pendant is unusable (500-1500 mg pendulum noise, lifts off the skin), yet the locked design uses a neck cord at 0.8 N preload. Dry-electrode ECG on a cord-held pod during motion is the weakest link; show data or add a sternal-strap/adhesive fallback as the default.
   - Syncope gate relies on wrist PPG amplitude loss, but the pitch argues wrist PPG collapses >95% in ischemic distress. That can false-trigger the siren on a conscious, standing patient. Gate on the chest SCG/ECG and IMU instead.
   - Hub Module 2 still says "No ECG, zero electrodes"; Decision 1 adds dry ECG. The poster says "TCN-Mamba", the log says "CNN-LSTM". Poster has B2C subscription pricing; log says hospital beachhead.
   - Health economics: Q12.1 reports three different outcomes (+6.45 QALY / $437,400 saved; ">$120,000" saved; and -$200,400 / +3.13 QALY = ICER -$64,025). Dominant ICERs of this size rest on assumed sensitivity and prevented-arrest rates. Treat as illustrative and state the assumptions.
5. **"Replace the LifeVest" overreaches.** LifeVest delivers shocks; yours alerts. The VEST RCT (n=2,302) missed its primary endpoint (arrhythmic death 1.6% vs 2.4%, P=0.18) with median wear about 18 h/day. Better framing: complement or bridge for patients who refuse the vest, plus a cheap remote-monitoring layer. Also: a sensing-only device does not terminate VF; your life-saving path is early alert, bystander CPR and AED access.
6. **Regulatory shortcut.** The Q9.2 plan assumes 510(k) on Zio-type predicates. A device claiming to predict or alert pre-arrest ischemia probably needs De Novo or a clinical study. Shared-reuse across 6 patients needs a validated reprocessing claim for skin-contact electrodes. HRRP applies to US hospitals and AMI (not PCI as such); say so carefully, and give an India-specific payer story (CGHS/Ayushman Bharat, hospital-bundled, private insurers).
7. **Event fit.** The symposium is about indigenous semiconductor infrastructure. A design built wholly from Nordic/ST/ADI/TI parts invites "where is the silicon?" Prepare an answer: custom low-power SoC/AFE integration (your own Tier-2 "bare silicon" BOM), RISC-V option, India-based fab/OSAT roadmap.

## 4. Verification evidence the project can still produce before 13 Nov
- Re-run the denoising claim honestly on CEBS or SCG-RHC with added walking-noise (simulated) and report the real SNR gain, not 28 dB by assertion.
- A bench demo of one thing end-to-end: IMU + ECG on a volunteer at rest, PEP trend, 30 s countdown UI, phone SMS. Even a 2-minute video beats 12 phases of text.
- A one-page "What is proven / simulated / assumed" table for judges.
- Q&A sheet for the 7 risks above.

## 5. Suggested positioning (honest and still strong)
"Early-warning, not diagnosis: a glue-free two-node wearable that fuses mechanical (SCG), electrical and autonomic (GSR/PPG) signals to flag possible acute ischemia in high-risk post-PCI patients, with a human-in-the-loop 30 s cancel step and an escalation path that includes bystander CPR. Validation is staged: public-data simulation, bench, then a supervised pilot."

## 6. Sources checked
- Marijon et al., Ann Intern Med 2016 (warning symptoms before SCA; Oregon SUDS).
- VEST trial (Olgin, ACC 2018; Nat Rev Cardiol summary).
- Inan lab: PMC5444999, PMC6874489, PMC5659316 (wearable SCG / PEP); Korzeniowska-Kubacka (SCG and ischemia).
- PhysioNet CEBS and SCG-RHC database pages.
- Cardiosense CardioTag and HeartBeam FDA announcements (2025-2026).
- India SCA estimates: Indian Heart Journal 2023 review; Lancet Commission commentary (5-6 lakh deaths/yr; survival <10%).

---

## Addendum (after reading the newest files: Master Conversation Archive, MakeInSilicon Master Poster/Dual Blueprint, Official Poster Content, circuit booklet PDF)
The newest files add the TCN-Mamba model, 8 "verification proofs", a closed-loop CPR depth coach, a 47 mF supercap SOS, and a B2B + B2C commercial split. They are more complete than the decisions log, and they also conflict with it. Items below add to sections 3 and 4 above.

**A. Proofs that do not hold up (fix before printing the poster)**
1. Proof 8 (supercap): 0.5 x 0.047 F x (3.3^2 - 1.8^2) V^2 = 0.180 J (about 180 mJ), not 1,527.5 uJ. The "10.18x margin" is therefore wrong, and the 150 uJ load for "3 BLE bursts + 2 s of piezo" is too low (2 s of piezo drive alone is typically tens of mJ). Re-derive both; the real margin may still be fine.
2. Proof 5: "r = 0.94 between sternal dry-electrode Lead-II and 12-lead on PTB-XL". PTB-XL holds standard 12-lead recordings only, so no sternal dry-electrode data exists in it. Either remove the claim, or label it a lead-vector simulation, or measure it on volunteers.
3. Proof 6: "106 dB CMRR with right-leg drive" with dry electrodes. The ADS1292R chip-level figure is about 105 dB; with dry-electrode impedance mismatch the system-level number is far lower. Present as a chip spec, not a measured result.
4. Proof 4 uses 1.55 mW dissipation while the pod's own average draw (1.23 mA at 3.7 V) is about 4.5 mW. Arithmetic is right (+0.022 C); the input is inconsistent.
5. Proof 3: 8.53 kPa suction under a skin-contact rim is the "shower vacuum" claim; it needs a source and a skin-comfort check, since sustained suction on skin marks and irritates.
6. Proofs 2, 7 and 1 check out arithmetically (zeta = 0.707, 3.58 N / 0.32 N = 11.2x, 1.43x). Proof 2 is a model with assumed stiffness/damping, not a measurement.

**B. More internal contradictions**
- Model: TCN-Mamba (archive, poster, booklet) vs CNN-LSTM (decisions log, abstract). RAM: 48 KB (archive) vs <42 KB (log). Pick one and make all documents agree.
- SCG sampling: 104 Hz (booklet) vs 416 Hz (archive) vs 500 Hz (dossier). At 104 Hz one sample is 9.6 ms, so the "<1.8 ms AO timing error" claim is impossible without interpolation; at 416 Hz one sample is 2.4 ms. ECG: 250 Hz (archive) vs 500 Hz (booklet).
- Prototype BOM: Rs 4,718 (archive; line items sum correctly) vs Rs 4,595 (decisions log). NLMS is "28 us" on its own in the archive, but 14 us NLMS + 14 us DWT in the log.
- Cancel UX: "2-second hold" (log) vs "2-sec tap / palm cover" (state machine). Siren gate: accelerometer only (state machine) vs accelerometer + wrist PPG (log); the accelerometer-only version is the safer one, adopt it.
- CDSCO class: Class B (roadmap) vs Class C (Q9.2).
- "Current milestone: hardware phantom and treadmill testing" suggests bench work has started, but there is no data, photo or code in the folder. If a prototype exists, add a photo and one real trace; if not, say "planned".

**C. Business numbers to correct**
- "Average hospital HRRP penalty $2.33 M" is about 10x too high. CMS data: the average penalty among penalized hospitals is 0.44% of Medicare payments (FY2027), with the program saving roughly $520 M across about 2,300-2,500 hospitals, i.e. on the order of $200 k per hospital. HRRP scores heart attack (not PCI as such), heart failure, COPD, pneumonia, CABG and hip/knee replacement, and applies to US Medicare only. Rebuild the "10.9x ROI" from these figures or drop it.
- "98.6% cheaper than Zio ($399)" compares your COGS ($5.58 per patient use) with Zio's price, which includes analysis and reporting. Compare price to price, or call it a hardware-cost comparison.
- The B2C plan (Rs 4,999 + Rs 299/month for diabetic parents) is a medical alarm sold directly to consumers: it still needs CDSCO licensing and an answer to who is liable when it misses or falsely triggers. Consider presenting B2B as the main path and B2C as a later phase.

**D. Good news in the newest files**
- Closed-loop CPR depth coaching via double-integrated sternal acceleration has precedent in accelerometer CPR-feedback devices, but needs drift correction and range checks (LSM6DSOX max 16 g). It is a distinctive feature if you can show a simple bench demo.
- Individual 24 h baseline + Mahalanobis threshold is a sensible design; add the weakness judges will raise: a 24 h window cannot capture sleep/activity variation, and a patient already ischemic during the baseline period would be learned as "normal". Mention a longer rolling baseline and clinician-set limits.
- The booklet's physical layer stack, pin-to-pin table and BOM are exactly what a "Smart Healthcare + Embedded" track should show. Keep them, but align the numbers across files first.

**E. Added sources**
- CMS HRRP FY2026/FY2027 penalty data (Becker's Hospital Review, KFF).
