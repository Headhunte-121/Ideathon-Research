# Product Translation: Question 11.3 — Power Hierarchy & "Dying Gasp" Reserve Capacitor Energy

---

> **Document Type**: Tier 2.5 Engineering Implementation Dossier  
> **Question Reference**: `Phase 11 -> Question 11.3`  
> **Source Research**: [`Q11_3_Reserve_Capacitor_Power_Hierarchy.md`](file:///c:/College/Ideathon/Research_Dossier/Phase_11_Failure_Modes_Failsafes/11.3_Reserve_Capacitor_Power_Hierarchy/Q11_3_Reserve_Capacitor_Power_Hierarchy.md)  
> **Target Audience**: Power Electronics Engineers, Hardware Architects, and Clinical Safety Systems Integrators

---

## 1. How the Finding Fits Our Device Concept

A cardiac monitoring wearable faces a catastrophic edge case: **the worst-case coincidence scenario**. In this scenario, a high-risk cardiac patient suffers Sudden Cardiac Arrest (SCA)—their heart enters ventricular fibrillation, the heart stops pumping blood, and blood pressure collapses to zero—at the exact minute the wearable's rechargeable lithium battery drops below minimum operating voltage ($3.00\text{ V}$, completely depleted).

In consumer smartwatches and ordinary fitness bands, the power management chip protects the lithium battery by shutting off instantly. The device dies, the screen turns black, and no emergency call is ever made. The patient perishes silently.

To prevent this tragedy, our Sentry Sternal Pendant incorporates a dedicated **Power Supply Hierarchy & Reserve Capacitor Energy Architecture**. Even when the main battery is completely empty, the system retains an independent reservoir of electrostatic energy in a high-density, low-ESR supercapacitor tank ($47\text{ mF}, 5.5\text{ V}$). If the heart collapses during a battery brownout, the device executes an automated **"Dying Gasp" Emergency Beacon**: it isolates the depleted battery, switches to reserve capacitor power, blasts a high-power Long Range Bluetooth SOS signal, sounds a 75 dB acoustic alarm, and saves diagnostic heart data before safely shutting down.

---

## 2. How We Implement It in Hardware & Firmware

### A. Power Supply Hierarchy & Voltage Supervisions
The power management architecture defines five strictly controlled operational voltage tiers:
1. **Nominal Monitoring ($3.70\text{ V} - 4.20\text{ V}$)**: 100% full-rate dual-node sensing (104 Hz chest vibrations, 500 Hz wrist optical pulse, continuous Bluetooth sync).
2. **Low-Battery Alert ($3.40\text{ V} - 3.70\text{ V}$)**: Gentle visual prompt on companion app; lengthens background cloud sync to save energy.
3. **Load Shedding Mode ($3.20\text{ V} - 3.40\text{ V}$)**: Non-critical loads are disabled: the wrist screen is turned completely off, flash memory wear-leveling is halted, and optical LEDs are duty-cycled to conserve every remaining electron.
4. **Power-Fail Interrupt ($V_{\text{PFI}} = 3.05\text{ V}$)**: An ultra-fast hardware comparator detects that the battery is about to die and generates a high-priority Non-Maskable Interrupt (NMI) to the microcontroller.
5. **Dying Gasp Trigger ($3.00\text{ V}$)**: The main battery is physically disconnected; system runs purely on reserve capacitor energy.

### B. Hardware Component Selection: The Reserve Energy Tank
1. **Selected Supercapacitor (Murata DMF3Z5R5H474M3DTA0)**:
   - *Capacitance*: $47\text{ mF}$ ($0.047\text{ Farads}$) at $5.5\text{ V}$ rated.
   - *Energy Storage*: Stores $158.2\text{ mJ}$ of usable energy between $3.30\text{ V}$ and $1.80\text{ V}$.
   - *Ultra-Low Resistance ($40\ \text{m}\Omega\text{ ESR}$)*: Under a high-power $25\text{ mA}$ radio transmission pulse, the internal voltage dip across the capacitor is only $1.0\text{ mV}$, preventing premature reset.
   - *Ultra-Low Leakage ($1.2\ \mu\text{A}$)*: Draws less than $0.6\%$ of our average system power, ensuring zero impact on the $>30\text{ days}$ battery life.
2. **PowerPath Controller & Isolation Switch (Analog Devices LTC3226 + TI TPS22918)**:
   - Contains a back-to-back P-channel MOSFET switch.
   - When battery voltage collapses to $3.00\text{ V}$, the switch isolates the battery in less than $15\ \mu\text{s}$. This prevents the dying battery's internal chemical resistance from pulling down the reserve capacitor.
   - An ideal diode controller seamlessly routes capacitor energy to the system's high-efficiency buck-boost regulator (TI TPS62840, 88.5% efficiency).

### C. The 6-Step "Dying Gasp" Firmware Sequence
When the Power Fail Interrupt triggers during a cardiac emergency, the firmware executes a deterministic sequence in under 180 milliseconds:
1. **Battery Isolation ($< 15\ \mu\text{s}$)**: Microcontroller pulls the isolation gate high; supercapacitor instantly takes over system power.
2. **Payload Construction ($5.0\text{ ms}, 31.5\ \mu\text{J}$)**: Assembles a 37-byte emergency packet containing the victim's anonymized medical ID, last known GPS coordinate, confirmed ventricular fibrillation rhythm flag, and an AES-128 GCM cryptographic signature.
3. **Data Logging ($2.5\text{ ms}, 20.3\ \mu\text{J}$)**: Writes the final cardiac vibration and pulse waveforms into non-volatile SPI flash memory so doctors can inspect the exact moments leading to the arrest.
4. **BLE 5.3 Coded PHY Transmission ($51.6\text{ ms}, 2.28\text{ mJ}$)**: Transmits 6 redundant advertising packets at maximum $+8\text{ dBm}$ power on long-range Coded PHY ($S=8$). This penetrating radio signal reaches companion phones through walls up to 100 meters away.
5. **Acoustic Distress Chirp ($120\text{ ms}, 3.89\text{ mJ}$)**: Drives the resonant $2,730\text{ Hz}$ piezoelectric sounder at $75\text{ dB}$, immediately alerting family members or bystanders in the room.
6. **Controlled Power-Down ($< 50\text{ nA}$)**: Shuts off all peripherals and enters deep ship mode to protect the battery from cell damage until placed on a charger.

---

## 3. Why We Chose This Over Alternatives

* **Why an Electrostatic Supercapacitor vs. Squeezing More Power from the Battery**:
  - *Alternative*: Many devices attempt to keep transmitting from the dying chemical battery down to $2.5\text{ V}$.
  - *Electrochemistry Reality*: Discharging a lithium-polymer battery below $2.70\text{ V}$ causes the copper current collector to dissolve into the electrolyte. When recharged, the copper forms metallic spikes (dendrites) that puncture the separator, causing internal short circuits and battery fires. Our design respects the chemical safety cutoff ($2.80\text{ V}$) by using an external supercapacitor for emergency energy.
* **Why BLE Coded PHY (Long Range) vs. Standard Bluetooth**:
  - *Alternative*: Standard Bluetooth 1M PHY consumes slightly less energy per packet.
  - *Clinical Safety Rationale*: If a patient collapses at home while their companion smartphone is in another room, standard Bluetooth often fails to penetrate interior walls. BLE Coded PHY ($S=8$) provides a $+12\text{ dB}$ link margin improvement, guaranteeing that the dying-gasp distress beacon penetrates walls to summon emergency rescue.
* **Why Murata Supercapacitor vs. Standard Tantalum Capacitors**:
  - *Alternative*: Using 10 small tantalum polymer capacitors on the circuit board.
  - *Engineering Sizing*: As proven in our physical calculations, a tantalum array can store only $0.33\text{ mJ}$ to $3.36\text{ mJ}$—far below the $15.54\text{ mJ}$ required for redundant radio bursts and acoustic chirping. The Murata supercapacitor provides $158.2\text{ mJ}$ ($10\times$ our requirement) in a slim 3.2 mm profile that fits easily inside the pendant housing.

---

## 4. Summary Specifications Table

| Parameter | Production Value | Systems Engineering Significance |
| :--- | :--- | :--- |
| **Reserve Storage Component** | Murata DMF3Z5R5H474M3DTA0 | $47\text{ mF}, 5.5\text{ V}$, ultra-low ESR ($40\ \text{m}\Omega$) supercapacitor |
| **Usable Reserve Energy** | $158.2\text{ mJ}$ (between 3.3V and 1.8V) | $10.18\times$ greater than minimum required emergency energy ($15.54\text{ mJ}$) |
| **Parasitic Leakage Current** | $1.2\ \mu\text{A}$ at $25^\circ\text{C}$ | Represents only $0.64\%$ of average power; zero penalty on 30-day battery life |
| **Battery Isolation Speed** | $< 15\ \mu\text{s}$ via back-to-back P-FETs | Disconnects collapsing battery before voltage sag trips microcontroller reset |
| **Emergency Radio Link** | BLE 5.3 Coded PHY ($S=8, +8\text{ dBm}$) | $+12\text{ dB}$ link margin guarantees domestic wall penetration to gateway |
| **Acoustic SOS Chirp** | $75\text{ dB}$ at 10 cm ($2,730\text{ Hz}$ tone) | Piercing resonant frequency instantly alerts nearby bystanders or family |
| **Emergency Execution Duration** | $178.6\text{ ms}$ total execution time | Completes radio transmission and logging before physical capacitor depletion |
