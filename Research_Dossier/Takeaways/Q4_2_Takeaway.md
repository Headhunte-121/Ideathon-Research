# Question 4.2: Pre-Event Window Labeling
## A Plain-English Breakdown of How We Teach Artificial Intelligence to Forecast a Heart Attack Hours in Advance Instead of Just Beeping When Someone Falls

---

> **Quick Context**: If you teach a computer to look only at the exact moment someone has a heart attack, the computer will only sound an alarm after the person has already collapsed. This summary explains how data scientists label training data so the artificial intelligence learns to forecast a cardiac event 1 to 6 hours before it happens.

---

## 1. Core Scientific Finding: The "Forecasting vs. Detecting" Divide

Most consumer health devices and fitness watches are **reactive detectors**, not proactive forecasters:
1. **The Flaw of Reactive Detection**:
   - Standard smartwatches look for catastrophic heart rhythms only when they are already occurring (Hour 0).
   - They notify the user only after the heart has already gone into cardiac arrest and the person is unconscious on the ground. At that point, permanent brain damage begins within 4 to 6 minutes.
2. **The Goal of Proactive Forecasting**:
   - A heart attack is not an instantaneous lightning strike. In $70\%\text{ to }80\%$ of cases, it is preceded by a **1-to-6-hour countdown** where coronary blood vessels progressively narrow, starving the heart muscle of oxygen.
3. **The Data Labeling Solution**:
   - To teach artificial intelligence to spot this countdown, data scientists cannot just label the moment of collapse as "bad" and everything else as "good."
   - Instead, the training data is divided into **three chronological stages**, allowing the computer to recognize the subtle early warning signs hours in advance.

---

## 2. What Happens in the Body: The 3-Hour Countdown

```
[ Normal Daily Baseline ]           [ Stage 1: The Warning Phase ]      [ Stage 2: The Critical Phase ]
• Time: More than 3 hours prior.    • Time: 1 to 3 hours prior.         • Time: Last 60 minutes.
• Heart Reality: Blood flows freely • Heart Reality: A coronary blood   • Heart Reality: Blood flow is
  through all coronary vessels;      vessel is partially blocked;        almost completely blocked;
  the heart muscle pumps strongly    heart muscle cells begin to stiffen; starved heart cells trigger
  with normal elasticity.            the pumping force starts dropping.  dangerous electrical misfires.
```

1. **The Normal Baseline State (More than 3 Hours Prior)**:
   - The heart muscle receives plenty of oxygenated blood. The heart contracts cleanly, and the pulse arrives at the wrist at a steady, normal speed.
2. **The Incubation Phase (1 to 3 Hours Prior)**:
   - An unstable cholesterol plaque inside a coronary blood vessel cracks or forms a small clot, restricting blood flow.
   - The starved section of heart muscle cannot relax normally between beats (called diastolic stiffening). The physical recoil vibration of the breastbone measured on the chest begins to weaken.
   - The body's autonomic nervous system tries to compensate, causing natural millisecond beat-to-beat variations (Heart Rate Variability) to drop sharply.
3. **The Critical Phase (Under 60 Minutes Prior)**:
   - Oxygen starvation becomes severe across the full thickness of the heart wall.
   - The starved tissue begins firing off rapid, chaotic electrical signals (ectopic beats and ventricular tachycardia), which can rapidly degenerate into fatal ventricular fibrillation.

---

## 3. How This Helps Us: Direct Engineering & Project Value

Labeling training data into three distinct biological stages provides four major engineering advantages:

1. **Actionable Emergency Triage**:
   - Rather than just giving a vague percentage risk, our system triggers distinct, practical responses:
     - In **Stage 1 (1 to 3 hours prior)**: The wristband gives a gentle vibration, prompting the user to sit down, rest, and confirm how they feel. This alerts them before they faint or drive a car.
     - In **Stage 2 (under 60 minutes prior)**: The device sounds an audible alarm, starts a 30-second cancellation window, and prepares to call emergency services with GPS coordinates.
2. **Giving Emergency Responders a Minute Countdown**:
   - Because our algorithm uses survival analysis math, it outputs an estimated countdown in minutes (e.g., *"Estimated Critical Window: 45 minutes"*).
   - This tells paramedics whether they are dealing with an early warning or an imminent cardiac arrest.
3. **Smooth Math Prevents Training Glitches**:
   - Naive AI systems that abruptly switch labels from $0$ to $1$ at an arbitrary 45-minute mark suffer from mathematical instability during training.
   - Our system uses a smooth mathematical curve and an exclusion buffer, preventing the AI from getting confused at transition boundaries.
4. **Eliminating False Panic**:
   - By creating an early incubation stage that warns the patient quietly without immediately calling an ambulance, the device prevents unnecessary hospital visits while keeping the patient safe.

---

## 4. Hardware Sensor Mapping: How the Devices React

* **Node A (Sentry Chest Pendant)**:
  - **Sensors**: ST LSM6DSOX accelerometer.
  - **Stage 1 Action**: Detects the early drop in Aortic Opening (AO) vibration force as the starved heart muscle stiffens.
  - **Stage 2 Action**: Detects sudden loss of coordinated mechanical pumping if arrhythmias begin.
* **Node B (Companion PulseBand Wristband)**:
  - **Sensors**: MAX86141 optical pulse sensor and haptic motor.
  - **Stage 1 Action**: Delivers a gentle, non-panicking wrist vibration to check on the user.
  - **Stage 2 Action**: Displays an emergency countdown screen and sounds an alarm.
* **Dual-Node PTT Measurement**:
  - The time difference between the chest heartbeat and the wrist pulse (Pulse Transit Time) tracks blood pressure changes continuously as the heart struggles.

---

## 5. Software Detection Logic: The 3 Operational States

```
[ Stage 0: Quiescent ]       ──> [ Stage 1: Incubation ]      ──> [ Stage 2: Critical ]
• Target Label: Y = 0            • Target Label: Y = 1            • Target Label: Y = 2
• Status: Healthy Baseline       • Status: Early Warning          • Status: Emergency Escalation
• Device: Low-power sentry       • Device: Gentle wrist tap       • Device: 911 dispatch triggered
```

By structuring the artificial intelligence around these three concrete biological stages, the device acts as a continuous protective shield.

---

## 6. Why Hospitals and Smartwatches Fail

1. **Smartwatches Wait for the Collapse**:
   - Consumer smartwatches only look for high pulse rates or hard ground impacts. They have no mechanical chest sensors to detect heart muscle stiffening, meaning they only notify someone after the wearer has already passed out.
2. **Hospitals Lack Out-of-Hospital Data**:
   - In-hospital monitors are designed for patients already lying in bed. They do not know how to evaluate an active person whose heart is slowly developing ischemia while walking or gardening.
3. **Our Predictive Advantage**:
   - By mathematically labeling the 1-to-6-hour window prior to collapse, our system gives the patient the most valuable medical asset in cardiology: **time to receive help before tissue death occurs**.

---

## 7. Key Takeaways in Brief

* **Early Warning Requires Early Labels**: An AI cannot predict a heart attack if it is only trained on the final moment of collapse.
* **The 3 Biological Stages**: The heart moves from normal baseline, to early muscle stiffening (1 to 3 hours prior), to critical electrical instability (under 60 minutes prior).
* **Two-Level Response**: The device gives a gentle, private wrist prompt during early warning, and only escalates to emergency 911 dispatch when the danger becomes critical.
* **Countdown in Minutes**: The algorithm provides an estimated time-to-event countdown, giving emergency responders vital situational awareness.
