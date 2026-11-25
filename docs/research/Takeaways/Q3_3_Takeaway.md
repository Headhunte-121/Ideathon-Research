# Question 3.3: Digital Signal Processing (DSP) for Motion Noise Removal
## A Plain-English Breakdown of How Software Algorithms Strip Walking Noise and Shivering from Heart Signals

---

> **Quick Context**: When a person walks, each footstep sends a shockwave through their chest that is 50 times larger than the heart's natural pumping vibration. This summary explains the three primary software algorithms used to subtract that walking noise (NLMS, RLS, and Wavelets) and compares their speeds, battery usage, and accuracy.

---

## 1. Core Scientific Finding: The 3 Ways to Clean Walking Noise

When recording heart vibrations on the chest, footstep shocks and heartbeats happen at the exact same rhythm (1 to 2 times per second). Because a simple frequency filter cannot separate them, software must use smart mathematical algorithms.

Engineers use three primary software methods to solve this:
1. **NLMS (Normalized Least Mean Squares)**: 
   - Uses the wristband as an external helper. 
   - The wrist tracks footsteps and feeds them into the algorithm. The algorithm continually adjusts a mathematical filter to subtract the footsteps from the chest signal in real time with zero delay.
   - **Characteristics**: Extremely lightweight, uses almost zero memory, and consumes less than 1% of processor power.
2. **RLS (Recursive Least Squares)**: 
   - A high-speed mathematical cousin of NLMS. 
   - Instead of slowly adjusting to footstep rhythms over a few seconds, RLS adapts almost instantaneously (within 3 to 5 steps).
   - **Characteristics**: Adapts rapidly when a person suddenly breaks into a sprint, but requires $5\times$ more computer processing power and $16\times$ more memory.
3. **Wavelet Denoising (Multi-Scale Wavelet Transform)**: 
   - Does not need a wrist sensor to help it. 
   - It acts like a mathematical magnifying glass, breaking a 1-second recording into multiple detail layers (fast muscle twitches, medium heartbeats, slow breathing waves). It wipes away the noise layers and pieces the clean heartbeat back together.
   - **Characteristics**: Excellent for removing random, unexpected muscle shivering or clothing rustle, but introduces a 1.2-second processing delay while it collects a block of data.
4. **The Hybrid Approach (NLMS + Wavelets)**: 
   - Uses NLMS to cancel regular walking footsteps in real time, and uses a gentle Wavelet pass in the background to clean up random shivering.

---

## 2. How Each Algorithm Works: A Plain-Language Breakdown

```
[ Method 1: NLMS ]              [ Method 2: RLS ]               [ Method 3: Wavelets ]
Wrist IMU tells chest:           Matrix math calculates          Breaks 1 second of data into
"Footstep just hit at 1.8 Hz."   instantaneous footstep changes. frequency slices; erases shivering
Subtracts it sample-by-sample.   Adapts in 40 ms; uses 5x power. layers and rebuilds the heart wave.
```

* **NLMS (The Real-Time Subtraction Method)**:
  - Imagine you are listening to someone talk in a room while a steady metronome is ticking. If a microphone right next to the metronome tells you the exact sound of the tick, you can subtract it from what you hear, leaving only the clean voice.
  - In our device, the wristband is the metronome microphone (it feels arm swings and footsteps), and the chest pendant is the main microphone. NLMS subtracts the footstep ticks 104 times per second with zero delay.
* **RLS (The High-Speed Precision Tracker)**:
  - If a patient suddenly jumps or starts running up a flight of stairs, the metronome rhythm changes violently. 
  - Standard NLMS takes 15 to 30 steps to catch up. RLS uses complex matrix algebra to recalculate the exact footstep rhythm in just 3 to 5 steps.
* **Wavelets (The Layer-by-Layer Cleaner)**:
  - What if the patient shivers from the cold, or their shirt rubs against the pendant? The wristband cannot predict random shivering because shivering happens only on the chest.
  - The Wavelet algorithm slices the chest vibration signal into five distinct speed layers:
    - *Layer 1 (Fast)*: Muscle shivering and clothing rustle $\rightarrow$ erased.
    - *Layer 2 (Medium)*: Aortic valve opening vibrations $\rightarrow$ preserved.
    - *Layer 3 (Slow)*: Deep breathing chest expansion $\rightarrow$ erased.
  - The remaining clean layers are recombined into a pristine heartbeat signal.

---

## 3. How This Helps Us: Direct Engineering & Project Value

Understanding the exact computational trade-offs between these algorithms gives our team the data needed to make sound engineering decisions:

1. **Protecting Battery Life on a Tiny Coin Battery**:
   - The NLMS algorithm runs in just **$14.2\ \mu\text{s}$ per sample** on our ARM Cortex-M33 processor, using less than **$19\ \mu\text{W}$ of power**.
   - This tiny power draw is what enables our chest pendant to run for **5 to 7 days continuously** on a small 150 mAh rechargeable cell without needing a bulky battery.
2. **SRAM Memory Optimization**:
   - Our microcontroller has limited internal memory (SRAM).
   - NLMS requires only **$256\text{ bytes}$** of memory, whereas RLS requires over **$4,000\text{ bytes}$** ($4\text{ KB}$) just to store its mathematical matrix. Using NLMS leaves memory completely free for our pre-infarction forecasting artificial intelligence models.
3. **The Power of the Hybrid Strategy**:
   - Combining real-time NLMS with background Wavelet cleaning gives our device **$>28.5\text{ dB}$ of noise reduction**.
   - This allows our system to clearly measure the heart's **Aortic Opening (AO) ejection force** and **Left Ventricular Ejection Time (LVET)** even while the patient is actively walking around their home or office.
4. **Reliable Ischemia Detection Without False Alarms**:
   - Single-sensor fitness watches either freeze or report crazy heart rate numbers during exercise because they cannot remove motion noise.
   - Our dual-node DSP architecture cleanly separates walking movement from the heart, preventing false emergency calls during daily physical activities.

---

## 4. Hardware Sensor Mapping: How Signals Flow Through Code

| Algorithm Component | Input Sensor | Code Execution Location | Output Result |
| :--- | :--- | :--- | :--- |
| **Primary Corrupted Input $d(n)$** | ST LSM6DSOX Sternal IMU | Sentry Pendant Microcontroller | Raw chest vibrations (Heart + Footsteps + Shivering) |
| **Noise Reference $x(n)$** | Wrist 3-Axis IMU (Companion PulseBand) | Transmitted via BLE 5.3 PAwR | Pure arm swing and footstep movement reference |
| **NLMS Real-Time Filter** | Both IMU streams | ARM Cortex-M33 Core (64 MHz) | Real-time footstep shockwave subtraction ($>22\text{ dB}$) |
| **Background Wavelet Denoising** | Cleaned NLMS stream | ARM CMSIS-DSP Library | Strips random muscle tremors and reconstructs clean AO peaks |
| **Optical Motion Filter** | MAX86141 Optical Sensor | Wristband Microcontroller | Ambient light cancellation + pulse shape verification |

---

## 5. Comparative Trade-Off Scorecard for the Team

| Algorithm | Processing Speed | Memory Used | Battery Overhead | Noise Reduction | Best Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option A: Pure NLMS** | **Ultra-Fast (14 µs)** | **Tiny (256 Bytes)** | **Extremely Low (18 µW)**| **$>22\text{ dB}$ (Walking)** | Best for maximum battery life and lowest memory footprint |
| **Option B: Pure RLS** | Slow (78 µs) | Large (4,096 Bytes) | High (92 µW) | **$>26\text{ dB}$ (Sprints)** | Best if tracking sudden rapid running transitions |
| **Option C: Pure Wavelets** | Block-based (1.8 ms)| Medium (1,536 Bytes) | Low (20 µW) | **$>18\text{ dB}$ (Shivering)**| Best when no wrist reference is available |
| **Option D: Hybrid (NLMS + DWT)**| **Balanced (28 µs)** | **Moderate (1.8 KB)**| **Very Low (38 µW)** | **$>28\text{ dB}$ (All Noise)**| **Recommended for Competition**: Cleans walking and shivering |

---

## 6. Why Single-Sensor Wearables Fail

* **Why Single Chest Patches Fail**: A single chest patch has no way of running NLMS because it has no separate reference sensor on the limb. It must guess whether a vibration came from a footstep or a heartbeat, causing severe errors whenever the patient walks.
* **Why Consumer Smartwatches Fail**: Smartwatches try to clean optical light signals using only the wrist accelerometer. But because wrist blood vessels flop and slosh with arm swings, the optical noise is non-linear and cannot be cleanly subtracted, causing smartwatches to lose pulse tracking during brisk walking.
* **Why Our Dual-Node Setup Wins**: Our chest pendant measures clean bone vibrations, and our wristband provides an independent motion reference. The two devices work together mathematically to cancel out daily body noise.

---

## 7. Key Takeaways in Brief

* **Footsteps Mask Heartbeats**: Walking creates shockwaves $50\times$ larger than heart vibrations at the exact same 1 to 2 Hz frequency.
* **NLMS is the Embedded Gold Standard**: It runs in just 14 microseconds per sample, uses only 256 bytes of memory, and cuts walking noise by over 22 dB.
* **Wavelets Clean Random Shivering**: A 4-level wavelet filter acts like a frequency sieve, stripping out unpredictable muscle twitches without needing a reference sensor.
* **Hybrid Wins for Accuracy**: Combining real-time NLMS with background Wavelet cleaning gives our product clinical-grade signal clarity on an ultra-low power budget ($38\ \mu\text{W}$).
