# Drip-Sense — Calibration & Setup Guide

> **Version:** 1.0  
> **Date:** 2026-02-19  
> **Audience:** Biomedical engineers, nursing staff, hospital IT

---

## 1. What's in the Box

| Item | Qty | Description |
|---|---|---|
| Drip-Sense unit | 1 | Pre-assembled with ESP32, load cell, servo, OLED |
| USB-C cable | 1 | Power + serial debug (1.5 m) |
| IV tube clamp adapter | 1 | 3D-printed bracket for servo-to-tube coupling |
| Calibration weight | 1 | 500 g reference weight (NIST-traceable, ±0.1 g) |
| Quick-start card | 1 | Laminated A5 reference |

---

## 2. Physical Setup

### 2.1 Mounting the Unit

```
    IV Pole
      │
      ├── Hook (existing)
      │     └── IV Bag
      │
      ├── Drip-Sense Unit ◄── Mount here, BELOW the drip chamber
      │     ├── Load cell platform (faces UP — bag hangs from hook through platform)
      │     ├── Servo clamp arm (wraps around IV tube)
      │     └── USB-C port (faces DOWN for cable routing)
      │
      └── Roller clamp (below the unit)
```

**Mounting rules:**
1. Attach the unit to the IV pole using the integrated clamp (ships pre-installed)
2. Route the IV bag's weight through the **load cell platform** — the bag hangs from a hook that rests on the platform
3. Position the **servo clamp arm** around the IV tube, **above** the roller clamp
4. Ensure the tube is seated firmly in the clamp channel — do not pinch or kink
5. Connect USB-C for power (5V, ≥1A adapter required)

### 2.2 IV Tube Routing Through Servo Clamp

```
    IV Tube (from drip chamber)
         │
         ▼
    ┌──────────────┐
    │  Servo Arm   │  ← Tube passes through the gap
    │   ┌────┐     │     between the fixed jaw and the
    │   │TUBE│     │     movable servo arm
    │   └────┘     │
    │  Fixed Jaw   │
    └──────────────┘
         │
         ▼
    Roller Clamp (manual backup)
         │
         ▼
    Patient
```

> [!WARNING]
> Always keep the manual roller clamp in place as a **backup**. Drip-Sense auto-clamp is a secondary safety layer, not a replacement for the roller clamp.

---

## 3. First-Time Power-On

### 3.1 Boot Sequence (What You'll See)

| Time | OLED Display | Buzzer |
|---|---|---|
| 0–1 s | Drip-Sense logo + firmware version | — |
| 1–2 s | "Initializing sensors..." | — |
| 2–3 s | "Wi-Fi: Connecting..." | — |
| 3–6 s | "Wi-Fi: Connected ✓" or "Wi-Fi: Not configured" | Single beep (if connected) |
| 6+ s | Main monitoring screen (showing "UNCALIBRATED") | — |

### 3.2 LED / OLED Status Indicators

| OLED Icon | Meaning |
|---|---|
| 📶 (filled bars) | Wi-Fi connected (RSSI > -60 dBm) |
| 📶 (1 bar) | Wi-Fi weak (RSSI < -75 dBm) |
| ✕ (no bars) | Wi-Fi disconnected |
| ⚖️ | Calibration mode active |
| ⚠️ | Alert / warning active |
| 🔒 | Tube clamped |

---

## 4. Wi-Fi Provisioning

### 4.1 BLE Provisioning (Recommended)

1. Install the **Drip-Sense Companion App** (Android/iOS) or use the ESP BLE Provisioning app
2. Power on the device — it automatically enters BLE provisioning mode if no Wi-Fi credentials are stored
3. On your phone:
   - Open the companion app
   - Tap "Scan for Devices"
   - Select `DRIPSENSE-XXXX` (last 4 hex of MAC address)
   - Enter BLE pairing PIN: `123456` (default; change in production)
4. Select your hospital Wi-Fi network from the scanned list
5. Enter the Wi-Fi password
6. The device will attempt to connect — OLED will show result
7. On success, credentials are saved to NVS and persist across reboots

### 4.2 Serial Provisioning (Alternative)

Connect via USB serial at **115200 baud** and send AT-style commands:

```
> AT+WIFI_SSID=HospitalNet5G
OK
> AT+WIFI_PASS=SecurePassword123
OK
> AT+WIFI_CONNECT
Connecting... OK
IP: 192.168.1.105
> AT+WIFI_SAVE
Credentials saved to NVS
```

### 4.3 MQTT Broker Configuration

```
> AT+MQTT_BROKER=mqtt.dripsense.io
OK
> AT+MQTT_PORT=8883
OK
> AT+MQTT_USER=DS-ESP32-001
OK
> AT+MQTT_PASS=device_token_here
OK
> AT+MQTT_SAVE
MQTT config saved to NVS
```

---

## 5. Load Cell Calibration

> [!IMPORTANT]
> Calibration must be performed on a **stable, level surface** with no vibration. Do not calibrate while the unit is mounted on the IV pole.

### 5.1 Step-by-Step Procedure

#### Step 1: Enter Calibration Mode

Press and hold the **Manual Override button** for 3 seconds until the OLED shows:

```
╔══════════════════════╗
║   CALIBRATION MODE   ║
║                      ║
║  Step 1: Remove all  ║
║  load from platform  ║
║                      ║
║  Press BTN to start  ║
╚══════════════════════╝
```

#### Step 2: Tare (Zero-Point)

1. Ensure the load cell platform is completely empty
2. Press the button once
3. The device reads 20 samples and computes the zero offset
4. OLED shows:

```
╔══════════════════════╗
║   TARE COMPLETE ✓    ║
║                      ║
║  Offset: 8421903     ║
║  StdDev: 12.4 units  ║
║                      ║
║  Step 2: Place 500g  ║
║  weight on platform  ║
╚══════════════════════╝
```

> [!CAUTION]
> If StdDev > 50 units, the surface is unstable. The device will show "UNSTABLE — RETRY" and refuse to proceed.

#### Step 3: Span (Known Weight)

1. Place the 500 g calibration weight on the center of the platform
2. Wait 3 seconds for reading to stabilize
3. Press the button once
4. The device reads 20 samples and computes the scale factor
5. OLED shows:

```
╔══════════════════════╗
║   CALIBRATION DONE   ║
║                      ║
║  Scale: 420.5 u/g    ║
║  Verify: 499.8 g     ║
║                      ║
║  Accuracy: ±0.2 g ✓  ║
║  Saved to NVS        ║
╚══════════════════════╝
```

6. Double beep confirms success
7. Remove calibration weight
8. Device returns to monitoring mode

### 5.2 Verification

After calibration, verify accuracy with a different known weight (e.g., 200 g). The displayed weight should be within ±1 g.

### 5.3 When to Recalibrate

| Trigger | Reason |
|---|---|
| Every 30 days | Preventive maintenance |
| After moving the unit | Mounting orientation affects zero-point |
| After firmware update | Scale factor may change with ADC driver updates |
| If displayed weight drifts > 2 g | Sensor drift over temperature cycles |

---

## 6. Servo Clamp Tuning

### 6.1 Initial Adjustment

The clamp angle may need tuning depending on the IV tube diameter:

| IV Tube Type | Outer Diameter | Recommended Clamp Angle |
|---|---|---|
| Standard PVC | 4.0 mm | 85°–95° |
| Thick-wall PVC | 4.5 mm | 95°–105° |
| Silicone | 5.0 mm | 80°–90° |

### 6.2 Serial Commands for Tuning

```
> AT+SERVO_TEST=90         # Move to 90° — check if tube is fully occluded
Servo moved to 90°
> AT+SERVO_TEST=0          # Release — confirm tube springs back open
Servo moved to 0°
> AT+SERVO_CLAMP_ANGLE=95  # Set new clamp angle
Clamp angle set to 95°, saved to NVS
> AT+SERVO_OPEN_ANGLE=5    # Set new open angle
Open angle set to 5°, saved to NVS
```

### 6.3 Clamp Force Verification

1. Set up IV with saline at a visible drip rate
2. Send `AT+SERVO_CLAMP` via serial
3. Observe: drip should stop completely within 2 seconds
4. If drip continues, increase clamp angle by 5° and repeat
5. Send `AT+SERVO_RELEASE` to resume flow

---

## 7. Factory Reset

To erase all calibration data and Wi-Fi credentials:

1. Press and hold the **Manual Override button** for **10 seconds**
2. OLED will show countdown: "FACTORY RESET in 5...4...3...2...1"
3. All NVS data is erased
4. Device reboots into first-time setup mode

**Alternatively, via serial:**

```
> AT+FACTORY_RESET
WARNING: This will erase all calibration and network settings.
Type CONFIRM to proceed: CONFIRM
Erasing NVS... OK
Rebooting...
```

---

## 8. Quick Reference Card

```
┌─────────────────────────────────────────────┐
│           DRIP-SENSE QUICK START            │
├─────────────────────────────────────────────┤
│                                             │
│  1. Mount unit below drip chamber           │
│  2. Route IV tube through servo clamp       │
│  3. Connect USB-C power                     │
│  4. Configure Wi-Fi (BLE app or serial)     │
│  5. Calibrate: hold button 3s, follow OLED  │
│  6. Hang IV bag — monitoring starts auto    │
│                                             │
│  BUTTON ACTIONS:                            │
│  • Short press: Cycle OLED display pages    │
│  • Hold 3s:     Enter calibration mode      │
│  • Hold 10s:    Factory reset               │
│  • During alarm: Acknowledge + release clamp│
│                                             │
│  BUZZER CODES:                              │
│  • ●●         Calibration complete          │
│  • ●—●—●—    Low fluid warning              │
│  • ●●●●●●    Emergency — tube clamped       │
│  • ●         Wi-Fi connected                │
│                                             │
│  SERIAL DEBUG: 115200 baud, type AT+HELP    │
│                                             │
└─────────────────────────────────────────────┘
```

---

> **Previous:** [← Cloud API & Data Format](api_spec.md)  
> **Next:** [Testing & Validation →](testing.md)
