# Product Translation: Question 11.2 — Embedded Memory Safety, Watchdogs & MCU Lockup Defense

---

> **Document Type**: Tier 2.5 Engineering Implementation Dossier  
> **Question Reference**: `Phase 11 -> Question 11.2`  
> **Source Research**: [`Q11_2_Memory_Corruption_MCU_Lockup.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_11_Failure_Modes_Failsafes/11.2_Memory_Corruption_MCU_Lockup/Q11_2_Memory_Corruption_MCU_Lockup.md)  
> **Target Audience**: Embedded Software Engineers, Firmware Architects, and Medical Device Safety Auditors

---

## 1. How the Finding Fits Our Device Concept

Our dual-node body area network runs continuous real-time machine learning models to detect acute myocardial ischemia and ventricular arrhythmias hours before sudden cardiac arrest occurs. Under international medical standard **IEC 62304**, our embedded software is classified as **Class C** (highest risk level: software failure could cause death or serious injury).

In an embedded medical system operating 24 hours a day for over 30 days without rebooting, software crashes, memory corruption, and processor lockups are fatal. If a software bug or static electricity strike freezes the microcontroller's CPU core while a patient is asleep, the device stops analyzing heart vibrations, creating an unannounced window of vulnerability. To make our wearable mathematically impervious to memory leaks, deadlocks, and silent software freezes, we implement a multi-layer defense architecture leveraging the hardware security features of the Nordic nRF5340 ARM Cortex-M33 microcontroller.

---

## 2. How We Implement It in Hardware & Firmware

### A. Windowed Watchdog Timer (WWDG) Architecture
1. **Clock Independence**:
   - Standard watchdogs can be fooled if the main system clock runs wild or if a runaway program loop repeatedly resets the timer.
   - Our system uses an autonomous Windowed Watchdog Timer driven by an independent $32.768\text{ kHz}$ low-frequency RC oscillator ($LFRC$), completely separate from the main $128\text{ MHz}$ CPU clock.
2. **Two-Sided Refresh Window ($4.0\text{ s} \le t \le 8.0\text{ s}$)**:
   - *Underflow Trap ($> 8.0\text{ s}$)*: If a software deadlock, infinite loop, or frozen driver halts the system supervisor for more than 8 seconds, the watchdog counter hits zero, triggering an immediate hardware reset.
   - *Early Refresh Trap ($< 4.0\text{ s}$)*: If a runaway program loop spins out of control and attempts to clear the watchdog too quickly (earlier than 4 seconds), the hardware detects this abnormal execution and forces an immediate reset.

### B. Hardware Memory Isolation: ARM TrustZone & MPU
1. **TrustZone Secure Enclave**:
   - The ARM Cortex-M33 physically separates code execution into a **Secure World** and a **Non-Secure World**.
   - *Secure World*: Contains the life-critical heart rhythm classifier, cryptographic encryption keys (ARM CryptoCell-312), and the system health supervisor.
   - *Non-Secure World*: Runs the Bluetooth communications stack, flash file system, and user display. A bug, memory leak, or buffer overflow in the Bluetooth stack cannot physically read or overwrite the Secure World's cardiac sentry code.
2. **Hardware Stack Pointer Limit Registers (`MSPLIM` / `PSPLIM`)**:
   - In traditional microcontrollers, stack overflows silently overwrite adjacent program data.
   - The Cortex-M33 hardware compares the stack pointer against programmed limits on every single instruction. If a recursive call or deep stack pushes past the boundary, the hardware halts execution and fires a `UsageFault` in zero clock cycles before any memory corruption occurs.
3. **Execute-Never (`XN`) Memory Protection**:
   - All internal SRAM (data memory) is configured with the `XN` bit enabled by the Memory Protection Unit (MPU). Code can only be executed from Flash memory. Even if corrupted data is injected into an optical PPG buffer, the processor physically refuses to execute instructions from RAM.

### C. Zero-Heap Policy: Strict MISRA-C:2012 Rule 21.3 Compliance
1. **Total Elimination of `malloc()` and `free()`**:
   - Over 30 days of continuous wear, dynamic memory allocation creates heap fragmentation, leading to unpredictable out-of-memory crashes and variable latency.
   - In our firmware, **dynamic memory allocation is 100% prohibited**. Every single buffer, queue, neural network weight array, and thread stack is statically declared at compile time.
2. **Deterministic Memory Slabs**:
   - Where buffers must be shared between sensor threads and machine learning algorithms, the system uses fixed-size Zephyr RTOS memory slabs (`k_mem_slab`), guaranteeing constant-time $O(1)$ allocation and zero fragmentation.

### D. Continuous Register CRC-16 Patrol
- External electromagnetic interference (EMI) or static electricity can cause Single Event Upsets (SEU) that flip bits in the peripheral sensor configuration registers (such as changing the ST LSM6DSOX accelerometer sampling rate).
- Every 5.0 seconds, the health supervisor reads back all 32 configuration registers from each sensor, computes a **CRC-16-CCITT** checksum, and validates it against a factory "golden" reference in secure flash. If a single bit has flipped, the supervisor instantly rewrites the correct configuration.

---

## 3. Why We Chose This Over Alternatives

* **Why Windowed Watchdogs vs. Standard Independent Watchdogs**:
  - *Alternative*: Standard watchdogs only check if the timer has expired.
  - *Engineering Reality*: In over 30% of embedded MCU lockups, the processor enters a rapid infinite fault loop that happens to call the watchdog refresh routine. A standard watchdog is continually cleared, allowing the device to stay frozen forever. The windowed watchdog catches this abnormal behavior by enforcing that refreshes cannot happen too early.
* **Why Static Memory Allocation vs. Dynamic Heaps**:
  - *Alternative*: Many general-purpose embedded systems use dynamic memory pools or standard C `malloc()`.
  - *Clinical Rationale*: A medical device guarding against sudden cardiac arrest cannot afford an unhandled "out of memory" null pointer exception during an acute ischemic event. Static allocation guarantees at compile time that the system will never run out of memory.
* **Why ARM TrustZone vs. Software-Only Task Separation**:
  - *Alternative*: Traditional RTOS systems use software-only task priorities.
  - *Safety Rationale*: Software-only isolation can be bypassed by wild pointers or stack corruption. ARM TrustZone provides silicon-level hardware enforcement; non-secure code physically lacks the bus permissions required to access the secure cardiac monitoring engine.

---

## 4. Summary Specifications Table

| Firmware Safety Feature | Production Specification | Compliance & Safety Rationale |
| :--- | :--- | :--- |
| **Software Safety Level** | IEC 62304 Class C (Death/Serious Injury) | Maximum rigor in architecture, unit testing, and risk traceability |
| **Coding Standard** | MISRA-C:2012 (100% Zero Heap Allocation) | Rule 21.3 compliance guarantees zero heap fragmentation over 30+ days |
| **Watchdog Window ($t_{\text{win}}$)** | $4.0\text{ s} \le t_{\text{refresh}} \le 8.0\text{ s}$ | Traps both frozen threads (late kick) and runaway loops (early kick) |
| **Watchdog Clock Source** | Independent 32.768 kHz Internal LFRC | Remains active even if main system 128 MHz PLL clock freezes |
| **Stack Overflow Trap** | Hardware `MSPLIM` / `PSPLIM` Limit Registers | Instantaneous hardware trap halts execution before memory corruption occurs |
| **RAM Code Execution** | Hardware Execute-Never (`XN = 1`) on all SRAM | Defeats buffer overflow code injection and wild function pointer execution |
| **Configuration Audit** | Periodic 5.0s CRC-16-CCITT Readback Patrol | Detects and corrects electrostatic single-event register bit flips |
| **Crash Diagnostic Dump** | Un-initialized 8 KB Retention SRAM | Saves CPU registers (CFSR, PC, LR) across reboot for post-mortem analysis |
