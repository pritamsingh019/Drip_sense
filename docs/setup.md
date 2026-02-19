# Drip-Sense — Setup Guide

> **Version:** 1.0  
> **Date:** 2026-02-19  
> **Audience:** Firmware developers, biomedical engineers, hospital IT

---

## Phase 1: Development Environment

### 1.1 System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| **Operating System** | Windows 10 / macOS 12 / Ubuntu 20.04 | Latest LTS |
| **Python** | 3.8 | 3.10+ |
| **RAM** | 4 GB | 8 GB |
| **Disk Space** | 2 GB (toolchain + libs) | 5 GB |
| **USB Port** | USB 2.0 | USB 3.0 |

### 1.2 Install PlatformIO (Recommended IDE)

**Option A: VSCode Extension (Recommended)**

1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Open Extensions panel (`Ctrl/Cmd + Shift + X`)
3. Search for "PlatformIO IDE"
4. Click **Install** — wait for toolchain download (~500 MB)
5. Restart VSCode

**Option B: CLI Only**

```bash
# Install PlatformIO Core via pip
pip install platformio

# Verify installation
pio --version
# Expected: PlatformIO Core, version 6.x.x
```

### 1.3 Install USB-UART Driver

The ESP32 dev board uses a CP2102 or CH340 USB-UART bridge.

| Chip | Driver Download |
|---|---|
| **CP2102** (most common) | [Silicon Labs CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) |
| **CH340** (budget boards) | [WCH CH340](http://www.wch.cn/download/CH341SER_MAC_ZIP.html) |

**Verify driver is installed:**

```bash
# macOS
ls /dev/cu.*
# Should show: /dev/cu.SLAB_USBtoUART or /dev/cu.wchusbserial*

# Linux
ls /dev/ttyUSB*
# Should show: /dev/ttyUSB0

# Windows
# Check Device Manager → Ports (COM & LPT) → Silicon Labs CP210x (COM3)
```

### 1.4 Clone the Repository

```bash
git clone https://github.com/your-org/drip-sense.git
cd drip-sense
```

### 1.5 Install Dependencies

PlatformIO auto-installs all dependencies on first build, but you can pre-fetch:

```bash
pio pkg install
```

**Library dependencies (auto-resolved):**

| Library | Version | Purpose |
|---|---|---|
| `HX711` by Bogdan Necula | ^0.7.5 | Load cell ADC communication |
| `Adafruit SSD1306` | ^2.5.7 | OLED display driver |
| `Adafruit GFX Library` | ^1.11.5 | Graphics primitives |
| `ESP32Servo` | ^1.1.1 | Servo PWM control |
| `PubSubClient` | ^2.8 | MQTT client |
| `ArduinoJson` | ^6.21.0 | JSON serialization |

### 1.6 Verify Build

```bash
pio run -e esp32dev
```

**Expected output:**

```
Processing esp32dev (platform: espressif32; board: esp32dev; framework: arduino)
...
Building .pio/build/esp32dev/firmware.bin
============= [SUCCESS] Took 45.32 seconds =============
```

> [!TIP]
> If `pio run` fails with "No module named...", ensure PlatformIO is using its own Python virtual environment, not your system Python.

### 1.7 Arduino IDE Setup (Alternative)

If using Arduino IDE instead of PlatformIO:

1. Open **File → Preferences**
2. Add to *Additional Board Manager URLs*:
   ```
   https://dl.espressif.com/dl/package_esp32_index.json
   ```
3. **Tools → Board → Board Manager** → Search "ESP32" → Install "ESP32 by Espressif Systems" v2.x
4. **Tools → Board** → Select **ESP32 Dev Module**
5. **Tools → Port** → Select your USB port
6. **Sketch → Include Library → Manage Libraries** → Install:
   - `HX711`
   - `Adafruit SSD1306`
   - `Adafruit GFX Library`
   - `ESP32Servo`
   - `PubSubClient`
   - `ArduinoJson`
7. Open `src/main.cpp` and compile with `Ctrl/Cmd + R`

---

## Phase 2: Hardware Assembly

### 2.1 Components Checklist

Before starting, verify you have all components:

| # | Component | Qty | Verified |
|---|---|---|---|
| 1 | ESP32 Dev Board (30-pin) | 1 | ☐ |
| 2 | Load Cell (5 kg) | 1 | ☐ |
| 3 | HX711 ADC Module | 1 | ☐ |
| 4 | SG90 Servo Motor | 1 | ☐ |
| 5 | 0.96" OLED (SSD1306, I2C) | 1 | ☐ |
| 6 | Piezo Buzzer (active, 3.3V) | 1 | ☐ |
| 7 | Push Button (momentary) | 1 | ☐ |
| 8 | 10 kΩ Resistor (pull-up) | 1 | ☐ |
| 9 | Breadboard (830 points) | 1 | ☐ |
| 10 | Jumper wires (M-M, M-F) | 20+ | ☐ |
| 11 | USB-C cable (data-capable) | 1 | ☐ |
| 12 | 5V USB power adapter (≥2A) | 1 | ☐ |
| 13 | 470 µF electrolytic capacitor (5V) | 1 | ☐ |

### 2.2 Wiring Diagram

```
                         ┌──────────────────┐
                         │     ESP32 Dev     │
                         │                  │
     HX711 ────────────  │ GPIO 18 ── SCK   │
     Module              │ GPIO 19 ── DOUT  │
     (VCC → 3.3V,       │                  │
      GND → GND)        │                  │
                         │ GPIO 21 ── SDA ──│── OLED SDA
                         │ GPIO 22 ── SCL ──│── OLED SCL
                         │                  │   (OLED VCC → 3.3V, GND → GND)
                         │                  │
                         │ GPIO 13 ── PWM ──│── Servo Signal (Orange)
                         │                  │   (Servo VCC → 5V isolated, GND → GND)
                         │                  │
                         │ GPIO 15 ── OUT ──│── Buzzer (+)
                         │                  │   (Buzzer GND → GND)
                         │                  │
                         │ GPIO 4 ─── IN  ──│── Button ── 10kΩ ── 3.3V
                         │                  │   (Button other leg → GND)
                         │                  │
                         │ 3V3 ─────────────│── HX711 VCC, OLED VCC
                         │ 5V ──────────────│── Servo VCC (through 470µF cap)
                         │ GND ─────────────│── Common ground for all
                         └──────────────────┘
```

### 2.3 Step-by-Step Wiring Instructions

#### Step 1: Power Rails

1. Connect ESP32 `3V3` pin to breadboard `+` rail (red) — this is the **logic power rail**
2. Connect ESP32 `GND` to breadboard `−` rail (blue) — this is the **common ground**
3. Connect ESP32 `5V` (VIN) to a **separate** breadboard section — this is the **servo power rail**
4. Place 470 µF capacitor across the servo power rail (`+` to 5V, `−` to GND)

> [!WARNING]
> The 470 µF capacitor is essential. Without it, servo actuation causes voltage dips that can brownout the ESP32 or inject noise into the HX711 readings.

#### Step 2: HX711 ADC Module

| HX711 Pin | Connect To |
|---|---|
| VCC | 3.3V rail |
| GND | GND rail |
| SCK | ESP32 GPIO 18 |
| DOUT | ESP32 GPIO 19 |

Load cell wires to HX711:
| Load Cell Wire | HX711 Terminal |
|---|---|
| Red | E+ |
| Black | E− |
| White | A− |
| Green | A+ |

> [!NOTE]
> Wire colors vary by manufacturer. If readings are inverted (negative when weight applied), swap A+ and A−.

#### Step 3: OLED Display

| OLED Pin | Connect To |
|---|---|
| VCC | 3.3V rail |
| GND | GND rail |
| SDA | ESP32 GPIO 21 |
| SCL | ESP32 GPIO 22 |

#### Step 4: Servo Motor

| Servo Wire | Connect To |
|---|---|
| Orange (signal) | ESP32 GPIO 13 |
| Red (power) | 5V servo rail (NOT the 3.3V rail) |
| Brown (ground) | GND rail |

#### Step 5: Buzzer

| Buzzer Pin | Connect To |
|---|---|
| `+` (longer leg) | ESP32 GPIO 15 |
| `−` (shorter leg) | GND rail |

#### Step 6: Override Button

1. One leg of button → ESP32 GPIO 4
2. Same leg → 10 kΩ resistor → 3.3V (pull-up)
3. Other leg of button → GND

> [!TIP]
> The ESP32 has internal pull-ups, but an external 10 kΩ is more reliable for the debounce circuit. If you prefer, you can skip the external resistor and enable the internal pull-up in firmware: `pinMode(PIN_BUTTON, INPUT_PULLUP)`.

### 2.4 Verification After Wiring

| Test | Command | Expected Result |
|---|---|---|
| **ESP32 boots** | Connect USB, open serial monitor (115200 baud) | Boot messages appear |
| **HX711 responds** | Flash firmware, check serial for `HX711: Ready` | Raw ADC values printed |
| **OLED works** | Check for splash screen | Logo + version displayed |
| **Servo moves** | `AT+SERVO_TEST=90` via serial | Servo rotates to 90° |
| **Buzzer sounds** | `AT+BUZZER_TEST` via serial | 500 ms beep |
| **Button works** | Press button, check serial for `Button: PRESSED` | Event logged |

---

## Phase 3: First Flash & Boot

### 3.1 Upload Firmware

```bash
# Build and flash in one step
pio run -e esp32dev -t upload

# If auto-detect fails, specify port:
# macOS:   pio run -e esp32dev -t upload --upload-port /dev/cu.SLAB_USBtoUART
# Linux:   pio run -e esp32dev -t upload --upload-port /dev/ttyUSB0
# Windows: pio run -e esp32dev -t upload --upload-port COM3
```

### 3.2 Open Serial Monitor

```bash
pio device monitor -b 115200
```

**Expected boot output:**

```
[BOOT] Drip-Sense v1.0.0
[BOOT] Build: Feb 19 2026, 09:30:00
[HAL ] GPIO initialized
[HAL ] I2C bus started (400 kHz)
[HAL ] PWM channel 0 configured (50 Hz)
[HAL ] HX711 powered up, waiting for stabilization...
[NVS ] Loaded calibration: offset=0, scale=1.0 (UNCALIBRATED)
[NVS ] Wi-Fi: not configured
[NVS ] Safety: low=10.0g, clamp=90°, open=0°
[OLED] Splash screen displayed
[TASK] task_sensor_read started on Core 1 (4096 bytes)
[TASK] task_safety_check started on Core 1 (2048 bytes)
[TASK] task_oled_update started on Core 0 (4096 bytes)
[TASK] task_mqtt_publish started on Core 0 (8192 bytes)
[SYS ] State: IDLE → MONITORING
[WARN] Device is UNCALIBRATED — hold button 3s to calibrate
```

### 3.3 Troubleshooting First Boot

| Problem | Solution |
|---|---|
| No serial output | Check baud rate is 115200; try different USB cable |
| `A fatal error occurred: Failed to connect to ESP32` | Hold BOOT → press EN → release BOOT (enter flash mode) |
| `Brownout detector was triggered` | Use a powered USB hub or ≥2A adapter |
| `E01: HX711 communication failure` | Check GPIO 18/19 wiring; ensure HX711 VCC is 3.3V |
| `E02: OLED I2C error` | Check GPIO 21/22 wiring; verify OLED address is 0x3C |

---

## Phase 4: Wi-Fi & Cloud Setup

### 4.1 Wi-Fi Provisioning

**Option A: Serial (Quick)**

```
> AT+WIFI_SSID=YourNetworkName
OK
> AT+WIFI_PASS=YourPassword
OK
> AT+WIFI_CONNECT
Connecting... OK (3.2s)
IP: 192.168.1.105
RSSI: -48 dBm
> AT+WIFI_SAVE
Credentials saved to NVS
```

**Option B: BLE Companion App**

1. Install the ESP BLE Provisioning app ([Android](https://play.google.com/store/apps/details?id=com.espressif.provble) / [iOS](https://apps.apple.com/app/esp-ble-provisioning/id1473590141))
2. Power on device (enters BLE mode if no Wi-Fi configured)
3. App → Scan → Select `DRIPSENSE-XXXX`
4. Enter BLE PIN: `123456`
5. Select Wi-Fi network → Enter password
6. Wait for connection confirmation

### 4.2 MQTT Broker Setup

**Option A: Cloud Broker (Production)**

```
> AT+MQTT_BROKER=mqtt.dripsense.io
OK
> AT+MQTT_PORT=8883
OK
> AT+MQTT_USER=DS-ESP32-001
OK
> AT+MQTT_PASS=your_device_token
OK
> AT+MQTT_SAVE
MQTT config saved to NVS
```

**Option B: Local Broker (Development)**

```bash
# Install Mosquitto on your dev machine
# macOS:
brew install mosquitto

# Linux:
sudo apt install mosquitto mosquitto-clients

# Start broker
mosquitto -v

# Configure device to use local broker
> AT+MQTT_BROKER=192.168.1.100
> AT+MQTT_PORT=1883
> AT+MQTT_SAVE
```

**Verify MQTT is working:**

```bash
# In a separate terminal, subscribe to device telemetry
mosquitto_sub -h localhost -t "dripsense/+/telemetry" -v

# You should see JSON payloads every 5 seconds
```

### 4.3 Cloud Dashboard Setup

1. Deploy the dashboard application (see API spec docs)
2. Register the device via REST API:
   ```bash
   curl -X POST https://api.dripsense.io/v1/devices \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"device_id": "DS-ESP32-001", "name": "ICU Bed 3", "ward": "ICU-A"}'
   ```
3. Open dashboard → device should appear with live telemetry

---

## Phase 5: Calibration

### 5.1 Prepare for Calibration

1. Place device on a **flat, stable surface** (not on the IV pole yet)
2. Remove all load from the platform
3. Have the 500 g calibration weight ready

### 5.2 Run Calibration

1. **Hold the override button for 3 seconds** → OLED shows "CALIBRATION MODE"
2. **Step 1 (Tare):** Ensure platform is empty → press button → wait 3s → "TARE COMPLETE ✓"
3. **Step 2 (Span):** Place 500 g weight on center → press button → wait 3s → "CALIBRATION DONE"
4. **Verify:** OLED shows measured weight — should read `499.5–500.5 g`
5. Remove weight → should read `0.0 ±1.0 g`

### 5.3 Verify with Different Weight

Place a different weight (e.g., 200 g) — reading should be within ±1 g.

**Via serial:**

```
> AT+WEIGHT
Weight: 199.8 g ✓
```

### 5.4 Save & Confirm

Calibration is auto-saved to NVS. Confirm persistence:

```
> AT+REBOOT
...
[NVS ] Loaded calibration: offset=8421903, scale=420.5 (CALIBRATED ✓)
```

---

## Phase 6: Deployment on IV Pole

### 6.1 Mount the Device

1. Attach Drip-Sense to IV pole using the integrated clamp (below drip chamber)
2. Route IV bag's weight through the load cell platform
3. Thread IV tube through the servo clamp channel

### 6.2 Verify After Mounting

```
> AT+WEIGHT
Weight: 1024.5 g (full 1L saline bag)

> AT+FLOW
Flow: 2.3 mL/min

> AT+STATUS
State: MONITORING
Uptime: 45s
Wi-Fi: CONNECTED (-52 dBm)
MQTT: CONNECTED
```

### 6.3 Post-Deployment Checklist

| Check | Method | Expected |
|---|---|---|
| OLED shows correct weight | Visual | Weight of bag + container |
| Flow rate updating | Visual (OLED) | Non-zero if valve is open |
| Wi-Fi connected | OLED icon + `AT+WIFI_STATUS` | 📶 bars showing |
| Telemetry reaching cloud | Dashboard | Data points updating |
| Alarm works | Remove weight below threshold | Buzzer sounds; servo clamps |
| Manual override works | Press button during alarm | Servo releases |

---

## Setup Complete ✓

Your Drip-Sense device is now:
- ✅ Firmware flashed and running
- ✅ Wi-Fi connected to hospital network
- ✅ MQTT publishing to cloud broker
- ✅ Load cell calibrated (±1 g accuracy)
- ✅ Mounted on IV pole with clamp ready
- ✅ Monitoring active

**Next steps:**
- [Calibration deep-dive →](calibration.md)
- [Troubleshooting →](troubleshooting.md)
- [Full Project Guide →](guide.md)

---

> **See also:** [Deployment Guide](deployment.md) for OTA updates, build variants, and release management
