# 💧 Drip-Sense

### Autonomous IV Drip Management System

[![Firmware](https://img.shields.io/badge/Firmware-ESP32-blue?logo=espressif)](https://www.espressif.com/)
[![Platform](https://img.shields.io/badge/Platform-PlatformIO-orange?logo=platformio)](https://platformio.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Prototype-yellow)]()
[![BOM Cost](https://img.shields.io/badge/BOM-₹2,800_INR-brightgreen)]()

---

## Overview

**Drip-Sense** is a low-cost, ESP32-based medical IoT device that transforms a standard IV stand into an intelligent, self-monitoring infusion system. It continuously measures IV bag weight, computes real-time flow rate, detects anomalies (low fluid, free-flow, air-in-line), and **automatically clamps the IV tube** when a safety threshold is breached.

### Key Features

- ⚖️ **Real-time weight monitoring** — Load cell + HX711 24-bit ADC at 10 Hz
- 💧 **Flow rate computation** — mL/min with EMA/Kalman filtering
- 🛑 **Auto-cutoff** — Servo clamps IV tube within 2 seconds on alarm
- 📺 **OLED dashboard** — 128×64 display showing weight, flow rate, ETA
- 🔊 **Audible alerts** — Distinct buzzer patterns for each alarm type
- 📡 **IoT telemetry** — MQTT over Wi-Fi/TLS to cloud dashboard
- 📲 **BLE provisioning** — Phone-based Wi-Fi setup
- 🔄 **OTA updates** — Remote firmware deployment with auto-rollback

---

## Hardware

| Component | Specification | GPIO |
|---|---|---|
| **ESP32 Dev Board** | Dual-core 240 MHz, 520 KB SRAM, Wi-Fi + BLE | — |
| **Load Cell + HX711** | 5 kg, 24-bit ADC | SCK: 18, DOUT: 19 |
| **Servo Motor (SG90)** | 180°, 1.8 kg·cm torque | PWM: 13 |
| **OLED Display** | 0.96" 128×64 SSD1306 | SDA: 21, SCL: 22 |
| **Buzzer** | Piezoelectric, active | GPIO: 15 |
| **Override Button** | Momentary push, pull-up | GPIO: 4 |

**Total BOM cost: ~₹2,800 INR** (~$33 USD)

---

## Quick Start

### 1. Clone & Build

```bash
git clone https://github.com/your-org/drip-sense.git
cd drip-sense
pio run -e esp32dev
```

### 2. Flash

```bash
pio run -e esp32dev -t upload
pio device monitor -b 115200
```

### 3. Configure Wi-Fi

Use the BLE companion app or serial commands:
```
AT+WIFI_SSID=YourNetwork
AT+WIFI_PASS=YourPassword
AT+WIFI_CONNECT
```

### 4. Calibrate

Hold the **override button** for 3 seconds, then follow the OLED prompts to perform tare and known-weight calibration.

### 5. Deploy

Mount on IV pole, route tube through servo clamp, hang IV bag — monitoring starts automatically.

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    APPLICATION                       │
│   Monitor Engine │ Safety Ctrl │ UI Mgr │ Telemetry │
├─────────────────────────────────────────────────────┤
│                    MIDDLEWARE                         │
│   Sensor Fusion │ State Machine │ Event Bus │ Config │
├─────────────────────────────────────────────────────┤
│                  HARDWARE ABSTRACTION                │
│   HX711 Driver │ SSD1306 │ Servo PWM │ Buzzer │ Net │
├─────────────────────────────────────────────────────┤
│                    HARDWARE                          │
│   Load Cell │ OLED │ SG90 Servo │ Piezo │ ESP32 SoC │
└─────────────────────────────────────────────────────┘
```

---

## Documentation

| Document | Description |
|---|---|
| [Product Requirements (PRD)](docs/prd.md) | Problem statement, user personas, functional requirements, success metrics |
| [Software Architecture](docs/architecture.md) | Layered design, dual-core task allocation, data flow, memory map |
| [Firmware Design](docs/firmware_design.md) | Boot sequence, FreeRTOS tasks, HAL drivers, power management, OTA |
| [Core Algorithms](docs/algorithms.md) | EMA/Kalman filters, flow rate calculation, anomaly detection |
| [Cloud API & Data Format](docs/api_spec.md) | MQTT topics, JSON schemas, REST endpoints, authentication |
| [Calibration & Setup](docs/calibration.md) | Physical mounting, Wi-Fi provisioning, load cell calibration |
| [Testing & Validation](docs/testing.md) | Unit tests, integration tests, HIL testing, safety validation |
| [Firmware Deployment](docs/deployment.md) | Build setup, serial flash, OTA updates, version management |
| [Troubleshooting](docs/troubleshooting.md) | Symptom-based diagnostics, serial debug commands, error codes |

---

## Development Roadmap

| Phase | Status | Milestone |
|---|---|---|
| **Phase 1: Rapid Prototype** | 🟡 In Progress | Breadboard PoC, 3D-printed case |
| **Phase 2: Engineering Prototype** | ⬜ Planned | Custom 4-layer PCB, EMI shielding |
| **Phase 3: Production Hardware** | ⬜ Planned | ISO 13485 certified assembly |

### Planned Upgrades

- 🔬 Optical drip counter (secondary flow verification)
- 📶 BLE fallback for Wi-Fi dead zones
- 🐕‍🦺 Hardware watchdog IC for system reset safety
- 🔋 Li-ion battery backup for uninterruptible operation

---

## Project Structure

```
drip-sense/
├── src/
│   ├── main.cpp              # Entry point
│   ├── config.h              # Pin definitions & constants
│   ├── hal/                  # Hardware Abstraction Layer
│   ├── middleware/            # Business logic & services
│   ├── app/                  # Application orchestration
│   └── net/                  # Network services
├── include/
│   └── version.h             # Firmware version
├── test/                     # Unit & integration tests
├── docs/                     # Documentation suite (this index)
├── data/                     # SPIFFS data files
├── platformio.ini            # Build configuration
└── partitions.csv            # Flash partition table
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/optical-drip-counter`)
3. Write tests for new functionality
4. Ensure all tests pass (`pio test -e native`)
5. Submit a pull request with a clear description

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **Espressif Systems** — ESP32 platform and ESP-IDF framework
- **ThrowTheSwitch** — Unity test framework for embedded C
- **Adafruit** — SSD1306 and GFX libraries
- **Robu.in / Robocraze** — Component sourcing (India)

---

> ⚠️ **Disclaimer:** Drip-Sense is currently a **research prototype**. It is not certified for clinical use. Deployment in a medical setting requires full regulatory certification (ISO 13485, IEC 60601-1).
