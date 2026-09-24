# Question 2.1: Product Translation & System Implementation
### How Sensing Modalities & Chip Architectures Translate Directly into Our Hardware Bill of Materials (BOM)

---

> **Ideathon Translation Reference**: `Research_Dossier -> Product_Translations -> Q2_1_Product_Translation.md`  
> **Topic**: Translating Multi-Modal Sensing Physics into Commercial Off-The-Shelf (COTS) Integrated Circuits, Bus Architecture, and Circuit Schematics  
> **Source Files**:
> - Quick Takeaway: [Q2_1_Takeaway.md](file:///c:/College/Ideathon/Research_Dossier/Takeaways/Q2_1_Takeaway.md)
> - Clinical Research Vault: [Q2_1_Sensing_Modalities_Biomarker_Mapping.md](file:///c:/College/Ideathon/Research_Dossier/Phase_02_Signal_Acquisition_Physics/2.1_Sensing_Modalities_Biomarker_Mapping/Q2_1_Sensing_Modalities_Biomarker_Mapping.md)

---

## 1. Subsystem 1: Electrodynamics & Thoracic Bio-Impedance (ECG + Bio-Z)

### What the Transduction Physics Proved (Tier 3)
Biopotentials on the chest surface are microvolt-to-millivolt signals ($0.5\text{ to }2.5\text{ mV}$) with a high source impedance ($10\text{ k}\Omega\text{ to }1\text{ M}\Omega$). Simultaneously, measuring thoracic fluid congestion requires injecting a high-frequency constant alternating current ($50\text{--}100\text{ kHz}$) and measuring sub-ohm changes ($\Delta Z \approx 0.05\text{--}0.2\ \Omega$) on a $20\text{--}50\ \Omega$ baseline.

### How It Fits Into Our Product Concept
To maintain an ultra-compact, lightweight chest pod that does not look like a bulky hospital monitor, we cannot afford multiple separate bulky chips for ECG and Bio-Z. We need a single, ultra-low-power integrated Analog Front-End (AFE) that combines high-precision ECG biopotential measurement with an integrated respiration and thoracic impedance engine.

### How We Are Using It in the Device
- **Selected Component**: **Texas Instruments ADS1292R** (Dual-channel, 24-bit Analog Front-End).
- **Circuit Architecture**:
  - *Channel 1*: Configured for single-lead bipolar ECG with Right Leg Drive (RLD) for common-mode rejection ($CMRR > 105\text{ dB}$).
  - *Channel 2*: Configured for respiration and thoracic bio-impedance (Bio-Z), utilizing the internal modulation/demodulation circuitry at $64\text{ kHz}$.
- **Bus Interface**: High-speed Serial Peripheral Interface (SPI). Data is read in 3-byte packets per channel.
- **Power Consumption**: Only **$335\ \mu\text{W}$ per channel** at $3.0\text{V}$, allowing continuous multi-day operation on a small 150 mAh LiPo battery.

### Why We Chose This Component
- **Single-Chip Integration**: Replaces what previously took 15 discrete operational amplifiers, analog switches, and ADCs with a tiny $5\text{ mm} \times 5\text{ mm}$ QFN package.
- **24-Bit Dynamic Range**: Eliminates the risk of ADC saturation from motion artifacts without requiring complex variable gain amplifiers.
- **Why Alternatives Fail**: General-purpose microcontrollers with internal 10-bit or 12-bit ADCs lack the Common-Mode Rejection Ratio (CMRR) and low-noise front-end needed to resolve microvolt ischemic ECG changes.

---

## 2. Subsystem 2: Mechanical Micro-Vibrations & Kinematics (SCG / GCG)

### What the Transduction Physics Proved (Tier 3)
Cardiac recoil micro-vibrations (SCG) generate forces of **$5\text{ to }50\text{ milli-g}$** ($0.05\text{ to }0.5\ \text{m/s}^2$) in the frequency band between $0.5\text{ Hz}$ and $50\text{ Hz}$. 
Simultaneously, human walking and body movement generate forces up to **$\pm 2\text{g}$ to $\pm 4\text{g}$**.
The sensor must have an ultra-low noise floor ($<70\ \mu\text{g}/\sqrt{\text{Hz}}$) to resolve the tiny 5 milli-g heart recoil while maintaining a wide enough dynamic range ($\pm 4\text{g}$) to prevent clipping during movement.

### How It Fits Into Our Product Concept
This component serves as our **Dual-Purpose Kinematic Core**. It measures mechanical heart contractions (SCG) when the user is resting, and acts as a physical activity classifier (IMU) to detect walking, running, and falls.

### How We Are Using It in the Device
- **Selected Component**: **STMicroelectronics LSM6DSOX** (6-axis iNEMO inertial module: 3-axis accelerometer + 3-axis gyroscope).
- **Key Hardware Features**:
  - *Ultra-Low Noise*: Accelerometer noise density of **$60\ \mu\text{g}/\sqrt{\text{Hz}}$**, resolving micro-g cardiac fiducial points easily.
  - *Embedded Machine Learning Core (MLC)*: Features an on-chip finite state machine and decision tree processor that classifies user activity (resting, walking, running, falling) drawing only **$4\ \mu\text{A}$** without waking the main system microcontroller.
  - *FIFO Buffer*: 9-kbyte internal FIFO stores up to 3 seconds of high-rate data, allowing the main MCU to sleep 95% of the time and read data in rapid burst DMA transfers.

### Why We Chose This Component
- **Zero Compute Burden on Master MCU**: The LSM6DSOX runs activity classification autonomously inside the sensor silicon, preserving battery life.
- **Why Alternatives Fail**: Cheap consumer accelerometers (e.g., ADXL345) have noise densities $>300\ \mu\text{g}/\sqrt{\text{Hz}}$, which completely drowns out subtle SCG aortic opening peaks in electronic noise.

---

## 3. Subsystem 3: Opto-Vascular Hemodynamics (Sternal Microvascular PPG)

### What the Transduction Physics Proved (Tier 3)
The pulsatile arterial blood volume (AC component) represents only **$0.1\%$ to $2\%$** of the total optical signal; the remaining $98\%$ is a massive non-pulsatile DC pedestal from skin, fat, bone, and venous blood. Furthermore, ambient sunlight and fluorescent room flicker ($100\text{--}120\text{ Hz}$) leak through skin tissue.

### How It Fits Into Our Product Concept
This component provides **Sternal Blood Volume, $SpO_2$, and Pulse Arrival Time (PAT)**. It must cancel ambient light and resolve the tiny $0.1\%$ pulsatile wave with high dynamic range.

### How We Are Using It in the Device
- **Selected Component**: **Analog Devices / Maxim MAX86141** (Optical Pulse Oximeter & Heart Rate AFE).
- **Optical Configuration**:
  - Drives dual high-efficiency LEDs: Red ($660\text{ nm}$) and Infrared ($940\text{ nm}$).
  - Reads from a low-capacitance PIN photodiode placed $6\text{ mm}$ away from the LEDs with an internal optical barrier to prevent direct light piping through the silicone casing.
- **Key Hardware Features**:
  - *Ambient Light Cancellation (ALC)*: On-chip dual-stage ambient light rejection exceeds **$90\text{ dB}$**, eliminating indoor light flicker and outdoor sunlight distortion.
  - *19-Bit High-Resolution ADC*: Resolves the tiny AC pulse with sub-millivolt precision.

### Why We Chose This Component
- **Medical-Grade Dynamic Range**: $>100\text{ dB}$ dynamic range prevents the sensor from saturating when the patch flexes against the skin.
- **Why Alternatives Fail**: Simple analog phototransistors drift heavily with ambient temperature and saturate immediately when exposed to sunlight.

---

## 4. Subsystem 4: Digital Bus Architecture & Power Optimization

### What the Transduction Physics Proved (Tier 3)
Streaming 6 high-rate sensor channels continuously over a shared I2C bus at 100 kHz causes **bus contention, fixed-address collisions, and data packet drops**. Furthermore, frequent CPU wake-ups consume up to $10\times$ more energy than the sensors themselves.

### How It Fits Into Our Product Concept
This establishes our **High-Speed SPI & Burst DMA Architecture**.
The microchip topology is engineered to maximize sleep time for the main brain.

### How We Are Using It in the Device
1. **SPI Bus Dominance**: All high-rate streaming sensors (ADS1292R, LSM6DSOX, MAX86141) communicate over dedicated high-speed SPI channels (up to 10 MHz) with independent Chip Select (`CS`) pins.
2. **Hardware FIFO Watermark Interrupts**: Sensors buffer their own data in internal hardware FIFOs. When the FIFO reaches 80% capacity, a single hardware interrupt wakes the MCU.
3. **Burst Direct Memory Access (DMA)**: The MCU core uses DMA to slurp the buffered packets across SPI in a few microseconds, processes the data, and returns immediately to deep sleep ($<5\ \mu\text{A}$).

---

## 5. Summary Hardware Component Scorecard

| Modality | Chosen Integrated Circuit | Package & Footprint | Active Power Draw | Key Architectural Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **ECG + Bio-Z** | Texas Instruments **ADS1292R** | 32-pin QFN ($5\times 5\text{ mm}$) | $670\ \mu\text{W}$ (both channels) | 24-bit $\Delta\Sigma$ ADC; integrated respiration impedance engine |
| **SCG / Kinematics** | STMicroelectronics **LSM6DSOX** | 14-pin LGA ($2.5\times 3\times 0.83\text{ mm}$) | $0.55\ \text{mA}$ (high-perf) | $60\ \mu\text{g}/\sqrt{\text{Hz}}$ ultra-low noise; embedded Machine Learning Core |
| **Sternal PPG / $SpO_2$** | Analog Devices **MAX86141** | 20-pin WLCSP ($2\times 1.5\text{ mm}$) | $1.2\ \text{mA}$ (pulsed) | 19-bit ADC; $>90\text{ dB}$ ambient light rejection; dual optical channels |
| **Acoustic Gallops** | Knowles **SPH0645LM4H** | Digital MEMS ($3.5\times 2.65\text{ mm}$) | $600\ \mu\text{A}$ | Direct 24-bit I2S digital output; acoustic impedance matching port |
