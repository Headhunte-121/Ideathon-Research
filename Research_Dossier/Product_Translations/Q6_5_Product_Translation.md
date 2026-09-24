# Product Translation: Question 6.5 — Secure Over-the-Air (OTA) Model Updating & Rollback

---

> **Document Type**: Tier 2.5 Engineering Implementation & Product Architecture Translation  
> **Source Research**: `Phase 06 -> Question 6.5: Secure Over-the-Air (OTA) Model Updating & Rollback`  
> **Target System**: Autonomous Dual-Node Sternal Sentry Pendant & Companion PulseBand  
> **Hardware Target**: Nordic Semiconductor nRF5340 Dual-Core SoC (1024 KB Flash, 512 KB SRAM, CryptoCell-312) + MCUboot Secure Bootloader

---

## 1. How This Research Directly Fits Our Wearable Architecture

Our wearable monitors high-risk cardiac patients continuously to catch the subtle 1-to-6-hour mechanical pre-infarction cascade. Over time, cardiology clinical trials will reveal new ischemic waveform variations, updated demographic calibrations, or more refined filter coefficients. We must be able to update the artificial intelligence models deployed on the patient's chest pendant and wristband without requiring the patient to visit a hospital or plug the device into a computer.

However, performing Over-the-Air (OTA) wireless updates on an active, life-critical medical wearable creates two catastrophic risks:
1. **The Bricking Risk**: If the patient walks out of Bluetooth range or the battery dies halfway through an update, a standard single-memory chip is corrupted, rendering the device dead and leaving the patient unprotected.
2. **The Security Risk (Model Poisoning)**: If an attacker hacks the phone app and sends altered AI weights, they could secretly disable heart attack alerts or cause constant fake alarms.

Question 6.5 solves both risks through a **Secure Dual-Bank Differential OTA Pipeline**:
- **Dual-Bank Flash Isolation (A/B Slots)**: The new model is downloaded into a secondary storage slot (Slot 1) while the active model (Slot 0) continues monitoring the patient's heart without interruption.
- **Differential Binary Compression (`bsdiff`)**: Instead of transmitting the entire $410\text{ KB}$ neural network, the cloud calculates only the mathematical difference (delta) from the prior version, compressing the download to just **$28.4\text{ KB}$** (a $93\%$ reduction) that transfers over BLE in **under 4 seconds**.
- **Hardware Cryptographic Defense**: The nRF5340's integrated **ARM CryptoCell-312** checks a digital signature (ECDSA P-256) and a tamper-proof hardware version counter. Any unauthorized, altered, or downgraded model is instantly rejected.
- **Self-Healing Watchdog Rollback**: The new model is tested on pre-loaded golden heart signals in RAM. If it crashes, produces erratic answers, or fails to service the hardware watchdog timer within 4 seconds, the system automatically reverts to the previous working model in **under 120 milliseconds**.

```
==================================================================================================
           DUAL-BANK OTA UPDATE & SAFETY INTERLOCK IN OUR SENTRY PENDANT (nRF5340)
==================================================================================================

 [ CLOUD SERVER ] ──► Compresses Update via bsdiff (410 KB ──► 28.4 KB) ──► Signs with ECDSA Key
                             │
                             ▼ (BLE 5.3 Transfer: ~3.8 Seconds)
 [ WEARABLE PENDANT ]
 ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
 │ Primary Slot 0 (448 KB)        │ Secondary Slot 1 (448 KB)      │ Bootloader (64 KB Locked) │
 │ [ ACTIVE FIRMWARE & MODEL ]    │ [ INCOMING OTA DELTA IMAGE ]   │ [ MCUboot + Public Key ]  │
 │ Continuous heart monitoring    │ Download completes safely      │ Write-protected in Flash  │
 └─────────────────────────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼ (Download Complete)
 [ ARM CryptoCell-312 Hardware Check ]
 ├── Check 1: ECDSA P-256 Digital Signature Matches Medical Manufacturer Public Key?
 ├── Check 2: Monotonic Hardware Counter Prevents Downgrade Attack?
 └── Check 3: SHA-256 Integrity Hash Intact?
                             │
              ┌──────────────┴──────────────┐
           PASS                             FAIL
              │                               │
              ▼                               ▼
 [ Atomic MCUboot Sector Swap ]    [ Discard Corrupt Slot 1 ]
 Swap Slot 0 and Slot 1 in Flash   [ Stay on Safe Slot 0 ]
              │
              ▼
 [ In-RAM Golden Vector Test ]
 Run 10 Pre-Stored Heart Waveforms
              │
              ├── Crashes or Deviation > 0.5% ──► [ Watchdog Timer Expires ] ──► [ AUTO-ROLLBACK! ]
              │                                                                  Reverts to Slot 0
              ▼ Passed Test Vectors & 50 Patient Beats!                          in <120 ms!
 [ Permanent Image Lock (boot_set_confirmed()) ]
 Monotonic Counter Burned; Safe Continuous Monitoring Resumes
==================================================================================================
```

---

## 2. Technical Implementation: How We Use Secure OTA in Firmware

Our embedded firmware executes updates through four strictly segregated layers compliant with **IEC 62304 Class C** and **FDA Cybersecurity Guidance**:

### A. Flash Partition Allocation on the nRF5340
We configure the Nordic nRF5340 Application Core's $1024\text{ KB}$ Flash memory via the Zephyr Project partition manager:
- `0x00000 - 0x0FFFF` ($64\text{ KB}$): **MCUboot Bootloader** (contains the manufacturer's root public key, locked via write-protection).
- `0x10000 - 0x7FFFF` ($448\text{ KB}$): **Slot 0 (Primary / Active)**: Runs the active operating system, signal processing, and INT8 TCN neural network.
- `0x80000 - 0xEFFFF` ($448\text{ KB}$): **Slot 1 (Secondary / Staging)**: Receives the OTA binary image over BLE.
- `0xF0000 - 0xF7FFF` ($32\text{ KB}$): **Scratch Partition**: Used by MCUboot for power-fail-safe atomic sector swaps.
- `0xF8000 - 0xFFFFF` ($32\text{ KB}$): **Factory Golden Recovery**: Permanent immutable backup firmware.

### B. Differential Delta Reconstruction (`bsdiff` + Heatshrink)
- To avoid battery drain, our smartphone companion app receives a compressed binary delta patch from the medical cloud server ($28.4\text{ KB}$).
- The phone streams this patch over a high-throughput BLE 5.3 L2CAP connection-oriented channel ($8\text{ KB/s}$).
- The nRF5340 decompresses the patch using the lightweight `heatshrink` LZSS engine into a small $4\text{ KB}$ streaming RAM buffer, generating the full candidate model directly into Flash Slot 1 without allocating large memory chunks.

### C. Hardware Cryptographic Authentication (CryptoCell-312)
- Before the bootloader touches the candidate image, the **ARM CryptoCell-312** coprocessor performs hardware-accelerated signature validation:
  1. Computes the SHA-256 hash of the candidate image.
  2. Verifies the ECDSA P-256 signature against the manufacturer's public key burned into the nRF5340's hardware One-Time-Programmable (OTP) eFuses.
  3. Checks the hardware security counter: if the update's version counter is less than or equal to the device's internal monotonic counter, the image is rejected as an adversarial downgrade attack.
- Verification completes in **$0.15\text{ ms}$**, consuming negligible power.

### D. Automated Watchdog Rollback & Golden Vector Testing
- MCUboot swaps Slot 0 and Slot 1 in "Test Mode" (`BOOT_SWAP_TYPE_TEST`).
- Upon reboot, the new firmware initializes and immediately executes **ten pre-compiled golden test waveforms** stored in protected Flash:
  - 5 waveforms representing normal, healthy cardiac mechanics (must predict $P < 0.15$).
  - 5 waveforms representing acute ischemic contractile failure (must predict $P > 0.85$).
- If any prediction deviates by more than $0.5\%$, or if an unhandled floating-point exception or stack overflow occurs, the firmware halts and intentionally lets the **4.0-second Hardware Watchdog Timer (WDT)** expire.
- Upon reset, MCUboot recognizes that the test image failed verification, restores the original verified model from Slot 1, and flags an update error to the cloud, **restoring full cardiac surveillance in under 120 milliseconds**.

---

## 3. Why We Chose This Architecture Over Alternatives

```
==================================================================================================
                 OTA UPDATE ARCHITECTURE TRADE-OFF EVALUATION
==================================================================================================

  Feature / Metric        Single-Bank Direct Write   Full-Image Dual-Bank      Our Dual-Bank Differential
  ──────────────────────────────────────────────────────────────────────────────────────────────────
  Flash Layout            Single 800 KB Slot         Dual 448 KB Slots         Dual 448 KB Slots + Scratch
  Update Payload Size     410 KB (Uncompressed)      410 KB (Full Image)       28.4 KB (bsdiff Delta)
  BLE Transfer Duration   51.2 Seconds               51.2 Seconds              3.55 Seconds (14x Faster!)
  Transfer Battery Energy 22.8 mAh                   22.8 mAh                  1.6 mAh (Negligible)
  Bricking Protection     None (Power drop = BRICK)  Complete (Slot 0 Safe)    Complete (Slot 0 Safe)
  Adversarial Security    Weak (CRC32 checksum)      Strong (ECDSA P-256)      Extreme (ECDSA + Anti-Rollback)
  Self-Healing Rollback   Impossible                 Manual via Factory Pin    Automated via Watchdog (<120ms)
==================================================================================================
```

### Why Not Single-Bank Direct Flash Overwriting?
- In single-bank architectures, incoming data overwrites the running program. If battery power fails, the Bluetooth connection drops, or a write error occurs, the chip is permanently bricked. In a life-critical cardiac monitor, an unbootable device leaves the patient with zero protection against sudden death.

### Why Not Full-Image Dual-Bank Updates?
- While standard dual-bank updates protect against bricking, sending the full $410\text{ KB}$ neural network image takes over 50 seconds of continuous radio transmission. This creates significant radio interference, drains battery life, and increases the chance of packet loss in crowded RF environments.

### The Decisive Advantage of Differential Delta + Hardware Rollback:
- By combining `bsdiff` delta compression with dual-bank isolation, our OTA transfer takes **only 3.55 seconds**, draws less than $2\text{ mAh}$ from the battery, and guarantees that the device can never be bricked or hijacked by unauthorized model poisoning.

---

## 4. Competitive Clinical & Regulatory Differentiation

1. **Compliance with FDA Premarket Cybersecurity Guidelines (2023)**: Our architecture natively implements the FDA's mandatory cybersecurity triad: (1) Cryptographic Root of Trust, (2) Anti-Rollback Monotonic Counters, and (3) In-Field Secure Updatability without physical device recalls.
2. **Zero Clinical Downtime for High-Risk Patients**: The sector swap takes less than $120\text{ ms}$, meaning the patient's continuous ischemic surveillance is never interrupted for more than a fraction of a single heartbeat during an update.
3. **Guaranteed Diagnostic Integrity via Golden Test Vectors**: Software updates cannot accidentally alter the clinical sensitivity or specificity of the algorithm. By running standardized cardiac vectors in RAM before locking in the update, our firmware guarantees that clinical diagnostic accuracy remains uncompromised.
