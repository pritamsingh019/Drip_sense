# Drip-Sense — Breadboard Simulator Guide

> **Version:** 1.0  
> **Date:** 2026-02-19  
> **Audience:** Beginners, students, hobbyists  
> **Goal:** Simulate the entire Drip-Sense circuit virtually — no physical hardware needed

---

## 1. What is a Breadboard Simulator?

A breadboard simulator is a **software tool** that lets you build and test electronic circuits on a virtual breadboard — exactly like a real one, but on your computer screen. You can:

- Drag and drop components (ESP32, sensors, LEDs, servos, etc.)
- Wire them together visually
- Write and run code (Arduino sketches)
- See real-time results without buying any hardware

This is perfect for **learning**, **prototyping**, and **validating** your circuit design before spending money on components.

---

## 2. Best Breadboard Simulators — Comparison

| Simulator | Best For | ESP32 Support | Free? | Difficulty |
|---|---|---|---|---|
| ⭐ **Wokwi** | **#1 Recommended** — Best for ESP32/Arduino | ✅ Full ESP32 support | ✅ Free | 🟢 Easy |
| **Tinkercad Circuits** | Absolute beginners | ❌ Arduino Uno only | ✅ Free | 🟢 Very Easy |
| **Proteus** | Professional simulation | ✅ (paid only) | ❌ Paid (~$250+) | 🔴 Advanced |
| **SimulIDE** | Open-source alternative | ⚠️ Limited | ✅ Free | 🟡 Medium |
| **Fritzing** | Visual wiring diagrams | ❌ No code simulation | ✅ Free (old) / $8 (new) | 🟢 Easy |
| **LTspice** | Analog circuit analysis | ❌ No MCU simulation | ✅ Free | 🔴 Advanced |

> [!IMPORTANT]
> **We strongly recommend [Wokwi](https://wokwi.com)** for Drip-Sense simulation. It's the only free simulator with full ESP32 support, Arduino code execution, and components like HX711, OLED, servo, and buzzer — all of which Drip-Sense uses.

### Why Wokwi?

- ✅ **Runs in your browser** — no installation needed
- ✅ **Full ESP32 simulation** — both cores, Wi-Fi stack (limited), GPIO, I2C, PWM
- ✅ **Built-in components** — HX711 load cell, SSD1306 OLED, servo motor, buzzer, buttons
- ✅ **Arduino code execution** — write, compile, and run directly in the browser
- ✅ **Free forever** for public projects
- ✅ **Share links** — share your simulation with classmates and mentors
- ✅ **Beginner-friendly UI** — drag, drop, wire, run

---

## 3. Getting Started with Wokwi (Step-by-Step)

### Step 1: Open Wokwi

1. Open your browser (Chrome recommended)
2. Go to **[https://wokwi.com](https://wokwi.com)**
3. Click **"Sign Up"** (use Google/GitHub account — free)
4. After login, click **"New Project"**
5. Select **"ESP32"** as the board
6. Choose **"Arduino"** as the framework
7. Click **"Create Project"**

You'll see a split screen:
- **Left side:** Code editor (Arduino `.ino` file)
- **Right side:** Virtual breadboard with an ESP32

### Step 2: Understand the Interface

```
┌───────────────────────────────────────────────────────────┐
│  📝 Code Editor          │  🔧 Virtual Breadboard         │
│                           │                                │
│  void setup() {           │   ┌──────────┐                │
│    // your code           │   │  ESP32   │                │
│  }                        │   │  Board    │                │
│                           │   └──────────┘                │
│  void loop() {            │                                │
│    // your code           │   [+ Add Component]            │
│  }                        │                                │
│                           │                                │
├───────────────────────────┴────────────────────────────────┤
│  ▶️ Start Simulation  │  ⏹ Stop  │  📟 Serial Monitor     │
└────────────────────────────────────────────────────────────┘
```

**Key buttons:**
- **▶️ Start Simulation** — compile and run your code
- **⏹ Stop** — stop the simulation
- **📟 Serial Monitor** — view `Serial.print()` output (like a real USB connection)
- **[+ Add Component]** — add new components to the breadboard

---

## 4. Building the Drip-Sense Circuit (Step-by-Step)

We'll build the full Drip-Sense circuit in 6 steps, adding one component at a time.

---

### Step 3: Add the Load Cell + HX711

**What it does:** Measures the weight of the IV bag.

1. Click **[+ Add Component]** on the breadboard area
2. Search for **"HX711"**  
3. Click to add it to the breadboard
4. Wire it to the ESP32:

| HX711 Pin | ESP32 Pin | Wire Color (suggestion) |
|---|---|---|
| VCC | 3V3 | 🔴 Red |
| GND | GND | ⚫ Black |
| SCK | GPIO 18 | 🟡 Yellow |
| DT (DOUT) | GPIO 19 | 🟢 Green |

**How to wire in Wokwi:**
1. Click on the HX711's **VCC** pin → a wire starts
2. Click on the ESP32's **3V3** pin → wire connects
3. Repeat for GND, SCK, and DT

> [!TIP]
> In Wokwi, you can click on the HX711 component during simulation and **type a weight value** (e.g., 500) to simulate placing a weight on the load cell. This is how you'll test without real hardware!

**Test code — paste into the editor:**

```cpp
#include "HX711.h"

#define HX711_SCK  18
#define HX711_DT   19

HX711 scale;

void setup() {
    Serial.begin(115200);
    Serial.println("HX711 Test - Starting...");
    
    scale.begin(HX711_DT, HX711_SCK);
    scale.set_scale(420.0);  // Calibration factor (adjust as needed)
    scale.tare();            // Zero the scale
    
    Serial.println("Scale is ready! Try changing the weight in the HX711 component.");
}

void loop() {
    if (scale.is_ready()) {
        float weight = scale.get_units(5);  // Average of 5 readings
        Serial.print("Weight: ");
        Serial.print(weight, 1);
        Serial.println(" g");
    }
    delay(500);
}
```

3. Click **▶️ Start Simulation**
4. Open **Serial Monitor** at the bottom
5. Click on the HX711 component → enter different weight values
6. Watch the serial monitor update! ✅

---

### Step 4: Add the OLED Display

**What it does:** Shows weight, flow rate, and ETA on a tiny screen.

1. Click **[+ Add Component]** → search **"SSD1306"** or **"OLED"**
2. Add the 128×64 I2C OLED to the breadboard
3. Wire it:

| OLED Pin | ESP32 Pin | Wire Color |
|---|---|---|
| VCC | 3V3 | 🔴 Red |
| GND | GND | ⚫ Black |
| SDA | GPIO 21 | 🔵 Blue |
| SCL | GPIO 22 | 🟣 Purple |

**Add to your code — replace the previous code with this expanded version:**

```cpp
#include "HX711.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Pin Definitions
#define HX711_SCK    18
#define HX711_DT     19
#define OLED_WIDTH   128
#define OLED_HEIGHT  64
#define OLED_ADDR    0x3C

HX711 scale;
Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);

void setup() {
    Serial.begin(115200);
    
    // Initialize HX711
    scale.begin(HX711_DT, HX711_SCK);
    scale.set_scale(420.0);
    scale.tare();
    
    // Initialize OLED
    if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
        Serial.println("OLED init failed!");
        while (true);  // Stop here if OLED fails
    }
    
    // Splash screen
    display.clearDisplay();
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(10, 10);
    display.println("Drip-Sense");
    display.setTextSize(1);
    display.setCursor(30, 40);
    display.println("v1.0.0");
    display.display();
    delay(2000);
    
    Serial.println("Drip-Sense started!");
}

void loop() {
    float weight = 0;
    if (scale.is_ready()) {
        weight = scale.get_units(5);
    }
    
    // Update OLED
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println("-- DRIP-SENSE --");
    
    display.setTextSize(2);
    display.setCursor(0, 16);
    display.print(weight, 1);
    display.println(" g");
    
    display.setTextSize(1);
    display.setCursor(0, 40);
    display.print("Flow: -- mL/min");
    
    display.setCursor(0, 52);
    display.print("ETA:  -- min");
    
    display.display();
    
    // Serial output
    Serial.print("Weight: ");
    Serial.print(weight, 1);
    Serial.println(" g");
    
    delay(500);
}
```

**Add libraries in Wokwi:**
1. Click the **"Library Manager"** icon (📚) in the code editor
2. Search and add:
   - `HX711`
   - `Adafruit SSD1306`
   - `Adafruit GFX Library`

3. Click **▶️ Start Simulation**
4. You should see the splash screen "Drip-Sense v1.0.0" on the OLED, then live weight updates!

---

### Step 5: Add the Servo Motor

**What it does:** Clamps the IV tube when an alarm triggers.

1. Click **[+ Add Component]** → search **"Servo"**
2. Add a servo motor to the breadboard
3. Wire it:

| Servo Wire | ESP32 Pin | Wire Color |
|---|---|---|
| Signal (Orange/Yellow) | GPIO 13 | 🟠 Orange |
| Power (Red) | 5V (VIN) | 🔴 Red |
| Ground (Brown/Black) | GND | ⚫ Black |

**Add servo code to your sketch — add these sections:**

At the top (with other includes):
```cpp
#include <ESP32Servo.h>

#define SERVO_PIN     13
#define CLAMP_ANGLE   90
#define OPEN_ANGLE    0
#define LOW_THRESHOLD 10.0  // grams

Servo clampServo;
bool isClamped = false;
```

In `setup()`:
```cpp
    // Initialize Servo
    clampServo.attach(SERVO_PIN);
    clampServo.write(OPEN_ANGLE);  // Start open
```

In `loop()`, after the weight reading:
```cpp
    // Safety check
    if (weight > 0 && weight < LOW_THRESHOLD && !isClamped) {
        Serial.println("⚠️ LOW FLUID! Clamping tube...");
        clampServo.write(CLAMP_ANGLE);
        isClamped = true;
    }
    
    // Display clamp status on OLED
    if (isClamped) {
        display.setCursor(0, 52);
        display.print("!! TUBE CLAMPED !!");
    }
```

4. **▶️ Start Simulation** → set HX711 weight to values below 10 → watch the servo rotate to 90°!

---

### Step 6: Add the Buzzer

**What it does:** Makes alarm sounds when something goes wrong.

1. Click **[+ Add Component]** → search **"Buzzer"** (or Piezo)
2. Add a buzzer to the breadboard
3. Wire it:

| Buzzer Pin | ESP32 Pin | Wire Color |
|---|---|---|
| + (positive) | GPIO 15 | 🟤 Brown |
| − (negative) | GND | ⚫ Black |

**Add buzzer code:**

At the top:
```cpp
#define BUZZER_PIN  15
```

In `setup()`:
```cpp
    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);
```

In the safety check section (when clamping):
```cpp
    // Buzzer alarm when clamped
    if (isClamped) {
        digitalWrite(BUZZER_PIN, HIGH);
        delay(200);
        digitalWrite(BUZZER_PIN, LOW);
        delay(200);
    }
```

---

### Step 7: Add the Override Button

**What it does:** Lets the nurse acknowledge the alarm and release the clamp.

1. Click **[+ Add Component]** → search **"Push Button"**
2. Add a pushbutton to the breadboard
3. Wire it:

| Button Pin | Connect To | Wire Color |
|---|---|---|
| One leg | GPIO 4 | 🟡 Yellow |
| Other leg | GND | ⚫ Black |

**Add button code:**

At the top:
```cpp
#define BUTTON_PIN  4
```

In `setup()`:
```cpp
    pinMode(BUTTON_PIN, INPUT_PULLUP);  // Built-in pull-up resistor
```

In `loop()`:
```cpp
    // Manual override button
    if (digitalRead(BUTTON_PIN) == LOW && isClamped) {
        Serial.println("✅ Override pressed — releasing clamp");
        clampServo.write(OPEN_ANGLE);
        isClamped = false;
        digitalWrite(BUZZER_PIN, LOW);
        delay(500);  // Debounce
    }
```

---

## 5. Complete Simulation Code

Here is the **complete, ready-to-paste code** that combines all components:

```cpp
// ========================================
// Drip-Sense — Breadboard Simulator Code
// Platform: ESP32 (Wokwi Simulator)
// ========================================

#include "HX711.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESP32Servo.h>

// ── Pin Definitions ──
#define HX711_SCK     18
#define HX711_DT      19
#define OLED_WIDTH    128
#define OLED_HEIGHT   64
#define OLED_ADDR     0x3C
#define SERVO_PIN     13
#define BUZZER_PIN    15
#define BUTTON_PIN    4

// ── Configuration ──
#define CLAMP_ANGLE       90      // Degrees to clamp tube
#define OPEN_ANGLE        0       // Degrees to open tube
#define LOW_THRESHOLD     10.0    // Grams — alarm when below this
#define FREEFLOW_LIMIT    10.0    // mL/min — alarm when above this
#define EMA_ALPHA         0.3     // Smoothing filter factor
#define SAMPLE_INTERVAL   500     // Milliseconds between readings

// ── Global Objects ──
HX711 scale;
Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);
Servo clampServo;

// ── State Variables ──
float filteredWeight = 0;
float previousWeight = 0;
float flowRate = 0;
bool isClamped = false;
bool isCalibrated = false;
unsigned long lastSampleTime = 0;
unsigned long alarmStartTime = 0;

// ── EMA Filter ──
float emaFilter(float newValue, float lastValue, float alpha) {
    if (lastValue == 0) return newValue;  // First reading
    return alpha * newValue + (1.0 - alpha) * lastValue;
}

// ── Setup ──
void setup() {
    Serial.begin(115200);
    Serial.println();
    Serial.println("============================");
    Serial.println("  Drip-Sense Simulator v1.0 ");
    Serial.println("============================");
    
    // GPIO setup
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    digitalWrite(BUZZER_PIN, LOW);
    
    // Servo setup
    clampServo.attach(SERVO_PIN);
    clampServo.write(OPEN_ANGLE);
    Serial.println("[HAL] Servo initialized (open position)");
    
    // HX711 setup
    scale.begin(HX711_DT, HX711_SCK);
    scale.set_scale(420.0);
    scale.tare();
    isCalibrated = true;
    Serial.println("[HAL] HX711 initialized and tared");
    
    // OLED setup
    if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
        Serial.println("[ERR] OLED initialization failed!");
    } else {
        Serial.println("[HAL] OLED initialized");
    }
    
    // Splash screen
    display.clearDisplay();
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(4, 8);
    display.println("Drip-Sense");
    display.setTextSize(1);
    display.setCursor(30, 35);
    display.println("Simulator v1.0");
    display.setCursor(15, 50);
    display.println("Initializing...");
    display.display();
    delay(2000);
    
    Serial.println("[SYS] System ready — MONITORING");
    Serial.println();
    Serial.println("TIP: Click the HX711 component");
    Serial.println("     and enter a weight value to");
    Serial.println("     simulate an IV bag!");
    Serial.println();
    
    lastSampleTime = millis();
}

// ── Main Loop ──
void loop() {
    unsigned long now = millis();
    
    // ── 1. Read weight (every SAMPLE_INTERVAL ms) ──
    if (now - lastSampleTime >= SAMPLE_INTERVAL) {
        float rawWeight = 0;
        if (scale.is_ready()) {
            rawWeight = scale.get_units(3);
            if (rawWeight < 0) rawWeight = 0;  // No negative weights
        }
        
        // Apply EMA filter
        filteredWeight = emaFilter(rawWeight, filteredWeight, EMA_ALPHA);
        
        // ── 2. Calculate flow rate ──
        float timeDelta = (now - lastSampleTime) / 60000.0;  // Minutes
        if (timeDelta > 0 && previousWeight > 0) {
            float weightDelta = previousWeight - filteredWeight;
            if (weightDelta > 0) {
                flowRate = weightDelta / timeDelta;  // g/min ≈ mL/min
            } else {
                flowRate = 0;
            }
        }
        
        previousWeight = filteredWeight;
        lastSampleTime = now;
        
        // ── 3. Calculate time to empty ──
        float timeToEmpty = 0;
        if (flowRate > 0.1) {
            timeToEmpty = filteredWeight / flowRate;  // Minutes
        }
        
        // ── 4. Safety checks ──
        bool lowFluid = (filteredWeight > 0 && filteredWeight < LOW_THRESHOLD);
        bool freeFlow = (flowRate > FREEFLOW_LIMIT);
        
        if ((lowFluid || freeFlow) && !isClamped) {
            // ALARM! Clamp the tube
            isClamped = true;
            clampServo.write(CLAMP_ANGLE);
            alarmStartTime = now;
            
            if (lowFluid) {
                Serial.println("🚨 ALARM: LOW FLUID DETECTED!");
                Serial.print("   Weight: ");
                Serial.print(filteredWeight, 1);
                Serial.print(" g (threshold: ");
                Serial.print(LOW_THRESHOLD, 1);
                Serial.println(" g)");
            }
            if (freeFlow) {
                Serial.println("🚨 ALARM: FREE FLOW DETECTED!");
                Serial.print("   Flow rate: ");
                Serial.print(flowRate, 1);
                Serial.println(" mL/min");
            }
            Serial.println("   → Servo CLAMPED at 90°");
            Serial.println("   → Press the button to override");
        }
        
        // ── 5. Update OLED display ──
        display.clearDisplay();
        
        // Status bar
        display.setTextSize(1);
        display.setCursor(0, 0);
        if (isClamped) {
            display.print("!! ALARM - CLAMPED !!");
        } else {
            display.print("MONITORING");
        }
        
        // Weight (large)
        display.setTextSize(2);
        display.setCursor(0, 14);
        display.print(filteredWeight, 1);
        display.setTextSize(1);
        display.print(" g");
        
        // Flow rate
        display.setTextSize(1);
        display.setCursor(0, 36);
        display.print("Flow: ");
        display.print(flowRate, 1);
        display.print(" mL/min");
        
        // ETA or alarm message
        display.setCursor(0, 48);
        if (isClamped) {
            // Flashing effect
            if ((now / 500) % 2 == 0) {
                display.print(">> PRESS BUTTON <<");
            }
        } else if (timeToEmpty > 0) {
            int hours = (int)(timeToEmpty / 60);
            int mins = (int)timeToEmpty % 60;
            display.print("ETA: ");
            if (hours > 0) {
                display.print(hours);
                display.print("h ");
            }
            display.print(mins);
            display.print("m remaining");
        } else {
            display.print("ETA: --");
        }
        
        display.display();
        
        // ── 6. Serial logging ──
        Serial.print("W:");
        Serial.print(filteredWeight, 1);
        Serial.print("g | F:");
        Serial.print(flowRate, 1);
        Serial.print("mL/m | ETA:");
        if (timeToEmpty > 0) {
            Serial.print(timeToEmpty, 0);
            Serial.print("m");
        } else {
            Serial.print("--");
        }
        Serial.print(" | State:");
        Serial.println(isClamped ? "CLAMPED" : "OK");
    }
    
    // ── 7. Buzzer alarm pattern ──
    if (isClamped) {
        // Intermittent buzzer: 200ms ON, 300ms OFF
        unsigned long buzzPhase = (now - alarmStartTime) % 500;
        digitalWrite(BUZZER_PIN, buzzPhase < 200 ? HIGH : LOW);
    }
    
    // ── 8. Manual override button ──
    if (digitalRead(BUTTON_PIN) == LOW && isClamped) {
        delay(50);  // Debounce
        if (digitalRead(BUTTON_PIN) == LOW) {
            Serial.println("✅ Override button pressed — releasing clamp");
            clampServo.write(OPEN_ANGLE);
            isClamped = false;
            digitalWrite(BUZZER_PIN, LOW);
            delay(500);  // Prevent multiple triggers
        }
    }
}
```

---

## 6. Wokwi `diagram.json` (Auto-Wiring)

Instead of manually wiring each component, you can paste this into Wokwi's **diagram.json** file (click the small file icon next to the code editor and select `diagram.json`):

```json
{
  "version": 1,
  "author": "Drip-Sense",
  "editor": "wokwi",
  "parts": [
    { "type": "board-esp32-devkit-c-v4", "id": "esp", "top": 0, "left": 0 },
    { "type": "wokwi-hx711", "id": "hx1", "top": -100, "left": 200 },
    { "type": "board-ssd1306", "id": "oled1", "top": -100, "left": -200 },
    { "type": "wokwi-servo", "id": "servo1", "top": 200, "left": 200 },
    { "type": "wokwi-buzzer", "id": "bz1", "top": 200, "left": -100 },
    { "type": "wokwi-pushbutton", "id": "btn1", "top": 200, "left": 0 }
  ],
  "connections": [
    ["esp:18", "hx1:SCK", "yellow", ["v:20"]],
    ["esp:19", "hx1:DT", "green", ["v:30"]],
    ["esp:3V3", "hx1:VCC", "red", ["v:10"]],
    ["esp:GND.1", "hx1:GND", "black", ["v:10"]],
    ["esp:21", "oled1:SDA", "blue", ["v:20"]],
    ["esp:22", "oled1:SCL", "purple", ["v:30"]],
    ["esp:3V3", "oled1:VCC", "red", ["v:10"]],
    ["esp:GND.2", "oled1:GND", "black", ["v:10"]],
    ["esp:13", "servo1:PWM", "orange", ["v:20"]],
    ["esp:5V", "servo1:V+", "red", ["v:10"]],
    ["esp:GND.3", "servo1:GND", "black", ["v:10"]],
    ["esp:15", "bz1:1", "brown", ["v:20"]],
    ["esp:GND.4", "bz1:2", "black", ["v:10"]],
    ["esp:4", "btn1:1.l", "yellow", ["v:20"]],
    ["esp:GND.5", "btn1:2.l", "black", ["v:10"]]
  ]
}
```

> [!TIP]
> After pasting the `diagram.json`, all components will be pre-wired. You can rearrange them visually by dragging, without breaking the connections.

---

## 7. How to Test Each Feature

### Test 1: Weight Measurement

1. **▶️ Start Simulation**
2. Click on the **HX711 component** on the breadboard
3. A pop-up appears — enter **500** (simulating a 500g IV bag)
4. Watch the OLED display update to show `500.0 g`
5. Watch the serial monitor log: `W:500.0g | F:0.0mL/m | ETA:--`

### Test 2: Flow Rate Detection

1. While simulation is running, change the HX711 weight from **500** to **490**
2. Wait 2 seconds, then change to **480**
3. Continue reducing by 10g every few seconds
4. The OLED will show a non-zero flow rate (e.g., `Flow: 2.5 mL/min`)
5. ETA will appear (e.g., `ETA: 3h 12m remaining`)

### Test 3: Low Fluid Alarm

1. While simulation is running, set the HX711 weight to **8** (below the 10g threshold)
2. Watch:
   - ⚙️ Servo rotates to 90° (clamped position)
   - 🔊 Buzzer starts beeping
   - 📺 OLED shows `"!! ALARM - CLAMPED !!"`
   - 📟 Serial prints `"🚨 ALARM: LOW FLUID DETECTED!"`

### Test 4: Manual Override

1. While the alarm is active, click the **push button** on the breadboard
2. Watch:
   - ⚙️ Servo returns to 0° (open position)
   - 🔊 Buzzer stops
   - 📺 OLED returns to normal `"MONITORING"` display
   - 📟 Serial prints `"✅ Override button pressed — releasing clamp"`

### Test 5: Free-Flow Detection

1. Set the HX711 weight to **500**
2. Wait 2 seconds, then rapidly change to **400**, then **300**, then **200** (very fast drops)
3. This simulates a free-flow condition (rapid drainage)
4. The alarm should trigger with `"🚨 ALARM: FREE FLOW DETECTED!"`

---

## 8. Common Beginner Mistakes & Fixes

| Mistake | What Happens | Fix |
|---|---|---|
| Forgot to add library | Compilation error: `'HX711.h' not found` | Click 📚 Library Manager → search and add the library |
| Wrong pin numbers | Component doesn't respond | Double-check GPIO numbers match `config.h` and wiring |
| OLED address wrong | Blank screen, no error | Use `0x3C` (default for most 0.96" OLEDs) |
| Servo on 3.3V | Servo jitters or doesn't move | Servo needs **5V** — connect to VIN, not 3V3 |
| Button not debounced | Multiple triggers per press | Add `delay(50)` after button read (already included in code) |
| Weight reads negative | Scale not tared | Call `scale.tare()` in setup, or re-run simulation |
| Simulation won't start | Code has syntax error | Check the error message at the bottom of the editor |
| Components overlap | Hard to see wiring | Drag components apart; use the zoom controls |

---

## 9. Next Steps After Simulation

Once you've verified the full circuit works in Wokwi:

| Step | What to Do | Guide |
|---|---|---|
| 1 | Buy the physical components (~₹2,800) | [PRD — Hardware Constraints](prd.md#6-hardware-constraints) |
| 2 | Wire on a real breadboard | [Setup Guide — Hardware Assembly](setup.md#phase-2-hardware-assembly) |
| 3 | Flash the firmware to a real ESP32 | [Deployment Guide](deployment.md) |
| 4 | Calibrate the load cell | [Calibration Guide](calibration.md) |
| 5 | Mount on an IV pole | [Setup Guide — Phase 6](setup.md#phase-6-deployment-on-iv-pole) |

---

## 10. Other Simulators (Alternatives)

### Tinkercad Circuits (Beginner-Friendly, No ESP32)

If you're completely new to electronics and want to learn the basics first:

1. Go to [tinkercad.com/circuits](https://www.tinkercad.com/circuits)
2. Create an account (free)
3. Use an **Arduino Uno** (ESP32 not available)
4. Good for learning: LEDs, buttons, servos, buzzers, basic sensors
5. **Limitation:** No HX711, no I2C OLED, no Wi-Fi — cannot simulate full Drip-Sense

### Proteus (Professional, Paid)

For professional PCB design simulation:

1. Download from [labcenter.com](https://www.labcenter.com/)
2. Requires paid license (~$250+)
3. Supports ESP32 with additional model libraries
4. Best for: PCB layout verification, analog simulation, EMI analysis
5. **Overkill for beginners** — recommended only for Phase 2 (engineering prototype)

---

> **See also:**
> - [Setup Guide](setup.md) — Physical hardware setup
> - [Firmware Design](firmware_design.md) — Understanding the code architecture
> - [Full Project Guide](guide.md) — Everything about Drip-Sense
