# Drip-Sense — Troubleshooting Guide

> **Version:** 1.0  
> **Date:** 2026-02-19  
> **Audience:** Nursing staff, biomedical engineers, field technicians

---

## 1. Symptom-Based Diagnostic Table

### Quick Reference — Start Here

| Symptom | Likely Cause | Quick Fix | Section |
|---|---|---|---|
| OLED screen is blank | No power / display failure | Check USB cable & power adapter | [§2.1](#21-no-power--blank-screen) |
| Weight reads 0.0 g with bag attached | Calibration lost or HX711 fault | Recalibrate or check wiring | [§2.2](#22-incorrect-weight-reading) |
| Weight is drifting over time | Temperature change or unstable mount | Recalibrate; check mount stability | [§2.2](#22-incorrect-weight-reading) |
| Flow rate shows 0.0 mL/min | IV stopped, tube kinked, or stall detection | Check tube and roller clamp | [§2.3](#23-flow-rate-issues) |
| Buzzer sounds continuously | Emergency clamp triggered | Check OLED for reason; press override button | [§2.4](#24-false-alarms--buzzer-issues) |
| Servo does not clamp | Servo disconnected or angle misconfigured | Test via serial: `AT+SERVO_TEST=90` | [§2.5](#25-servo--clamp-problems) |
| Wi-Fi won't connect | Wrong credentials or signal too weak | Re-provision via BLE; check RSSI | [§2.6](#26-wi-fi-connectivity) |
| MQTT telemetry not reaching dashboard | Broker down or network firewall | Check broker status; verify port 8883 open | [§2.7](#27-mqtt--cloud-issues) |
| Device reboots repeatedly | Firmware crash or brownout | Check serial log for crash reason | [§2.8](#28-device-crashes--reboots) |
| OTA update fails | Network interruption or corrupt binary | Retry; if persistent, flash via USB | [§2.9](#29-ota-update-failures) |

---

## 2. Detailed Troubleshooting

### 2.1 No Power / Blank Screen

```
Check 1: USB cable connected?
   ├── YES → Check 2
   └── NO  → Connect USB-C cable to 5V ≥1A adapter
   
Check 2: Power LED on ESP32 board lit?
   ├── YES → Check 3
   └── NO  → Try different USB cable/adapter; check for bent pins
   
Check 3: Any text on OLED?
   ├── YES → Screen is working; check contrast settings
   └── NO  → OLED may be faulty
              → Connect serial, run AT+OLED_TEST
              → If test shows I2C error: check SDA/SCL wiring (GPIO 21/22)
              → If test passes but screen blank: replace OLED module
```

### 2.2 Incorrect Weight Reading

| Problem | Diagnosis | Solution |
|---|---|---|
| Always reads 0.0 g | Calibration data missing or corrupt | Run calibration procedure (hold button 3s) |
| Reads negative values | Tare offset is wrong | Re-tare with empty platform |
| Off by a constant amount | Scale factor inaccurate | Recalibrate with known weight |
| Fluctuating ±5 g rapidly | Mechanical vibration or loose wiring | Tighten mount; check HX711 connections |
| Slow drift over hours | Temperature-induced sensor drift | Recalibrate; consider environmental control |
| Reads a fixed large number | HX711 DOUT pin stuck | Check GPIO 19 wiring; replace HX711 if damaged |

**Diagnostic serial commands:**

```
> AT+HX711_RAW        # Show raw 24-bit ADC value
Raw: 8421903 (stable ✓)

> AT+HX711_TARE_INFO  # Show stored tare offset
Offset: 8421903, Samples: 20, StdDev: 12.4

> AT+HX711_SCALE_INFO # Show stored scale factor
Scale: 420.5 units/g, RefWeight: 500.0 g
```

### 2.3 Flow Rate Issues

| Problem | Diagnosis | Solution |
|---|---|---|
| Flow rate = 0 permanently | No weight change detected | Check IV tube is open; roller clamp released |
| Flow rate jumps erratically | Noisy sensor or vibration | Increase EMA alpha (`AT+EMA_ALPHA=0.15`) |
| Flow rate too low vs. actual | Fluid density misconfigured | Check `AT+FLUID_DENSITY` — should be ~1.0 for saline |
| Flow rate spikes on bag change | Sudden weight change | Expected behavior; ignore first 10s after bag change |

### 2.4 False Alarms / Buzzer Issues

| Problem | Cause | Solution |
|---|---|---|
| Continuous buzzer (no apparent reason) | Threshold too high for current bag size | Lower threshold: `AT+LOW_THRESHOLD=5` |
| Intermittent buzzer during normal operation | Vibration causing weight to dip below threshold | Increase debounce or reduce threshold |
| Buzzer too quiet | Volume not adjustable (hardware limit) | Replace with louder buzzer module |
| Buzzer doesn't sound on alarm | GPIO 15 fault or buzzer failure | Test: `AT+BUZZER_TEST` → if silent, check wiring |

**To silence the buzzer during an alarm:**
- Press the **Manual Override button** once → acknowledges alarm, releases clamp
- If the underlying condition persists (e.g., bag is still empty), alarm will re-trigger after 30 seconds

### 2.5 Servo / Clamp Problems

| Problem | Cause | Solution |
|---|---|---|
| Servo doesn't move at all | PWM signal not reaching servo | Check GPIO 13 wiring; `AT+SERVO_TEST=90` |
| Servo jitters/buzzes in clamped position | PWM signal still active after clamp | Normal for 2s after clamp; if persistent, check code |
| Clamp doesn't fully occlude tube | Angle too low for tube diameter | Increase: `AT+SERVO_CLAMP_ANGLE=100` |
| Clamp is too tight / crushes tube | Angle too high | Decrease: `AT+SERVO_CLAMP_ANGLE=80` |
| Servo moves but tube doesn't clamp | Tube adapter misaligned | Reposition tube in clamp channel |

### 2.6 Wi-Fi Connectivity

```
Check 1: OLED shows WiFi icon?
   ├── ✕ (no bars) → Wi-Fi not connected
   │   ├── Check 2: Were credentials provisioned?
   │   │   ├── NO  → Provision via BLE app or serial (AT+WIFI_SSID=..., AT+WIFI_PASS=...)
   │   │   └── YES → Check 3
   │   └── Check 3: Is the AP in range?
   │       ├── Run: AT+WIFI_SCAN → verify SSID appears in scan results
   │       ├── RSSI > -75 dBm → Credentials wrong; re-enter password
   │       └── RSSI < -75 dBm → Move device closer to AP or add extender
   └── 📶 (bars) → Connected but other issues
       └── Check MQTT section below
```

**Serial commands for Wi-Fi debug:**

```
> AT+WIFI_STATUS
SSID: HospitalNet5G
IP: 192.168.1.105
RSSI: -52 dBm
State: CONNECTED

> AT+WIFI_SCAN
1: HospitalNet5G (-48 dBm, WPA2)
2: Guest_WiFi (-72 dBm, Open)
3: IoT_Devices (-55 dBm, WPA2)

> AT+WIFI_RECONNECT
Disconnecting... Connecting... OK (3.2s)
```

### 2.7 MQTT / Cloud Issues

| Problem | Diagnosis | Solution |
|---|---|---|
| Telemetry not appearing on dashboard | MQTT not publishing | Check `AT+MQTT_STATUS` |
| MQTT status: DISCONNECTED | Broker unreachable or auth failure | Verify broker URL, port 8883, credentials |
| MQTT status: CONNECTED but no data on dashboard | Topic mismatch or dashboard filter | Check `AT+MQTT_TOPIC` matches dashboard subscription |
| Data appears delayed by > 30s | Network congestion or QoS issues | Check Wi-Fi RSSI; reduce publish interval |

```
> AT+MQTT_STATUS
Broker: mqtt.dripsense.io:8883
State: CONNECTED
Last publish: 2s ago
Publish count: 4821
Errors: 0

> AT+MQTT_TEST
Publishing test message... OK (latency: 120ms)
```

### 2.8 Device Crashes / Reboots

**How to read crash information:**

1. Connect serial at 115200 baud
2. Wait for crash or trigger `AT+CRASH_LOG`
3. Look for the **Guru Meditation Error** output:

```
Guru Meditation Error: Core  1 panic'ed (LoadProhibited). Exception was unhandled.
Core 1 register dump:
PC      : 0x400d1234  PS      : 0x00060130  A0      : 0x800d5678
...
Backtrace: 0x400d1234:0x3ffb1234 0x400d5678:0x3ffb5678
```

4. Decode the backtrace:

```bash
xtensa-esp32-elf-addr2line -e .pio/build/esp32dev/firmware.elf 0x400d1234
```

**Common crash causes:**

| Crash Type | Typical Cause | Fix |
|---|---|---|
| `LoadProhibited` | Null pointer dereference | Check sensor init; add null guards |
| `StoreProhibited` | Writing to invalid memory | Check buffer overflows |
| `InstrFetchProhibited` | Stack overflow | Increase task stack size |
| `Brownout detector triggered` | Insufficient power supply | Use 5V ≥ 2A adapter; add bulk cap |
| `Task watchdog got triggered` | Task blocked for > 5s | Check for infinite loops or blocking I/O |
| Repeated reboot loop | OTA firmware is crashing | Auto-rollback should activate; if not, USB reflash |

### 2.9 OTA Update Failures

| Problem | Cause | Solution |
|---|---|---|
| OTA download stalls at X% | Network interruption | Retry; ensure stable Wi-Fi |
| "SHA-256 mismatch" error | Corrupted download | Retry; if persistent, check server binary integrity |
| Device boots old firmware after OTA | OTA partition not set as boot | Check `AT+OTA_PARTITION_INFO`; retry update |
| Device won't boot after OTA | New firmware has fatal bug | Wait for auto-rollback (3 crash cycles); or USB reflash |

---

## 3. Serial Debug Command Reference

| Command | Description | Example Output |
|---|---|---|
| `AT+HELP` | List all available AT commands | Command list |
| `AT+VERSION` | Show firmware version and build info | `v1.2.0, built Feb 19 2026` |
| `AT+STATUS` | Show current system state | `State: MONITORING, Uptime: 86400s` |
| `AT+HX711_RAW` | Read raw ADC value | `Raw: 8421903` |
| `AT+WEIGHT` | Read calibrated, filtered weight | `Weight: 487.3 g` |
| `AT+FLOW` | Read current flow rate | `Flow: 2.1 mL/min` |
| `AT+SERVO_TEST={angle}` | Move servo to specified angle | `Servo moved to 90°` |
| `AT+BUZZER_TEST` | Sound buzzer for 500 ms | `Buzzer: ON... OFF` |
| `AT+OLED_TEST` | Display test pattern on OLED | `OLED test pattern displayed` |
| `AT+WIFI_STATUS` | Show Wi-Fi connection details | `SSID: X, IP: Y, RSSI: Z` |
| `AT+MQTT_STATUS` | Show MQTT connection details | `Broker: X, State: CONNECTED` |
| `AT+HEAP` | Show free heap memory | `Free: 142560 bytes, Min: 98304 bytes` |
| `AT+TASKS` | Show FreeRTOS task stack usage | Task list with high-water marks |
| `AT+NVS_DUMP` | Dump all NVS key-value pairs | Calibration + config data |
| `AT+CRASH_LOG` | Show last crash backtrace | Backtrace addresses |
| `AT+FACTORY_RESET` | Erase NVS and reboot | Confirmation prompt |
| `AT+REBOOT` | Soft restart | Device reboots |

---

## 4. Error Codes (OLED Display)

| Code | Meaning | Action |
|---|---|---|
| `E01` | HX711 communication failure | Check load cell wiring (GPIO 18/19) |
| `E02` | OLED I2C error | Check SDA/SCL (GPIO 21/22); verify address 0x3C |
| `E03` | Servo PWM fault | Check GPIO 13; test with `AT+SERVO_TEST` |
| `E04` | NVS read/write failure | Factory reset; if persistent, flash may be failing |
| `E05` | Wi-Fi authentication failure | Re-enter credentials; check WPA2 compatibility |
| `E06` | MQTT connection refused | Verify broker URL, port, and device credentials |
| `E07` | OTA verification failed | Retry download; verify server binary |
| `E08` | Watchdog reset occurred | Check serial log for crash cause |
| `E09` | Heap critically low (< 20 KB) | Reboot; if recurring, report firmware bug |
| `E10` | Calibration data invalid | Recalibrate the device |

---

## 5. Escalation Procedure

```
Level 1: Nursing Staff
   └── Follow symptom table (§1)
   └── Press override button to clear alarms
   └── If unresolved → call Biomedical Engineering

Level 2: Biomedical Engineer
   └── Connect serial, run AT+STATUS and AT+CRASH_LOG
   └── Attempt recalibration or Wi-Fi re-provisioning
   └── If hardware fault → swap unit from spares inventory
   └── If firmware bug → collect serial logs, escalate

Level 3: Firmware Engineering Team
   └── Analyze crash logs and core dumps
   └── Reproduce issue on test bench
   └── Issue firmware patch via OTA
   └── Update troubleshooting guide if new issue pattern found
```

---

> **Previous:** [← Firmware Deployment](deployment.md)  
> **Next:** [Project Overview (README) →](README.md)
