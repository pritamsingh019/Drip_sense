# Drip-Sense — Product Requirements Document (PRD)

> **Version:** 1.0  
> **Date:** 2026-02-19  
> **Status:** Draft  
> **Author:** Drip-Sense Engineering Team

---

## 1. Executive Summary

**Drip-Sense** is an autonomous intravenous (IV) drip management system designed to eliminate the risks of manual IV monitoring in hospitals and clinics. By combining real-time gravimetric sensing, intelligent flow-rate computation, and automated servo-actuated tube clamping, Drip-Sense transforms a passive IV stand into a smart, self-regulating medical device.

The system is built around the **ESP32 microcontroller**, leveraging its dual-core architecture, integrated Wi-Fi/BLE, and low-power modes to deliver a compact, cost-effective (~₹2,800 INR per unit) solution that is suitable for deployment in resource-constrained healthcare environments across India and emerging markets.

---

## 2. Problem Statement

### 2.1 Current Challenges

| Challenge | Impact |
|---|---|
| **Manual monitoring burden** | Nurses must visually check IV bags every 15–30 minutes, diverting attention from critical patients |
| **Air embolism risk** | When an IV bag empties, air can enter the line — a potentially fatal complication |
| **Uncontrolled flow rates** | Roller clamp adjustments are imprecise, leading to over-infusion or under-infusion |
| **No remote visibility** | Physicians and charge nurses have no real-time view of infusion status across the ward |
| **Alarm fatigue** | Existing IV pumps generate excessive false alarms, leading staff to ignore genuine alerts |

### 2.2 Target Outcome

A bedside device that:
- Continuously measures remaining IV fluid volume via weight
- Computes real-time drip rate and estimated time-to-empty
- Automatically clamps the IV tube when the bag is critically low or an anomaly is detected
- Pushes telemetry to a cloud dashboard for centralized ward monitoring
- Alerts nursing staff via audible buzzer, on-device OLED display, and cloud notifications

---

## 3. User Personas

### 3.1 Bedside Nurse — "Priya"
- **Role:** Primary caregiver, manages 4–8 patients per shift
- **Pain point:** Constant rounds to check IV bags; missed alerts during emergencies
- **Need:** Automatic drip stop on empty bag; loud bedside alarm; glanceable OLED status
- **Interaction:** Powers on device, attaches to IV stand, runs calibration, monitors OLED

### 3.2 Attending Physician — "Dr. Mehta"
- **Role:** Oversees treatment plans, adjusts infusion orders
- **Pain point:** No real-time visibility into infusion progress from the nursing station
- **Need:** Cloud dashboard showing all active IV sessions; flow-rate history; anomaly logs
- **Interaction:** Views web dashboard; receives push notifications on critical events

### 3.3 Hospital IT / Biomedical Engineer — "Arjun"
- **Role:** Maintains medical devices, manages hospital network
- **Pain point:** Device provisioning, firmware updates, network security
- **Need:** OTA firmware update capability; Wi-Fi provisioning tool; device health diagnostics
- **Interaction:** Configures Wi-Fi via BLE provisioning; triggers OTA updates; reviews system logs

---

## 4. Functional Requirements

### 4.1 Weight Measurement & Fluid Tracking

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Measure IV bag weight continuously using a load cell + HX711 ADC at ≥10 Hz | **P0** |
| FR-02 | Apply digital filtering (EMA / Kalman) to suppress mechanical vibration noise | **P0** |
| FR-03 | Convert filtered weight to remaining volume (mL) using density mapping | **P0** |
| FR-04 | Calculate real-time flow rate (mL/min) from weight delta over time | **P0** |
| FR-05 | Estimate time-to-empty based on current flow rate | **P1** |

### 4.2 Safety & Auto-Cutoff

| ID | Requirement | Priority |
|---|---|---|
| FR-06 | Detect critically low fluid level (< 10 mL threshold, configurable) | **P0** |
| FR-07 | Actuate servo motor to clamp IV tube within 2 seconds of threshold breach | **P0** |
| FR-08 | Detect free-flow condition (flow rate > 150% of expected) and trigger clamp | **P0** |
| FR-09 | Detect air-in-line condition (sudden weight plateau + drip stop) | **P1** |
| FR-10 | Provide manual override button to release servo clamp | **P0** |

### 4.3 User Interface (OLED + Buzzer)

| ID | Requirement | Priority |
|---|---|---|
| FR-11 | Display real-time weight, flow rate, and time-to-empty on 0.96" OLED | **P0** |
| FR-12 | Show system status (calibrating, monitoring, alarm, clamped) via status icons | **P0** |
| FR-13 | Sound buzzer pattern for: low fluid (intermittent), emergency clamp (continuous), calibration complete (double beep) | **P0** |
| FR-14 | Support OLED screen-saver / dimming after 60s of inactivity to extend display life | **P2** |

### 4.4 Connectivity & Telemetry

| ID | Requirement | Priority |
|---|---|---|
| FR-15 | Connect to hospital Wi-Fi (WPA2-Enterprise support) | **P0** |
| FR-16 | Publish telemetry (weight, flow rate, status, battery) via MQTT every 5 seconds | **P0** |
| FR-17 | Fall back to BLE beacon mode if Wi-Fi is unavailable | **P1** |
| FR-18 | Support OTA firmware updates over Wi-Fi | **P1** |
| FR-19 | Provide BLE-based Wi-Fi provisioning for initial setup | **P1** |

### 4.5 Calibration & Diagnostics

| ID | Requirement | Priority |
|---|---|---|
| FR-20 | Support two-point load cell calibration (zero + known weight) | **P0** |
| FR-21 | Store calibration coefficients in non-volatile storage (NVS) | **P0** |
| FR-22 | Expose serial debug interface for diagnostics | **P1** |
| FR-23 | Log system events to flash-based ring buffer | **P1** |

---

## 5. Non-Functional Requirements

| Category | Requirement | Target |
|---|---|---|
| **Accuracy** | Weight measurement accuracy | ±1 g after calibration |
| **Latency** | Sensor-to-display update latency | < 100 ms |
| **Safety response** | Time from threshold breach to servo clamp engagement | < 2 s |
| **Uptime** | Continuous operation without reboot | ≥ 72 hours |
| **Power** | Operating current (active monitoring) | < 250 mA @ 5V |
| **Power** | Deep-sleep current (standby) | < 10 µA |
| **Temperature** | Operating temperature range | 10°C – 45°C |
| **Connectivity** | Wi-Fi reconnection time after dropout | < 10 s |
| **Memory** | Firmware flash footprint | < 1.5 MB |
| **Memory** | RAM usage (heap) | < 200 KB |

---

## 6. Hardware Constraints

The firmware and software architecture must operate within the constraints of the following hardware bill of materials:

| Component | Specification | Cost (INR) |
|---|---|---|
| ESP32 Dev Board | Dual-core 240 MHz, 520 KB SRAM, 4 MB Flash, Wi-Fi + BLE | ₹550 |
| Load Cell + HX711 | 5 kg capacity, 24-bit ADC, 10/80 Hz selectable sample rate | ₹200 |
| Servo Motor (SG90) | 180° rotation, 1.8 kg·cm torque, PWM-controlled | ₹150 |
| OLED Display | 0.96" 128×64, SSD1306 controller, I2C interface | (included in dev board kit) |
| Buzzer | Piezoelectric, active type, 3.3V GPIO-driven | (included in dev board kit) |
| Power Modules | Dual buck converters: 5V→3.3V (logic), 5V (servo isolated rail) | ₹150 |
| Housing / PCB | 3D-printed enclosure; 4-layer PCB (prototype phase) | ₹800 |
| **Total** | | **~₹2,800** |

### GPIO Pin Allocation

| GPIO | Function | Protocol |
|---|---|---|
| GPIO 18 | HX711 SCK (Clock) | Bit-bang |
| GPIO 19 | HX711 DOUT (Data) | Bit-bang |
| GPIO 21 | OLED SDA | I2C |
| GPIO 22 | OLED SCL | I2C |
| GPIO 13 | Servo PWM | PWM (50 Hz) |
| GPIO 15 | Buzzer | Digital Out |
| GPIO 4 | Manual Override Button | Digital In (pull-up) |

---

## 7. Regulatory & Compliance Considerations

| Standard | Scope | Phase |
|---|---|---|
| **ISO 13485** | Quality management for medical devices | Production (Phase 3) |
| **IEC 60601-1** | General safety for medical electrical equipment | Production (Phase 3) |
| **IEC 62304** | Software lifecycle for medical devices | Engineering Prototype (Phase 2) |
| **CE / BIS marking** | Market-specific certification | Post-production |

> [!IMPORTANT]
> The current prototype (Phase 1) is intended for **research and demonstration only**. Clinical deployment requires full regulatory certification as outlined above.

---

## 8. Development Roadmap

| Phase | Milestone | Deliverables |
|---|---|---|
| **Phase 1: Rapid Prototype** | Proof of concept on breadboard | Functional sensor + servo + OLED + Wi-Fi demo; 3D-printed case |
| **Phase 2: Engineering Prototype** | Custom PCB with EMI shielding | 4-layer PCB; integrated power management; BLE provisioning; OTA updates |
| **Phase 3: Production Hardware** | Certified assembly | ISO 13485 compliance; injection-molded enclosure; clinical trial readiness |

### Recommended Upgrades for Clinical Deployment

| Upgrade | Purpose |
|---|---|
| Optical Drip Counter | Secondary flow verification (redundant sensing) |
| BLE Fallback Module | Local redundancy when Wi-Fi is unavailable |
| Hardware Watchdog IC | Automatic system reset on firmware hang |
| Li-ion Battery Backup | Uninterruptible power during mains outage |

---

## 9. Success Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| **Weight accuracy** | ±1 g after calibration | Bench test with calibrated weights |
| **False alarm rate** | < 1 per 24 hours | Clinical simulation over 7-day trial |
| **Detection-to-clamp latency** | < 2 seconds | Oscilloscope + logic analyzer |
| **Nurse satisfaction** | > 80% approval | Post-trial survey (Likert scale) |
| **System uptime** | > 99.5% over 30 days | Cloud telemetry uptime tracking |
| **Unit cost** | < ₹3,000 at scale | BOM audit |

---

## 10. Glossary

| Term | Definition |
|---|---|
| **ADC** | Analog-to-Digital Converter |
| **BLE** | Bluetooth Low Energy |
| **EMA** | Exponential Moving Average |
| **HAL** | Hardware Abstraction Layer |
| **HIL** | Hardware-in-the-Loop |
| **HX711** | 24-bit ADC IC designed for bridge sensors |
| **I2C** | Inter-Integrated Circuit (serial protocol) |
| **IV** | Intravenous |
| **MQTT** | Message Queuing Telemetry Transport |
| **NVS** | Non-Volatile Storage |
| **OTA** | Over-the-Air (firmware update) |
| **PCB** | Printed Circuit Board |
| **PWM** | Pulse Width Modulation |
| **SSD1306** | OLED display controller IC |

---

> **Next:** [Software Architecture →](architecture.md)
