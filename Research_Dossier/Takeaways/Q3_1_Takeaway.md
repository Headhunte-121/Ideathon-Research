# Question 3.1: Sources of Signal Degradation in Body-Worn Sensors
## A Plain-English Breakdown of Real-World Noise, Motion Artifacts, and How Our Dual-Node System Cleans Them

---

> **Quick Context**: In real life, people walk, climb stairs, swing their arms, and step into bright sunlight. These everyday movements create physical noise up to 100 times larger than the heart's subtle signals. This summary explains what corrupts wearable heart sensors and how our dual-node setup eliminates that noise.

---

## 1. Core Scientific Finding: The "Same Frequency" Problem

In medicine, filtering noise is easy when the noise happens at a completely different speed or frequency than the heartbeat (for example, very high-pitched electrical hums can be blocked by a simple filter). 

The fundamental problem with ambulatory heart monitoring is that **everyday body movements occur at the exact same rhythm as the human heartbeat**:
1. **Footstep Shocks**: Walking impacts the body at 1 to 2 steps per second (1 to 2 Hz). A normal resting heart also beats at 1 to 2 times per second (60 to 120 beats per minute). The shock of heels hitting the floor travels up the skeleton into the chest with a force **$50\times\text{ to }100\times$ larger** than the heart's tiny mechanical pumping vibrations.
2. **Arm Swing Sloshing**: When arms swing during walking, gravity and momentum force dark, oxygen-poor venous blood to slosh back and forth in the wrist veins. Optical light sensors see this dark blood moving and mistake it for a plunging blood oxygen level ($SpO_2$), triggering false emergency alerts.
3. **Standing Up (Postural Trap)**: When a person stands up, gravity naturally pulls blood down into their legs and abdomen. This temporarily reduces the amount of blood returning to the heart, causing the heart's pumping force to drop by nearly half ($48\%$). A simple sensor will confuse this normal posture change with a sudden heart attack.

Because these movements happen at the same frequency as the heart, traditional single-sensor devices cannot filter them out with standard software filters.

---

## 2. The Step-by-Step Breakdown of Real-World Body Noise

```
[ Locomotion Shocks ]  --->  [ Optical Sunlight & Flicker ]  --->  [ Posture & Respiration ]
Footsteps send 1.5g to 3.0g   Direct sun overloads sensors;        Breathing swells chest tension;
shocks up the skeleton,       indoor lamps flicker at 100 Hz,      standing up drops blood return
swamping the 0.03g heartbeat. creating phantom heart rates.        and cuts pump force by 48%.
```

1. **Footstrike Locomotion Transients**: Each time a foot hits the ground, it sends a mechanical shockwave ($1.5\text{ to }3.0\text{ g}$) through the spine and ribs into the sternal breastbone. The heart's actual pumping vibration (Seismocardiography - SCG) is only $0.01\text{ to }0.05\text{ g}$. Without specialized cancellation, walking makes heart vibrations invisible.
2. **Sunlight and Lightbulb Flicker**: In outdoor daylight, direct sunlight is thousands of times brighter than the sensor's tiny LEDs, blinding the photodiode. Indoors, standard electric lights flicker at 100 or 120 times a second. If an optical sensor is not synchronized to ambient light, this flicker aliases into false high heart rate readings.
3. **Venous Blood Pooling at the Wrist**: Arteries carry bright red oxygenated blood under high pressure, while veins carry dark deoxygenated blood under low pressure. Shaking or swinging the wrist moves the floppy veins, creating optical dips that mimic arterial pulses and corrupt pulse oximetry.
4. **Thoracic Breathing Swell**: Taking a deep breath expands the ribcage by 2 to 4 centimeters. This stretches the chest pendant cord, causing slow baseline wave shifts that must be separated from genuine cardiac cycles.
5. **Postural Gravitational Shift**: When sitting or standing, gravity changes the angle of the sensor and pulls blood downward. This reduces the heart's stroke volume via the Frank-Starling biological law, cutting heart vibration amplitude by $48\%$ without any disease being present.

---

## 3. How This Helps Us: Direct Engineering & Project Value

Understanding exactly how and where noise enters the system led directly to our team's choice of **Route 1+3 (Modern Digital DSP + Dual-Node Adaptive Subtraction)**, giving our product major advantages:

1. **Dual-Node Active Noise Cancellation (Route 3)**:
   - Because our device has two nodes—a pendant on the chest and a band on the wrist—we turn them into a cooperative noise-cancellation pair.
   - The wristband measures arm swings and walking footsteps.
   - An on-device adaptive filter subtracts that walking rhythm from the chest pendant's signal. This strips away footstep shocks and isolates clean heart pumping signals, boosting signal clarity by over **$26\text{ dB}$**.
2. **Compact & Affordable Hardware (Route 1)**:
   - Instead of adding bulky, expensive physical analog filter chips onto our circuit board, we use the high-resolution digital converters and anti-aliasing already built into our modern chips.
   - All bandpass filtering is performed in software by the microcontroller using ARM CMSIS-DSP math routines.
   - This keeps the chest pendant ultra-compact ($38\text{ mm}$), lightweight, and within our ₹820 ($9.84) target bill of materials.
3. **Eliminating Postural False Alarms**:
   - The chest pendant uses its 3-axis accelerometer to continuously track which way gravity points (supine lying down, sitting up, or standing).
   - The software only evaluates cardiac contraction strength against the patient's baseline for that specific posture, preventing normal standing from triggering false infarction alarms.
4. **Built-In Optical Ambient Light Rejection**:
   - The wristband's MAX86141 optical front-end automatically samples background room light immediately before and after every LED flash, subtracting ambient light directly on the silicon die before converting to numbers.

---

## 4. Hardware Sensor Mapping: How Each Node Handles Noise

| Noise Source | Sensor Affected | Where It Is Cleaned | Method of Elimination |
| :--- | :--- | :--- | :--- |
| **Footstep Shockwaves** | Sternal IMU (Pendant) | Cortex-M33 Firmware | **Dual-Node NLMS Filter**: Wrist IMU tracks footsteps and subtracts them from chest signal |
| **Ambient Sunlight & Lamp Flicker** | Optical PPG (Wristband) | On-Chip Front-End | **MAX86141 Ambient Subtraction**: Samples background light before LED flash and cancels it ($>90\text{ dB}$) |
| **Venous Blood Sloshing** | Optical PPG (Wristband) | Cortex-M33 Firmware | **Aortic Timing Gating**: Optical peaks are only counted if confirmed by sternal valve opening timing |
| **Breathing Baseline Drift** | Sternal IMU (Pendant) | Cortex-M33 Firmware | **Digital High-Pass Filter (1.0 Hz)**: Strips out slow chest expansion waves while preserving heart beats |
| **Standing Up / Posture Shifts** | Sternal IMU (Pendant) | Cortex-M33 Firmware | **Gravity Orientation Vector (0.05 Hz)**: Tags posture to normalize expected heart pump strength |
| **High-Frequency RF & Static** | Sternal IMU (Pendant) | On-Chip Hardware | **LSM6DSOX 400 Hz Anti-Aliasing Filter**: Blocks motor static and friction before digitization |

---

## 5. Software Detection Logic: Real-Time Signal Cleanup Flow

```
[ Wrist IMU: Footstep Reference x(n) ] ──┐
                                         ├──> [ NLMS Adaptive Filter ] ──> [ Cleaned SCG Heart Beats ]
[ Chest IMU: Heart + Footstep d(n) ]   ──┘                                       │
                                                                                 ├──> Aortic Opening (AO) Force
[ Chest Gravity Tilt: Posture State ]  ──────────────────────────────────────────> Normalized Against Active Posture
                                                                                 │
[ Wrist Optical: Ambient Subtracted ]  ──────────────────────────────────────────> Clean SpO2 & Radial Pulse Wave
```

1. **Step 1: On-Chip Pre-Cleaning**: Sensor chips strip away out-of-band high frequencies and ambient room light flicker before numbers reach the microcontroller.
2. **Step 2: Posture Classification**: The microcontroller checks the steady pull of gravity to see whether the user is lying in bed, sitting upright, or standing.
3. **Step 3: Adaptive Walking Subtraction**: If the patient is walking, the software compares the wrist movement to the chest vibration, mathematically removing the footsteps.
4. **Step 4: Clean Cardiovascular Feature Extraction**: The cleaned heart signal is analyzed for Aortic Opening (AO) ejection strength and Left Ventricular Ejection Time (LVET) to detect coronary ischemia hours before symptoms begin.

---

## 6. Why Single-Sensor Wearables Fail in Real Life

* **Why Single Chest Patches Fail**: A single chest patch has no secondary reference point. When a patient walks or coughs, the patch cannot distinguish between the chest cage shaking and the heart contracting, forcing it to either freeze or throw false alarms.
* **Why Consumer Smartwatches Fail**: Smartwatches sit on the most active limb of the body. Typing, gesturing, and swinging arms slosh venous blood and rattle the watch case, completely swamping optical blood flow signals during movement. Furthermore, a watch cannot detect the heart's physical pumping strength at all.
* **Why Our Dual-Node Setup Succeeds**: By linking the chest and wrist wirelessly, each sensor cancels the other's blind spots. The wrist watches the body move, while the chest measures the heart pump.

---

## 7. Key Takeaways in Brief

* **Noise Matches the Heartbeat**: Locomotion, arm swings, and venous blood sloshing happen at 1 to 2 Hz, exactly overlapping human heart rates.
* **Dual-Node Cooperative Filtering**: Our wristband acts as a motion reference, allowing software on the chest pendant to subtract footstep shocks and isolate pure heart vibrations.
* **Pure Digital Processing**: By handling filtering in code (Route 1+3) and utilizing on-chip sensor anti-aliasing, we keep our device sleek, tiny, and within our ₹820 budget.
* **Immune to False Posture Alarms**: By tracking gravity tilt, our device accounts for normal stroke volume drops when standing up, preventing false emergency alerts.
