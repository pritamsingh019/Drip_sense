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
float filteredWeight  = 0;
float previousWeight  = 0;
float flowRate        = 0;
bool  isClamped       = false;
bool  isCalibrated    = false;
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

    Serial.println("[SYS] System ready - MONITORING");
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

    // ── 1. Read weight every SAMPLE_INTERVAL ms ──
    if (now - lastSampleTime >= SAMPLE_INTERVAL) {

        float rawWeight = 0;
        if (scale.is_ready()) {
            rawWeight = scale.get_units(3);
            if (rawWeight < 0) rawWeight = 0;  // No negative weights
        }

        // Apply EMA filter
        filteredWeight = emaFilter(rawWeight, filteredWeight, EMA_ALPHA);

        // ── 2. Calculate flow rate ──
        float timeDelta = (float)(now - lastSampleTime) / 60000.0;  // Minutes
        if (timeDelta > 0 && previousWeight > 0) {
            float weightDelta = previousWeight - filteredWeight;
            flowRate = (weightDelta > 0) ? (weightDelta / timeDelta) : 0;
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
        bool freeFlow  = (flowRate > FREEFLOW_LIMIT);

        if ((lowFluid || freeFlow) && !isClamped) {
            isClamped = true;
            clampServo.write(CLAMP_ANGLE);
            alarmStartTime = now;

            if (lowFluid) {
                Serial.println("[ALARM] LOW FLUID DETECTED!");
                Serial.print("        Weight: ");
                Serial.print(filteredWeight, 1);
                Serial.print(" g (threshold: ");
                Serial.print(LOW_THRESHOLD, 1);
                Serial.println(" g)");
            }
            if (freeFlow) {
                Serial.println("[ALARM] FREE FLOW DETECTED!");
                Serial.print("        Flow rate: ");
                Serial.print(flowRate, 1);
                Serial.println(" mL/min");
            }
            Serial.println("        Servo CLAMPED at 90 deg");
            Serial.println("        Press the button to override");
        }

        // ── 5. Update OLED ──
        display.clearDisplay();

        // Status bar
        display.setTextSize(1);
        display.setCursor(0, 0);
        display.print(isClamped ? "!! ALARM - CLAMPED !!" : "MONITORING");

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
            if ((now / 500) % 2 == 0) {
                display.print(">> PRESS BUTTON <<");
            }
        } else if (timeToEmpty > 0) {
            int hours = (int)(timeToEmpty / 60);
            int mins  = (int)timeToEmpty % 60;
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

    // ── 7. Buzzer alarm pattern (200ms ON / 300ms OFF) ──
    if (isClamped) {
        unsigned long buzzPhase = (now - alarmStartTime) % 500;
        digitalWrite(BUZZER_PIN, (buzzPhase < 200) ? HIGH : LOW);
    }

    // ── 8. Manual override button ──
    if (digitalRead(BUTTON_PIN) == LOW && isClamped) {
        delay(50);  // Debounce
        if (digitalRead(BUTTON_PIN) == LOW) {
            Serial.println("[OK] Override pressed - releasing clamp");
            clampServo.write(OPEN_ANGLE);
            isClamped = false;
            digitalWrite(BUZZER_PIN, LOW);
            delay(500);  // Prevent re-trigger
        }
    }
}
