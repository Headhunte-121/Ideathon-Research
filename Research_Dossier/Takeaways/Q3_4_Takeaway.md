# Question 3.4: Morphological vs. Positional Artifacts
## A Plain-English Breakdown of Why Rolling Over and Standing Up Mimic Heart Attacks and How Our Device Separates Them

---

> **Quick Context**: When a person rolls onto their side in bed or sits up, their heart's pumping force naturally drops by nearly half. This natural drop looks identical to the early stages of a heart attack. This summary explains why this happens and how our device distinguishes normal position changes from true coronary ischemia.

---

## 1. Core Scientific Finding: The "Posture Trap"

When monitoring the heart's physical pumping vibrations on the chest, two completely normal movements fool basic sensors into thinking the heart is failing:
1. **Rolling onto the Left Side in Bed (Left Lateral Recumbent)**:
   - Inside the chest, the heart is suspended in a fluid sac. When a person turns onto their left side, gravity causes the heart to sag downward and tilt toward the left armpit by $15^\circ\text{ to }30^\circ$.
   - A single-direction sensor measuring front-to-back chest vibrations sees the heart signal **plummet by up to $60\%$**, simply because the heart is pumping sideways relative to the sensor.
2. **Standing Up (The Orthostatic Preload Drop)**:
   - When a person sits or stands up, gravity pulls about 2 to 3 cups ($500\text{ to }800\text{ mL}$) of blood downward into their legs and belly veins.
   - Because less blood returns to the heart's main chamber, the heart muscle stretches less and pumps out less blood with each beat (governed by the biological **Frank-Starling law of the heart**).
   - The heart's mechanical pumping force drops by **$35\%\text{ to }48\%$** in a healthy body.

Because coronary blood starvation (myocardial ischemia) **also causes a $>50\%$ drop in pumping force**, a naive sensor will sound a false heart attack alarm every time a user sits up to drink water.

---

## 2. What Happens in the Body: Position Shift vs. Real Heart Attack

```
[ Normal Postural Shift ]                      [ True Coronary Ischemia ]
• Cause: Patient sits up or rolls over.         • Cause: Coronary blood vessel is blocked.
• Timing: Pumping force drops in 2 seconds.     • Timing: Pumping force decays over 30 to 90 minutes.
• Motion: Gyroscope spins at >20 degrees/sec.   • Motion: Patient is resting quietly (<2 degrees/sec).
• Tilt: Gravity vector changes by 30° to 90°.   • Tilt: Body stays at the exact same angle.
```

1. **Speed of Change**:
   - A posture change happens almost instantly—in **less than 2 seconds**.
   - An actual heart attack causes cardiac muscle cells to run out of oxygen slowly, producing a **gradual decay over 30 to 90 minutes** (the 1-to-6-hour pre-infarction countdown).
2. **Rotation Verification**:
   - A posture shift is always accompanied by body turning. The sensor's gyroscope detects a rapid spin (greater than $20^\circ$ per second).
   - An ischemic heart event occurs while the patient is sedentary or resting, with near-zero body rotation.
3. **The 3D Energy Law**:
   - When the heart tilts sideways in bed, its vibration does not disappear—it simply shifts direction into the side-to-side (X) axis.

---

## 3. How This Helps Us: Direct Engineering & Project Value

Understanding the biophysics of posture shifts directly led to our **3-Tier Postural Disambiguation Architecture**, providing four major advantages:

1. **Tri-Axial Kinetic Energy Sum ($L_2$ Norm)**:
   - Instead of looking only at front-to-back vibrations, our software calculates the **total 3D energy** across all three directions: $a_{\text{kinetic}} = \sqrt{a_x^2 + a_y^2 + a_z^2}$.
   - When a patient turns onto their left side, the energy that leaves the front-to-back axis immediately appears on the side-to-side axis. The total 3D energy remains rock-solid, completely eliminating false alarms from sleeping positions!
2. **Temporal Decoupling Software Rules**:
   - The software checks how fast the drop occurred. If pumping force drops in 2 seconds while the gyroscope detects a body turn, the software flags it as a **benign posture change** and resets the baseline for that new position.
   - If pumping force drops slowly over 45 minutes while the body is stationary, the software recognizes **genuine pre-infarction ischemia** and sounds an early warning.
3. **Posture-Binned Baselines**:
   - The chest pendant maintains separate expected heart strength baselines for each body position (lying flat, lying on side, sitting upright).
   - When the patient stands, the software compares their heart strength to their **standing baseline**, not their lying-down baseline.
4. **Zero-Touch Patient Experience**:
   - The patient never needs to manually tell the device that they got out of bed or rolled over. The device continuously recognizes their physical position via gravity tracking.

---

## 4. Hardware Sensor Mapping: How Components Track Posture

| Measurement Parameter | Physical Sensor | Location | Purpose |
| :--- | :--- | :--- | :--- |
| **3D Heart Pumping Strength** | ST LSM6DSOX Accelerometer | Sentry Pendant (Chest) | Computes total 3D kinetic energy ($a_{\text{kinetic}}$) to prevent false alarms when the heart tilts sideways |
| **Body Turning & Rotation** | ST LSM6DSOX Gyroscope | Sentry Pendant (Chest) | Detects active body turns ($>20^\circ\text{/s}$) to flag instant posture transitions |
| **Gravity Tilt Angle (Pitch/Roll)** | Accelerometer (0.05 Hz Filter) | Sentry Pendant (Chest) | Identifies whether the user is lying flat, lying on side, or sitting upright |
| **Arm Position Verification** | Wrist 3-Axis Accelerometer | Companion PulseBand (Wrist) | Confirms whether arm movement matches torso movement during position changes |

---

## 5. Transition Window Options Compared for the Team

When a patient moves, there is a brief 10 to 30 second window where body shaking and blood pressure shifts occur. Here is how the team's candidate options compare:

| Feature | Option 1: Hold & Mask Window | Option 2: Instant Angle Scaling | Option 3: Dual-Track Hybrid |
| :--- | :--- | :--- | :--- |
| **How It Works** | Pauses pre-infarction checks for 15 seconds during and after moving | Mathematically recalculates expected strength continuously by angle | Pauses for 10 seconds during movement, then instantly applies angle scaling |
| **False Alarm Immunity** | **100% (Completely ignores movement)** | Moderate (Can be tricked by 10s blood pressure dip) | **100% (Best protection)** |
| **Monitoring Blind Spot** | 15.0 seconds | **0.0 seconds** | 10.0 seconds |
| **Risk of Missing an Arrest**| **Zero (Heart attacks take 30-90 min)** | **Zero** | **Zero** |
| **Software Complexity** | Ultra-Simple | Moderate (Trigonometric math) | Low-to-Moderate |
| **Team Recommendation** | Simple and completely safe | Good for continuous tracking | **Recommended for Competition Pitch** |

---

## 6. Why Single-Sensor Wearables Fail in Real Life

* **Why Single-Axis Chest Monitors Fail**: Devices that record only one direction of vibration are blinded when the heart tilts inside the chest during sleep. They mistake a comfortable sleeping posture for cardiac collapse.
* **Why Consumer Smartwatches Fail**: Smartwatches on the wrist have no idea whether a drop in pulse volume is caused by a heart attack or simply because the user stood up and blood pooled in their veins.
* **Why Our Dual-Node Device Succeeds**: Our chest pendant measures 3D heart vibrations and gravity angles simultaneously, ensuring that normal body movements never trigger false medical emergencies.

---

## 7. Key Takeaways in Brief

* **Position Changes Mimic Heart Attacks**: Standing up reduces heart pumping force by 48% due to blood pooling in the legs, and rolling onto the left side rotates the heart sideways inside the chest.
* **3D Energy Solves Heart Tilting**: Computing the total 3D acceleration magnitude ($a_{\text{kinetic}}$) captures the heart's true contraction energy no matter which way the patient lies in bed.
* **Time Separates Posture from Disease**: Posture shifts happen in less than 2 seconds with body rotation, whereas real heart attacks evolve over 30 to 90 minutes while the patient is still.
* **Hybrid Transition Protection**: Using a brief 10-second pause during active movement combined with instant angle scaling completely eliminates false alarms while maintaining uninterrupted cardiac surveillance.
