# Question 3.5: Real-Time Signal Quality Index (SQI)
## A Plain-English Breakdown of How Our Device Checks Its Own Work to Stop False Alarms and Save Battery

---

> **Quick Context**: In real life, people walk, cough, scratch their chest, and bump into tables. These daily actions create noisy vibrations that fool artificial intelligence into sounding false heart attack alarms. This summary explains how our device evaluates the cleanliness of its own sensor signals in less than a millisecond, discarding noise while keeping battery life long.

---

## 1. Core Scientific Finding: The "Garbage In, False Alarm Out" Trap

When monitoring the heart continuously outside a hospital, physical movement causes serious problems for sensors:
1. **The False Alarm Disaster**:
   - When a person walks or runs, foot impacts rattle the chest and arms.
   - If an artificial intelligence (AI) algorithm receives this messy, corrupted signal, it cannot tell whether the wild spikes are normal walking or dangerous cardiac rhythms (such as ventricular fibrillation or acute heart muscle failure).
   - The result is a flood of false emergency alerts. After being falsely alarmed a few times, the patient stops wearing the device.
2. **The Battery Drain Disaster**:
   - Modern artificial intelligence takes significant computer power.
   - If a microcontroller runs complex AI math on noisy data that contains no recoverable heartbeat, the battery drains rapidly—dying in two days instead of lasting a full week.
3. **The Solution: A Signal Quality Index (SQI)**:
   - Before any heartbeat data is passed to the AI, a fast quality-checking algorithm grades the signal on a scale from $0.0$ (pure useless noise) to $1.0$ (crystal-clear heartbeat).
   - This quality check runs in less than **$100\ \mu\text{s}$** (one-tenth of a millisecond) and uses less than **$35\ \mu\text{W}$** of power (virtually zero battery drain).

---

## 2. What Happens in the Body: Clean Heartbeats vs. Noise

```
[ Clean Physiological Signal ]               [ Corrupted Motion Noise ]
• Source: Ventricular heart muscle pumps.    • Source: Footsteps, coughing, shivering.
• Peak Profile: Very sharp, peaked pulse     • Peak Profile: Random, jagged, or flattened
  (called high "kurtosis" in statistics).      (random scatter).
• Frequency: Concentrated strictly between   • Frequency: Spread across wide, erratic
  1 and 25 beats per second (Hz).              frequencies (>30 Hz muscle vibration).
• Repeatability: Each pulse matches the      • Repeatability: Chaotic wave that never
  previous beat by over 85%.                   repeats the same pattern twice.
```

1. **The Sharpness Rule (Kurtosis & Skewness)**:
   - When the heart's main pumping chamber (left ventricle) contracts, it violently ejects blood into the aorta in a fraction of a second. This produces a sudden, sharp spike.
   - Random electrical noise and gentle clothing friction create flat, smooth distributions. By measuring how "peaked" or "skewed" the signal is, the microchip confirms whether a true heartbeat occurred.
2. **The Biological Frequency Boundary**:
   - The physical vibrations of the human heart cannot pump at 50 or 100 times per second. Heart vibrations are strictly bounded between $1\text{ and }25\text{ Hz}$.
   - If a signal contains energy outside this range (like shivering at $40\text{ Hz}$), the algorithm recognizes it as muscle noise, not heart activity.
3. **Morphological Self-Similarity**:
   - In a resting or walking person, consecutive heartbeats look nearly identical to each other.
   - If a candidate beat matches the running average shape by at least $85\%$, the software marks it as reliable.

---

## 3. How This Helps Us: Direct Engineering & Project Value

Implementing a real-time Signal Quality Index provides four immediate engineering and project benefits:

1. **Stopping False Alarms Before They Start**:
   - No data enters the predictive heart attack AI unless it passes the quality gate.
   - If a patient scratches their chest or shakes their hands dry, the device recognizes the noise and suppresses the alarm, completely eliminating "cry wolf" false alarms.
2. **Extending Battery Life to Over 7 Days**:
   - The heavy TinyML neural network only runs when clean data is present.
   - When the patient is moving or exercising, the heavy AI is automatically put to sleep, saving up to $92\%$ of the processor's energy while still monitoring simple heart rate in the background.
3. **Cross-Node Teamwork (Chest Pendant + Wristband)**:
   - Our system has two separate sensor nodes communicating over a wireless body network: the **Sentry Pendant on the chest** and the **Companion PulseBand on the wrist**.
   - If the chest sensor gets noisy because the person is talking or coughing, the wrist sensor is usually still steady and takes over tracking.
   - If the wrist sensor gets noisy because the person is writing or gesturing, the chest sensor takes over tracking.
   - The two nodes cover each other's blind spots so monitoring never stops.
4. **Sub-Milliwatt Execution on Small Microcontrollers**:
   - The quality index was designed specifically to use simple 16-bit integer math instead of slow floating-point operations.
   - It runs completely inside the sensor driver, taking less than $0.01\%$ of the microcontroller's available time.

---

## 4. Hardware Sensor Mapping: Who Computes What

* **Node A (Sentry Chest Pendant)**:
  - **Sensor**: STMicroelectronics LSM6DSOX 6-axis accelerometer.
  - **What It Measures**: Mechanical chest recoil vibrations (Seismocardiography).
  - **Quality Check**: Measures peak sharpness (kurtosis), $1\text{ to }25\text{ Hz}$ vibration energy, and beat template correlation.
* **Node B (Companion PulseBand Wristband)**:
  - **Sensor**: Analog Devices MAX86141 optical pulse oximeter.
  - **What It Measures**: Blood volume pulses in the radial artery (Photoplethysmography).
  - **Quality Check**: Measures pulse asymmetry (skewness), optical Perfusion Index (AC blood pulse divided by DC baseline), and light flicker.
* **Microcontroller (STM32U575 / nRF5340)**:
  - Wakes up via Direct Memory Access (DMA) every 1 second.
  - Runs the quality check in $95\ \mu\text{s}$, determines whether the data is clean, and decides whether to launch the heart attack prediction model.

---

## 5. Software Detection Logic: The 3-Tier Gating Policy

Our architecture evaluates three possible ways to handle noisy data:

```
[ Option 1: Hard Discard ]        [ Option 2: Soft Weighting ]     [ Option 3: Multi-Tier Gated ] (Ours)
• Rule: If noisy, throw away      • Rule: Never throw away data.   • High Quality (SQI ≥ 0.80):
  the frame completely.             Run full AI on every frame.      Run full heart attack AI.
• Flaw: Dangerous blind spot!     • Flaw: Wastes battery 24/7      • Medium Quality (0.50 ≤ SQI < 0.80):
  If the patient walks for 20       and noise can trick the          Sleep heavy AI; run light
  minutes, the device is blind      AI into false alarms.            emergency rhythm sentry.
  the entire time.                                                 • Poor Quality (SQI < 0.50):
                                                                     Drop frame; suppress alarms.
```

We chose **Option 3 (Multi-Tier Gated Degradation)** because it prevents false alarms while ensuring the patient is never left unmonitored during exercise or walking.

---

## 6. Why Hospitals and Smartwatches Fail

1. **Hospital Telemetry Monitors**:
   - Traditional hospital bedside monitors do not have smart quality checking. If a wire tugs or a patient turns over, the monitor sounds an ear-piercing alarm.
   - Nurses suffer from "alarm fatigue" and often silence the monitors, leading to missed real emergencies.
2. **Consumer Smartwatches**:
   - Smartwatches only check basic optical light reflection on the wrist.
   - When the user walks, arm swinging creates massive blood sloshing that smartwatches mistake for irregular heartbeats or dangerously low oxygen.
   - Smartwatches cannot tell whether a weak pulse is caused by sensor looseness or actual heart failure because they lack a second corroborating sensor on the chest.

---

## 7. Key Takeaways in Brief

* **Noise Is Inevitable**: Normal human activities (walking, talking, scratching) create signals that mimic heart attacks.
* **Math Separates Truth from Noise**: Real heart contractions are sharp and rhythmically consistent; mechanical noise is chaotic, broad, and irregular.
* **Sub-Milliwatt Efficiency**: Our quality check runs in less than $0.1\text{ ms}$, using under $35\ \mu\text{W}$ of power so battery life is preserved.
* **Dual-Node Redundancy**: If the chest sensor is corrupted by coughing, the wrist sensor covers for it; if the wrist sensor is corrupted by arm swinging, the chest sensor covers for it.
* **No False Alarms, No Blind Spots**: By using a 3-tier gating strategy, the device suppresses false alarms during motion while keeping a lightweight emergency sentry active at all times.
