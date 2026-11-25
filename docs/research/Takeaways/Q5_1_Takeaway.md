# Question 5.1: Multivariate Time-Series Forecasting Architectures
## A Plain-English Breakdown of How We Fit an Advanced Heart Attack Prediction Brain Onto a Tiny Wearable Microchip

---

> **Quick Context**: To predict a heart attack hours before it happens, an artificial intelligence algorithm must understand two very different things at once: the tiny millisecond vibrations of a single heartbeat, and the slow multi-hour weakening of the heart muscle. This summary explains how our device combines two specialized mathematical models to run on a tiny wearable battery without needing an internet connection.

---

## 1. Core Scientific Finding: The "Two Time Scales" Problem

Teaching an artificial intelligence algorithm to monitor the human heart requires handling two extreme speeds simultaneously:
1. **The Fast Millisecond World**:
   - Every single time the heart pumps, its valves open and close in a fraction of a second.
   - When the main heart valve (the aortic valve) opens, it creates a sharp mechanical recoil vibration across the breastbone that lasts only about $20\text{ to }40\text{ milliseconds}$ (one-fiftieth of a second).
   - If the software blurs or averages this vibration, it loses the ability to measure how strongly the heart is contracting.
2. **The Slow Multi-Hour World**:
   - A heart attack is not an instantaneous event; it develops gradually over **1 to 6 hours**.
   - As coronary blood vessels narrow, the heart muscle slowly starves of oxygen, causing the natural variation between heartbeats (Heart Rate Variability) to decline over hundreds of minutes.
3. **The Microchip Challenge**:
   - Popular artificial intelligence models (such as the Transformers used in ChatGPT) require massive supercomputers. If you try to run them on a wearable wristband, their memory needs crash the microchip within seconds.
   - Older models (like traditional recurrent networks) have poor memory: they forget what happened 10 seconds ago, making them blind to a multi-hour countdown.
4. **The Solution: A Specialized 2-Stage Brain**:
   - We combine a fast mathematical filter (a **Temporal Convolutional Network**) for millisecond vibrations with a continuous memory model (a **State Space Model**) that remembers hours of history using only a tiny amount of computer memory.

---

## 2. What Happens in the Body: The Fast and Slow Signs of Oxygen Starvation

```
[ Fast Mechanical Sign: The Heartbeat ]         [ Slow Autonomic Sign: The Multi-Hour Drift ]
• Scale: Split-second (10 to 100 milliseconds). • Scale: Hours (1 to 6 hours).
• Heart Reality: Starved heart muscle cells      • Heart Reality: The autonomic nervous system
  cannot contract with full elasticity; the       tries to compensate by releasing stress hormones;
  physical recoil kick of the heartbeat weakens.  natural beat-to-beat variability collapses.
• What We Measure: Breastbone vibration height. • What We Measure: Multi-hour rhythm trends.
```

1. **The Physical Muscle Kick**:
   - With every beat, healthy heart muscle snaps tight like a strong elastic band, pushing blood forcefully into the aorta.
   - When a coronary artery becomes partially blocked, the oxygen-starved muscle tissue stiffens and cannot pump with full force. The mechanical vibration felt on the breastbone drops significantly.
2. **The Nervous System Exhaustion**:
   - Over hours of oxygen starvation, the body's nervous system tries to save the heart by pumping adrenaline.
   - This stress response causes the natural, healthy variations between heartbeats to flatten out into a rigid, exhausted rhythm.
3. **Connecting the Dots**:
   - To forecast a collapse, the software must connect that early morning drop in pumping strength with the afternoon crash in nervous system variability.

---

## 3. How This Helps Us: Direct Engineering & Project Value

Designing a two-stage hybrid brain provides four major project advantages:
1. **Runs Completely On-Device Without the Cloud**:
   - Many medical AI concepts require sending all sensor data to a remote cloud server over the internet. If the wearer is in a basement, on an airplane, or has no cellular reception, cloud devices stop working.
   - Our hybrid architecture consumes less than **$48\text{ kilobytes}$ of memory**, fitting completely inside the wristband's microchip for 100% offline, continuous protection.
2. **Multi-Day Battery Life**:
   - The artificial intelligence evaluates the wearer's heart in less than **$1\text{ millisecond}$ per second**.
   - Because the processor spends $99.9\%$ of its time asleep, the device consumes under **$35\ \mu\text{W}$ of power**, allowing it to run for over a week on a small rechargeable battery.
3. **No Loss of Heartbeat Detail**:
   - Unlike models that compress or downsample heartbeats into blurry averages, our convolutional stage preserves the exact millisecond shape of the heartbeat.
   - This keeps continuous blood pressure tracking accurate within fractions of a millimeter of mercury.
4. **Continuous Multi-Hour Memory**:
   - The State Space Model (Mamba) uses continuous differential equations to track multi-hour trends without forgetting past events or overflowing memory buffers.

---

## 4. Hardware Sensor Mapping: How the Brain Connects to the Body

* **Node A (Sentry Chest Pendant)**:
   - **Sensors**: ST LSM6DSOX accelerometer.
   - **Data Feed**: Sends $100\text{ Hz}$ continuous chest vibration data to the model's convolutional stage, which measures the physical recoil force of the aortic valve opening.
* **Node B (Companion PulseBand Wristband)**:
   - **Sensors**: Analog Devices MAX86141 optical sensor.
   - **Data Feed**: Measures the blood pulse arrival at the wrist.
   - **Computing Unit**: Hosts the full two-stage artificial intelligence network inside its Nordic nRF5340 dual-core processor.
* **Combined Dual-Node Metric (Pulse Transit Time)**:
   - The time difference between the chest heartbeat and the wrist pulse gives the model continuous blood pressure measurements without an arm cuff.

---

## 5. Software Detection Logic: The 2-Stage Forecasting Pipeline

```
[ Stage 1: Fast Vibration Analysis (TCN) ]
• Examines split-second heartbeats.
• Measures breastbone recoil force (Aortic Opening peak).
• Measures time taken to pump blood out of the heart (LVET).
                     │
                     ▼
[ Stage 2: Long-Term Memory Tracking (Mamba SSM) ]
• Remembers trends across 1 to 6 hours.
• Monitors progressive oxygen starvation and nervous system exhaustion.
• Uses only 64 bytes of memory per channel to maintain continuous history.
                     │
                     ▼
[ Clinical Output: 3 Actionable Zones ]
• State 0: Normal healthy baseline.
• State 1: Early warning (1 to 3 hours prior) -> Gentle wrist vibration to check on wearer.
• State 2: Critical emergency (under 60 min prior) -> Emergency siren and ambulance dispatch.
```

---

## 6. Why Hospitals and Smartwatches Fail

1. **Smartwatches Lack the Right Sensors and Memory**:
   - Consumer smartwatches only look at simple optical heart rates on the wrist. They do not have chest sensors to detect heart muscle stiffening, and their software looks at short time windows rather than modeling the full multi-hour pre-infarction countdown.
2. **Hospital Bedside Monitors Rely on Heavy Power**:
   - In intensive care units, monitoring computers are plugged directly into wall outlets and draw hundreds of watts of power. They cannot be adapted to run on a tiny coin-sized battery.
3. **Our Wearable Breakthrough**:
   - By structuring the software into a mathematically efficient two-stage hybrid, our device achieves hospital-grade predictive accuracy within the ultra-low power limits of a wearable patch.

---

## 7. Key Takeaways in Brief

* **Two Speeds at Once**: Predicting a heart attack requires analyzing split-second heartbeat recoil vibrations alongside multi-hour nervous system fatigue.
* **Cloud-Independent Safety**: The entire predictive AI model fits within $48\text{ KB}$ of memory, allowing it to run completely inside the wearable without needing internet or cell service.
* **Ultra-Low Battery Draw**: The algorithm executes its calculations in less than $1\text{ ms}$, preserving battery life for over a week of continuous wear.
* **Early Warning Window**: By maintaining multi-hour memory, the device identifies oxygen starvation 1 to 6 hours before irreversible tissue death or cardiac arrest occurs.
