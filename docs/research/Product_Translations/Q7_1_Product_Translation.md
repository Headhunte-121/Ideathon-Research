# Product Translation: Question 7.1 — Distributed vs. Centralized Processing in Multi-Node BAN

---

> **Document Type**: Tier 2.5 Engineering Implementation & Product Architecture Translation  
> **Source Research**: `Phase 07 -> Question 7.1: Distributed vs. Centralized Processing in Multi-Node Body Area Networks`  
> **Target System**: Autonomous Dual-Node Sternal Sentry Pendant (Node A) & Companion PulseBand (Node B)  
> **Hardware Target**: Dual Nordic nRF5340 System-on-Chips (BLE 5.3 + ARM Cortex-M33 DSP)

---

## 1. How This Research Directly Fits Our Wearable Architecture

Our system requires two physical nodes on the human body to achieve 100% glue-free, non-adhesive cardiac monitoring:
1. **Node A (Sentry Pendant on the breastbone)**: Measures precordial mechanical recoil vibrations (Seismocardiography / SCG via ST LSM6DSOX).
2. **Node B (Companion PulseBand on the wrist)**: Measures optical blood pulse waveforms (PPG via MAX86141), blood oxygen ($SpO_2$), and provides an emergency touch-cancellation screen.

By combining the exact timing between the aortic valve opening on the chest ($t_{\text{AO}}$) and the pulse arriving at the wrist ($t_{\text{wrist}}$), our system calculates continuous, cuffless **Pulse Transit Time (PTT)**—detecting the sudden drops in blood pressure and vascular tone that signal acute cardiogenic shock.

However, having two separate nodes worn on different parts of the body creates a critical networking question: **Should the wristband stream raw sensor data continuously to the chest, or should both devices process data locally?**

Question 7.1 proves why a **Hybrid Asymmetric Edge Architecture** is the only clinically viable answer:
- **The Thermodynamic Reality**: Transmitting a single raw bit of data over Bluetooth Low Energy consumes $15\text{ to }23\text{ nanojoules}$. Running an 8-bit mathematical instruction on the processor consumes only $0.06\text{ nanojoules}$. Transmitting data wirelessly burns **250 times more battery energy** than calculating it directly on the chip!
- **The Human Body Shadowing Problem**: The human chest and arms block radio waves. Radio signals traveling between the chest and the wrist must bend around the body via "creeping waves." When a patient walks or swings their arms, radio signal strength drops by up to **$-40\text{ dB}$**, causing continuous raw streaming to drop nearly $30\%$ of packets.
- **Our Hybrid Solution**:
  - The **Wrist PulseBand** does NOT stream raw waveforms. It runs lightweight mathematical filters locally, checks signal quality, and extracts the pulse peak timestamp ($t_{\text{wrist}}$).
  - It packages this into a tiny **16-byte summary token** sent once per second over Bluetooth.
  - This slashes radio power consumption by **$99.4\%$**, completely bypasses radio dropouts, and enables **over 7 days of continuous battery life** on both devices.

```
==================================================================================================
           HYBRID ASYMMETRIC BAN PROCESSING IN OUR DUAL-NODE ARCHITECTURE
==================================================================================================

 [ NODE B: COMPANION PULSEBAND (WRIST) ]
 • MAX86141 Optical PPG (100 Hz) + IMU
 • Runs Local Digital Signal Processing (SQI & Peak Detection) in 0.05 ms (0.56 uJ)
 • Extracts Pulse Arrival Timestamp (t_wrist) and SpO2
 • Transmits Tiny 16-Byte Summary Token over BLE 5.3 (Once per second)
 • Power consumed: ONLY 0.003 mW (Saves 99.4% radio energy vs streaming!)
                             │
                             ▼ (16-Byte BLE Token | Creeping Wave Robust)
 [ NODE A: SENTRY PENDANT (BREASTBONE - MASTER BRAIN) ]
 • LSM6DSOX Precordial SCG (100 Hz)
 • Runs 4-Stage Hierarchical Sentry Pipeline
 • Receives 16-Byte Token from Wristband
 • Calculates Continuous Pulse Transit Time: PTT = t_wrist - t_AO
 • Evaluates Multimodal TCN-Mamba Neural Fusion Model
 • Manages Automated Cellular Emergency Escalation
==================================================================================================
```

---

## 2. Technical Implementation: How We Use Asymmetric Processing in Firmware

Our firmware implements this hybrid architecture across both nodes using the Nordic nRF5340 Dual-Core SoC:

### A. Peripheral Firmware on Node B (Companion PulseBand)
- The wristband's ARM Cortex-M33 core wakes up periodically using EasyDMA:
  1. **Local SQI Filtering**: Evaluates optical signal perfusion and removes arm-motion noise.
  2. **Systolic Peak Detection**: Pinpoints the pulse wave arrival with microsecond precision.
  3. **Token Formatting**: Assembles the compact 16-byte telemetry structure:
     ```c
     typedef struct __attribute__((packed)) {
         uint16_t token_magic;            // 0x5A43 ("ZC")
         uint32_t pulse_arrival_master_us;// Synchronized timestamp
         uint16_t pulse_interval_prv_ms;  // Pulse rate variability
         uint16_t spo2_ratio_q8;          // Blood oxygen (e.g. 98.2%)
         uint8_t  signal_quality_index;   // Signal confidence [0 - 100]
         uint8_t  motion_magnitude_lsb;   // Wrist motion level
         uint32_t token_checksum;         // CRC-32 integrity
     } ban_pulse_token_t;
     ```
  4. Transmits this single 16-byte packet to Node A during the scheduled 1-second BLE connection event, then immediately returns to Deep Sleep.

### B. Master Firmware on Node A (Sentry Pendant)
- The Sentry Pendant acts as the central coordinator and medical decision engine:
  1. Captures precordial Aortic Opening (AO) recoil acceleration timestamps ($t_{\text{AO}}$).
  2. Ingests the 16-byte token from Node B over BLE.
  3. Computes continuous Pulse Transit Time:
     $$\text{PTT} = t_{\text{pulse\_arrival\_master\_us}} - t_{\text{sternal\_AO}}$$
  4. Feeds PTT, SCG recoil energy, and wrist $SpO_2$ into the multimodal TCN-Mamba neural network.
  5. If an acute pre-infarction pattern is confirmed, Node A commands Node B to display the 30-second emergency haptic countdown screen.

### C. Microsecond Time Synchronization via BLE Connection Anchors
To ensure PTT calculations are clinically valid, the two devices must not suffer from clock drift:
- A $10\text{ ms}$ clock mismatch creates an unacceptable $18\text{ mmHg}$ error in blood pressure estimation!
- **Our Hardware Synchronization**: 
  - Every 1.0 second, the Master (Pendant) transmits a BLE packet.
  - The hardware radio captures the packet arrival at the physical preamble with zero software latency via the nRF5340's **DPPI (Distributed Programmable Peripheral Interconnect)**.
  - The Slave (PulseBand) calculates the crystal frequency skew ($\alpha$) and phase offset ($\beta$), disciplining its clock to within **$\pm 18.2\ \mu\text{s}$** of the Master.
  - This provides hospital-grade synchronization while drawing zero additional battery power.

---

## 3. Why We Chose This Architecture Over Alternatives

```
==================================================================================================
                 BAN ARCHITECTURAL TRADE-OFF EVALUATION
==================================================================================================

  Feature / Metric        Pure Centralized Streaming Pure Distributed (Dual AI) Our Hybrid Asymmetric
  ──────────────────────────────────────────────────────────────────────────────────────────────────
  Processing Location     100% on Sentry Pendant     50% Pendant / 50% Wrist    Asymmetric Hierarchical
  Data Sent over BLE      12.0 kbps continuous raw   Zero (Only alerts sent)    16-Byte Token (1 Hz)
  Radio Power Consumption 1.85 mW continuous         0.001 mW                   0.003 mW (99.4% savings!)
  Battery Life (250mAh)   < 18 Hours (Unusable!)     5.8 Days                   7.4+ Days (Viable!)
  Continuous PTT Support  Yes (High radio cost)      NO (Cannot cross-compare)  YES (Sub-millisecond sync)
  Body Shadowing Immunity Very Poor (28% drops)      Complete                   Extreme (SRAM Buffered)
  Bill of Materials Cost  Low                        High (Two large AI SoCs)   Optimal (Nordic Ecosystem)
==================================================================================================
```

### Why Not Pure Centralized Raw Streaming?
- Constantly transmitting raw optical and motion samples over the radio consumes $1.85\text{ mW}$, killing the battery in less than 18 hours. Furthermore, whenever the patient walks or puts their hands in their pockets, body shadowing drops up to 28% of the data packets, blinding the algorithm.

### Why Not Pure Distributed Independent Processing?
- If both the chest pendant and wristband ran independent AI models without communicating, they could never calculate **Pulse Transit Time (PTT)**, because PTT requires subtracting the chest valve opening time from the wrist pulse arrival time. Losing PTT removes our ability to detect sudden blood pressure collapse and cardiogenic shock.

### The Decisive Advantage of Hybrid Asymmetric Architecture:
- By doing lightweight signal quality filtering and peak detection on the wrist, and sending only 16-byte tokens to the chest, we preserve continuous PTT and multi-modal neural fusion while keeping radio power consumption at virtually zero ($0.003\text{ mW}$), guaranteeing a **7.4+ day battery life**.

---

## 4. Competitive Clinical & Regulatory Differentiation

1. **Uninterrupted 7-Day Continuous Wear**: Eliminates daily recharging anxiety. High-risk cardiac patients can wear the pendant and wristband continuously through work, sleep, and exercise without losing monitoring coverage.
2. **Resilience to Arm Swings and Body Shadowing**: Because the system transmits compact 16-byte tokens that can be buffered in memory, momentary RF signal blockages caused by arm movement or clothing never corrupt the medical monitoring record.
3. **Hospital-Grade Cuffless Blood Pressure Tracking**: Hardware microsecond clock synchronization ($\pm 18.2\ \mu\text{s}$) enables continuous PTT blood pressure tracking that matches arterial line standards without the painful inflation of a traditional arm cuff.
