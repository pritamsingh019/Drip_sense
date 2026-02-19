#!/usr/bin/env python3
"""Create all project directories and placeholder files for Drip-Sense."""

import os

BASE = '/Volumes/Aditya ssd/github_collab/Drip_sense'

# ============================================================
# Define all files and their contents
# ============================================================
files = {}

# ── src/main.cpp ──
files['src/main.cpp'] = '''/**
 * @file main.cpp
 * @brief Drip-Sense Application Entry Point
 *
 * Initializes all HAL drivers, loads NVS configuration,
 * creates FreeRTOS tasks, and starts the scheduler.
 */

#include "config.h"

void setup() {
    // TODO: HAL initialization
    // TODO: NVS config load
    // TODO: FreeRTOS task creation
}

void loop() {}
'''

# ── src/config.h ──
files['src/config.h'] = '''#ifndef CONFIG_H
#define CONFIG_H

// GPIO Pin Definitions
#define PIN_HX711_SCK       18
#define PIN_HX711_DOUT      19
#define PIN_OLED_SDA        21
#define PIN_OLED_SCL        22
#define PIN_SERVO_PWM       13
#define PIN_BUZZER          15
#define PIN_BUTTON_OVERRIDE  4

// Sensor Settings
#define SENSOR_SAMPLE_RATE_HZ   10
#define EMA_ALPHA               0.3f
#define TARE_SAMPLES            20

// Safety Thresholds
#define LOW_FLUID_THRESHOLD_G   10.0f
#define FREE_FLOW_MULTIPLIER    1.5f
#define FLOW_STALL_TIMEOUT_MS   30000

// Network Settings
#define MQTT_BROKER_URL     "mqtts://broker.dripsense.io"
#define MQTT_PORT           8883
#define WIFI_RETRY_MAX      5
#define MQTT_PUBLISH_INTERVAL_MS 5000

// Display Settings
#define OLED_I2C_ADDR       0x3C
#define OLED_WIDTH          128
#define OLED_HEIGHT         64
#define SCREENSAVER_TIMEOUT_MS 60000

// Servo Settings
#define SERVO_CLAMP_ANGLE   90
#define SERVO_OPEN_ANGLE    0

// Watchdog
#define WDT_TIMEOUT_SEC     5

#endif // CONFIG_H
'''

# ── HAL Layer ──
files['src/hal/hw_hx711.h'] = '''#ifndef HW_HX711_H
#define HW_HX711_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint8_t pin_sck;
    uint8_t pin_dout;
    int32_t offset;
    float   scale;
} hx711_config_t;

void    hx711_init(hx711_config_t *cfg);
bool    hx711_is_ready(void);
int32_t hx711_read_raw(void);
float   hx711_read_grams(void);
void    hx711_tare(int samples);
void    hx711_set_gain(uint8_t gain);
void    hx711_power_down(void);
void    hx711_power_up(void);

#endif
'''

files['src/hal/hw_hx711.cpp'] = '''#include "hw_hx711.h"
#include "../config.h"

// TODO: Implement HX711 ADC driver (bit-bang protocol)
'''

files['src/hal/hw_oled.h'] = '''#ifndef HW_OLED_H
#define HW_OLED_H

#include <stdint.h>
#include <stdbool.h>

void oled_init(void);
void oled_clear(void);
void oled_set_cursor(uint8_t x, uint8_t y);
void oled_print(const char *text, uint8_t font_size);
void oled_draw_icon(const uint8_t *bitmap, uint8_t x, uint8_t y);
void oled_draw_progress_bar(uint8_t x, uint8_t y, uint8_t w, uint8_t h, uint8_t percent);
void oled_display(void);
void oled_set_brightness(uint8_t level);
void oled_sleep(bool enable);

#endif
'''

files['src/hal/hw_oled.cpp'] = '''#include "hw_oled.h"
#include "../config.h"

// TODO: Implement SSD1306 OLED display driver
'''

files['src/hal/hw_servo.h'] = '''#ifndef HW_SERVO_H
#define HW_SERVO_H

#include <stdint.h>

void servo_init(void);
void servo_set_angle(uint8_t angle);
void servo_clamp(void);
void servo_release(void);
void servo_detach(void);
void servo_smooth_clamp(uint16_t step_delay_ms);

#endif
'''

files['src/hal/hw_servo.cpp'] = '''#include "hw_servo.h"
#include "../config.h"

// TODO: Implement Servo motor PWM driver
'''

files['src/hal/hw_buzzer.h'] = '''#ifndef HW_BUZZER_H
#define HW_BUZZER_H

typedef enum {
    BUZZER_PATTERN_SINGLE,
    BUZZER_PATTERN_DOUBLE,
    BUZZER_PATTERN_INTERMITTENT,
    BUZZER_PATTERN_CONTINUOUS,
    BUZZER_PATTERN_OFF
} buzzer_pattern_t;

void buzzer_init(void);
void buzzer_play(buzzer_pattern_t pattern);
void buzzer_stop(void);

#endif
'''

files['src/hal/hw_buzzer.cpp'] = '''#include "hw_buzzer.h"
#include "../config.h"

// TODO: Implement piezo buzzer driver
'''

# ── Middleware Layer ──
files['src/middleware/sensor_fusion.h'] = '''#ifndef SENSOR_FUSION_H
#define SENSOR_FUSION_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    float alpha;
    float last_value;
    bool  initialized;
} ema_filter_t;

typedef struct {
    float x_est, P, Q, R, K;
} kalman_1d_t;

typedef struct {
    float   *ring_buffer;
    uint16_t index;
    bool     full;
} flow_calc_t;

void  ema_init(ema_filter_t *f, float alpha);
float ema_update(ema_filter_t *f, float new_value);
void  kalman_init(kalman_1d_t *k, float Q, float R);
float kalman_update(kalman_1d_t *k, float measurement);
float flow_calc_update(flow_calc_t *fc, float weight_g, uint32_t timestamp_ms);

#endif
'''

files['src/middleware/sensor_fusion.cpp'] = '''#include "sensor_fusion.h"

// TODO: Implement signal processing pipeline (EMA, Kalman, flow calc)
'''

files['src/middleware/safety_ctrl.h'] = '''#ifndef SAFETY_CTRL_H
#define SAFETY_CTRL_H

#include <stdbool.h>

typedef enum {
    SAFETY_EVENT_NONE,
    SAFETY_EVENT_LOW_FLUID,
    SAFETY_EVENT_FREE_FLOW,
    SAFETY_EVENT_FLOW_STALL,
    SAFETY_EVENT_AIR_DETECT
} safety_event_t;

typedef struct {
    float   rate_history[10];
    uint8_t debounce_count;
} freeflow_detector_t;

bool detect_low_fluid(float weight_g);
bool detect_free_flow(float flow_rate, float expected_rate);
bool detect_flow_stall(float delta_weight, uint32_t elapsed_ms);
safety_event_t evaluate_safety(float weight_g, float flow_rate, float expected_rate);

#endif
'''

files['src/middleware/safety_ctrl.cpp'] = '''#include "safety_ctrl.h"
#include "../config.h"

// TODO: Implement safety controller
'''

files['src/middleware/state_machine.h'] = '''#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

typedef enum {
    STATE_IDLE,
    STATE_CALIBRATING,
    STATE_MONITORING,
    STATE_LOW_FLUID,
    STATE_FREE_FLOW,
    STATE_AIR_DETECT,
    STATE_CLAMPED,
    STATE_ERROR,
    STATE_OTA_UPDATE
} system_state_t;

void state_init(void);
bool state_transition(system_state_t new_state);
system_state_t state_get_current(void);
const char* state_get_name(system_state_t state);

#endif
'''

files['src/middleware/state_machine.cpp'] = '''#include "state_machine.h"

// TODO: Implement system state manager
'''

files['src/middleware/event_bus.h'] = '''#ifndef EVENT_BUS_H
#define EVENT_BUS_H

#include <stdint.h>

typedef enum {
    EVENT_WEIGHT_UPDATE,
    EVENT_FLOW_UPDATE,
    EVENT_ALARM,
    EVENT_STATE_CHANGE,
    EVENT_WIFI_STATUS,
    EVENT_BUTTON_PRESS
} event_type_t;

typedef union {
    float weight_g;
    float flow_rate;
    int   alarm_type;
    int   state;
    int   wifi_status;
} event_data_t;

typedef void (*event_callback_t)(event_type_t type, event_data_t data);

void event_bus_init(void);
void event_bus_subscribe(event_type_t type, event_callback_t callback);
void event_bus_publish(event_type_t type, event_data_t data);

#endif
'''

files['src/middleware/event_bus.cpp'] = '''#include "event_bus.h"

// TODO: Implement event pub/sub system with FreeRTOS queue
'''

files['src/middleware/config_mgr.h'] = '''#ifndef CONFIG_MGR_H
#define CONFIG_MGR_H

#include <stdbool.h>

void  config_init(void);
bool  config_load(void);
bool  config_save(void);
float config_get_float(const char *ns, const char *key, float default_val);
bool  config_set_float(const char *ns, const char *key, float value);
const char* config_get_string(const char *ns, const char *key, const char *default_val);
bool  config_set_string(const char *ns, const char *key, const char *value);
void  config_factory_reset(void);

#endif
'''

files['src/middleware/config_mgr.cpp'] = '''#include "config_mgr.h"

// TODO: Implement NVS configuration manager
'''

# ── App Layer ──
files['src/app/monitor.h'] = '''#ifndef MONITOR_H
#define MONITOR_H

void  monitor_task(void *pvParameters);
float monitor_get_weight(void);
float monitor_get_flow_rate(void);
float monitor_get_time_to_empty(void);

#endif
'''

files['src/app/monitor.cpp'] = '''#include "monitor.h"
#include "../middleware/sensor_fusion.h"
#include "../middleware/safety_ctrl.h"
#include "../middleware/event_bus.h"

// TODO: Implement monitoring engine task (Core 1, 10 Hz)
'''

files['src/app/ui_mgr.h'] = '''#ifndef UI_MGR_H
#define UI_MGR_H

void ui_task(void *pvParameters);
void ui_show_splash(void);
void ui_show_calibration(void);
void ui_show_alarm(int alarm_type);

#endif
'''

files['src/app/ui_mgr.cpp'] = '''#include "ui_mgr.h"
#include "../hal/hw_oled.h"
#include "../hal/hw_buzzer.h"
#include "../middleware/event_bus.h"

// TODO: Implement UI manager (OLED + Buzzer, Core 0, 2 Hz)
'''

files['src/app/telemetry.h'] = '''#ifndef TELEMETRY_H
#define TELEMETRY_H

void telemetry_task(void *pvParameters);
void telemetry_publish_immediate(const char *topic, const char *payload);

#endif
'''

files['src/app/telemetry.cpp'] = '''#include "telemetry.h"
#include "../net/mqtt_client.h"
#include "../middleware/event_bus.h"

// TODO: Implement MQTT telemetry publisher (Core 0, 5s interval)
'''

# ── Network Layer ──
files['src/net/wifi_mgr.h'] = '''#ifndef WIFI_MGR_H
#define WIFI_MGR_H

#include <stdbool.h>
#include <stdint.h>

void wifi_init(void);
void wifi_connect(const char *ssid, const char *password);
void wifi_disconnect(void);
int8_t wifi_get_rssi(void);
const char* wifi_get_ip(void);
bool wifi_is_connected(void);
void wifi_scan(void);

#endif
'''

files['src/net/wifi_mgr.cpp'] = '''#include "wifi_mgr.h"

// TODO: Implement Wi-Fi connection manager
'''

files['src/net/mqtt_client.h'] = '''#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include <stdbool.h>
#include <stdint.h>

void mqtt_init(const char *broker_url, uint16_t port);
void mqtt_connect(const char *device_id, const char *token);
void mqtt_publish(const char *topic, const char *payload, int qos);
void mqtt_subscribe(const char *topic);
bool mqtt_is_connected(void);

#endif
'''

files['src/net/mqtt_client.cpp'] = '''#include "mqtt_client.h"

// TODO: Implement MQTT client wrapper (TLS, QoS 0/1)
'''

files['src/net/ble_prov.h'] = '''#ifndef BLE_PROV_H
#define BLE_PROV_H

#include <stdbool.h>

void ble_prov_init(void);
void ble_prov_start(void);
void ble_prov_stop(void);
bool ble_prov_is_active(void);

#endif
'''

files['src/net/ble_prov.cpp'] = '''#include "ble_prov.h"

// TODO: Implement BLE Wi-Fi provisioning (GATT server)
'''

files['src/net/ota_mgr.h'] = '''#ifndef OTA_MGR_H
#define OTA_MGR_H

#include <stdbool.h>

void ota_init(void);
bool ota_check(void);
void ota_start_update(const char *url);
void ota_rollback(void);
void ota_get_partition_info(char *active, char *inactive);

#endif
'''

files['src/net/ota_mgr.cpp'] = '''#include "ota_mgr.h"

// TODO: Implement OTA update manager (SHA-256 verify, dual partition)
'''

# ── include/ ──
files['include/version.h'] = '''#ifndef VERSION_H
#define VERSION_H

#define FW_VERSION_MAJOR    1
#define FW_VERSION_MINOR    0
#define FW_VERSION_PATCH    0
#define FW_VERSION_STRING   "1.0.0"

#define FW_BUILD_DATE       __DATE__
#define FW_BUILD_TIME       __TIME__

#endif
'''

# ── lib/ ──
files['lib/dripsense_common/ds_types.h'] = '''#ifndef DS_TYPES_H
#define DS_TYPES_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    float    weight_g;
    uint32_t timestamp_ms;
    bool     valid;
} weight_reading_t;

typedef struct {
    float rate_ml_min;
    float time_to_empty_min;
} flow_data_t;

typedef enum {
    ALARM_NONE, ALARM_LOW_FLUID, ALARM_FREE_FLOW,
    ALARM_AIR_DETECT, ALARM_SENSOR_FAIL
} alarm_event_t;

typedef struct {
    float    weight_g;
    float    flow_rate;
    float    eta_min;
    int8_t   rssi;
    uint32_t heap_free;
    uint32_t uptime_sec;
} device_status_t;

#endif
'''

files['lib/dripsense_common/ds_constants.h'] = '''#ifndef DS_CONSTANTS_H
#define DS_CONSTANTS_H

#define GRAVITY             9.80665f
#define WATER_DENSITY       1.0f
#define SALINE_DENSITY      1.0046f

#define DRIP_FACTOR_MACRO   20
#define DRIP_FACTOR_MICRO   60
#define DRIP_FACTOR_BLOOD   10

#endif
'''

files['lib/at_command/at_parser.h'] = '''#ifndef AT_PARSER_H
#define AT_PARSER_H

typedef void (*at_handler_t)(const char *args);

void at_register(const char *command, at_handler_t handler);
void at_process_line(const char *line);

#endif
'''

files['lib/at_command/at_parser.cpp'] = '''#include "at_parser.h"

// TODO: Implement AT command parser (AT+HELP, AT+VERSION, AT+REBOOT)
'''

# ── Test files ──
native_tests = [
    'test_ema_filter', 'test_kalman_filter', 'test_flow_calc',
    'test_anomaly_detection', 'test_servo_mapping', 'test_state_machine',
    'test_event_bus', 'test_config_mgr'
]
for t in native_tests:
    files[f'test/test_native/{t}.cpp'] = f'''#include <unity.h>

// TODO: Implement {t.replace("test_", "")} unit tests

void setUp(void) {{}}
void tearDown(void) {{}}

void test_placeholder(void) {{
    TEST_ASSERT_TRUE(1);
}}

int main(void) {{
    UNITY_BEGIN();
    RUN_TEST(test_placeholder);
    return UNITY_END();
}}
'''

embedded_tests = [
    'test_hx711_driver', 'test_oled_driver', 'test_servo_driver',
    'test_buzzer_driver', 'test_wifi_connection', 'test_mqtt_pubsub',
    'test_integration_pipeline'
]
for t in embedded_tests:
    files[f'test/test_embedded/{t}.cpp'] = f'''#include <unity.h>

// TODO: Implement {t.replace("test_", "")} hardware tests (runs on ESP32)

void setUp(void) {{}}
void tearDown(void) {{}}

void test_placeholder(void) {{
    TEST_ASSERT_TRUE(1);
}}

int main(void) {{
    UNITY_BEGIN();
    RUN_TEST(test_placeholder);
    return UNITY_END();
}}
'''

# ── data/ ──
files['data/config_defaults.json'] = '''{
    "calibration": {
        "zero_offset": 0,
        "scale_factor": 1.0
    },
    "network": {
        "wifi_ssid": "",
        "wifi_pass": "",
        "mqtt_broker": "mqtts://broker.dripsense.io",
        "mqtt_port": 8883
    },
    "device": {
        "device_id": "DS-ESP32-001"
    },
    "safety": {
        "low_fluid_threshold_g": 10.0,
        "free_flow_multiplier": 1.5,
        "flow_stall_timeout_ms": 30000,
        "servo_clamp_angle": 90,
        "servo_open_angle": 0
    }
}
'''

# Placeholder binary files (just create empty)
files['data/splash.bmp'] = '// Placeholder: 128x64 1-bit boot splash screen bitmap\n'
files['data/icons.bmp'] = '// Placeholder: Icon sprite sheet (Wi-Fi, lock, warning, battery)\n'

# ── scripts/ ──
files['scripts/calibrate.py'] = '''#!/usr/bin/env python3
"""Serial-based calibration automation for Drip-Sense."""

# TODO: Implement serial calibration script
# - Connect to ESP32 via serial port
# - Send AT+TARE command
# - Prompt user to place known weight
# - Send AT+CALIBRATE command
# - Verify calibration accuracy

if __name__ == "__main__":
    print("Drip-Sense Calibration Tool")
'''

files['scripts/provision_wifi.py'] = '''#!/usr/bin/env python3
"""BLE Wi-Fi provisioning script for Drip-Sense devices."""

# TODO: Implement BLE provisioning
# - Scan for DRIPSENSE-XXXX devices
# - Connect via BLE GATT
# - Write SSID and password characteristics
# - Trigger connection

if __name__ == "__main__":
    print("Drip-Sense Wi-Fi Provisioning Tool")
'''

files['scripts/ota_deploy.py'] = '''#!/usr/bin/env python3
"""OTA firmware deployment to single or batch Drip-Sense devices."""

# TODO: Implement OTA deployment
# - Read firmware binary
# - Connect to MQTT broker
# - Publish OTA notification to target devices
# - Monitor update progress

if __name__ == "__main__":
    print("Drip-Sense OTA Deployment Tool")
'''

files['scripts/generate_certs.sh'] = '''#!/bin/bash
# Generate TLS client certificates for MQTT communication
# TODO: Implement certificate generation
echo "Generating TLS certificates for Drip-Sense MQTT..."
'''

files['scripts/flash_factory.sh'] = '''#!/bin/bash
# Full factory flash: erase + bootloader + firmware
# TODO: Implement factory flash procedure
echo "Drip-Sense Factory Flash Tool"
'''

# ── tools/ ──
files['tools/serial_monitor.py'] = '''#!/usr/bin/env python3
"""Enhanced serial monitor with AT command shortcuts for Drip-Sense."""

# TODO: Implement enhanced serial monitor
if __name__ == "__main__":
    print("Drip-Sense Serial Monitor")
'''

files['tools/mqtt_dashboard.py'] = '''#!/usr/bin/env python3
"""CLI dashboard for MQTT telemetry visualization."""

# TODO: Implement CLI MQTT dashboard
if __name__ == "__main__":
    print("Drip-Sense MQTT Dashboard")
'''

files['tools/crash_decoder.py'] = '''#!/usr/bin/env python3
"""ESP32 backtrace decoder (addr2line wrapper)."""

# TODO: Implement crash decoder
if __name__ == "__main__":
    print("Drip-Sense Crash Decoder")
'''

# ── CI/CD ──
files['ci/.github/workflows/build.yml'] = '''name: Build Check
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: ~/.platformio
          key: pio-${{ hashFiles('platformio.ini') }}
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install platformio
      - run: pio run
'''

files['ci/.github/workflows/test.yml'] = '''name: Unit Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install platformio
      - run: pio test -e native
'''

files['ci/.github/workflows/release.yml'] = '''name: Release
on:
  push:
    tags: ["v*"]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install platformio
      - run: pio run
      - name: Upload firmware
        uses: actions/upload-artifact@v4
        with:
          name: firmware
          path: .pio/build/esp32dev/firmware.bin
'''

files['ci/Dockerfile'] = '''FROM python:3.11-slim

RUN pip install platformio
WORKDIR /project
COPY . .
RUN pio run
'''

# ── hardware/ (placeholder README files) ──
files['hardware/schematic/README.md'] = '''# Schematic Files
Place KiCad/EasyEDA schematic files here:
- `dripsense_schematic.kicad_sch`
- `dripsense_schematic.pdf`
'''

files['hardware/pcb/README.md'] = '''# PCB Layout Files
Place PCB layout and manufacturing files here:
- `dripsense_pcb.kicad_pcb`
- `gerber/` (manufacturing Gerber files)
- `bom.csv` (Bill of Materials)
'''

files['hardware/pcb/bom.csv'] = '''Component,Value,Package,Quantity,Reference,Cost_INR
ESP32 Dev Board,ESP32-WROOM-32,Module,1,U1,550
Load Cell + HX711,5kg + 24-bit ADC,Module,1,U2,200
Servo Motor,SG90,Motor,1,M1,150
OLED Display,0.96" SSD1306,I2C,1,D1,0
Buzzer,Piezo Active,3.3V,1,BZ1,0
Buck Converter,5V to 3.3V,Module,2,VR1-VR2,150
PCB,4-layer,Custom,1,PCB,800
'''

files['hardware/enclosure/README.md'] = '''# Enclosure Files
Place 3D-printed enclosure STL files here:
- `case_top.stl` (top shell with OLED window)
- `case_bottom.stl` (bottom shell with mounting clamp)
- `servo_bracket.stl` (servo-to-tube clamp adapter)
'''

# ── Root config files ──
files['platformio.ini'] = '''[platformio]
default_envs = esp32dev

[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
board_build.partitions = partitions.csv
monitor_speed = 115200
lib_deps =
    bogde/HX711@^0.7.5
    adafruit/Adafruit SSD1306@^2.5.7
    adafruit/Adafruit GFX Library@^1.11.5
    bblanchon/ArduinoJson@^7.0.0
    knolleary/PubSubClient@^2.8
build_flags =
    -DCORE_DEBUG_LEVEL=3
    -DBOARD_HAS_PSRAM=0

[env:native]
platform = native
test_framework = unity
build_flags = -std=c++17
'''

files['partitions.csv'] = '''# Name,    Type,  SubType, Offset,   Size,     Flags
nvs,       data,  nvs,     0x9000,   0x6000,
otadata,   data,  ota,     0xF000,   0x2000,
app0,      app,   ota_0,   0x10000,  0x180000,
app1,      app,   ota_1,   0x190000, 0x180000,
spiffs,    data,  spiffs,  0x310000, 0xF0000,
'''

files['.gitignore'] = '''.pio/
build/
*.o
*.elf
*.bin
.vscode/
.DS_Store
node_modules/
.env
.env.local
*.log
__pycache__/
.next/
'''

files['.clang-format'] = '''BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
AllowShortFunctionsOnASingleLine: Empty
BreakBeforeBraces: Attach
'''

files['LICENSE'] = '''MIT License

Copyright (c) 2026 Drip-Sense

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

files['CHANGELOG.md'] = '''# Changelog

All notable changes to Drip-Sense will be documented in this file.

## [Unreleased]

### Added
- Initial project structure and documentation
- Hardware abstraction layer (HAL) headers
- Middleware module stubs (sensor fusion, safety, state machine, event bus, config)
- Application layer stubs (monitor, UI manager, telemetry)
- Network layer stubs (Wi-Fi, MQTT, BLE provisioning, OTA)
- Test framework setup (native + embedded)
- CI/CD pipeline configuration
- Dashboard design documentation

## [1.0.0] - TBD

### Planned
- Full HAL driver implementations
- Sensor fusion pipeline
- Safety controller with servo actuation
- MQTT telemetry publishing
- Cloud dashboard (Next.js)
'''

# ── Dashboard (Next.js) ──
files['dashboard/package.json'] = '''{
    "name": "dripsense-dashboard",
    "version": "1.0.0",
    "private": true,
    "scripts": {
        "dev": "next dev",
        "build": "next build",
        "start": "next start",
        "lint": "next lint"
    },
    "dependencies": {
        "next": "^14.0.0",
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "recharts": "^2.10.0",
        "zustand": "^4.4.0",
        "socket.io-client": "^4.7.0",
        "date-fns": "^3.0.0",
        "lucide-react": "^0.300.0",
        "sonner": "^1.3.0",
        "next-auth": "^4.24.0",
        "@prisma/client": "^5.7.0"
    },
    "devDependencies": {
        "typescript": "^5.3.0",
        "@types/react": "^18.2.0",
        "@types/node": "^20.10.0",
        "prisma": "^5.7.0",
        "tailwindcss": "^3.4.0",
        "postcss": "^8.4.0",
        "autoprefixer": "^10.4.0"
    }
}
'''

files['dashboard/tsconfig.json'] = '''{
    "compilerOptions": {
        "target": "es5",
        "lib": ["dom", "dom.iterable", "esnext"],
        "allowJs": true,
        "skipLibCheck": true,
        "strict": true,
        "noEmit": true,
        "esModuleInterop": true,
        "module": "esnext",
        "moduleResolution": "bundler",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "jsx": "preserve",
        "incremental": true,
        "plugins": [{ "name": "next" }],
        "paths": { "@/*": ["./src/*"] }
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules"]
}
'''

files['dashboard/tailwind.config.ts'] = '''import type { Config } from "tailwindcss";

const config: Config = {
    content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                primary: { DEFAULT: "#6366F1", hover: "#4F46E5" },
                accent: "#06B6D4",
                surface: "#1E293B",
                card: "#334155",
            },
            fontFamily: {
                sans: ["Inter", "sans-serif"],
                mono: ["JetBrains Mono", "monospace"],
            },
        },
    },
    plugins: [],
};

export default config;
'''

files['dashboard/postcss.config.js'] = '''module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
'''

files['dashboard/next.config.js'] = '''/** @type {import("next").NextConfig} */
const nextConfig = {
    reactStrictMode: true,
};

module.exports = nextConfig;
'''

files['dashboard/.env.example'] = '''DATABASE_URL="postgresql://user:password@localhost:5432/dripsense"
MQTT_BROKER_URL="mqtt://localhost:1883"
NEXTAUTH_SECRET="your-secret-key"
NEXTAUTH_URL="http://localhost:3000"
'''

# Dashboard — App Router pages
files['dashboard/src/app/layout.tsx'] = '''import type { Metadata } from "next";
import "@/styles/globals.css";

export const metadata: Metadata = {
    title: "Drip-Sense Control Center",
    description: "Real-time IV drip monitoring dashboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en" className="dark">
            <body className="bg-slate-900 text-slate-50 font-sans">
                {/* TODO: Add sidebar layout, auth provider */}
                {children}
            </body>
        </html>
    );
}
'''

files['dashboard/src/app/page.tsx'] = '''export default function Home() {
    return (
        <main className="flex min-h-screen items-center justify-center">
            <h1 className="text-4xl font-bold">Drip-Sense Control Center</h1>
        </main>
    );
}
'''

files['dashboard/src/app/login/page.tsx'] = '''/**
 * Login Page — /login
 * Role-based authentication (Admin, Doctor, Nurse)
 */
export default function LoginPage() {
    return (
        <main className="flex min-h-screen items-center justify-center">
            <div className="rounded-xl bg-slate-800 p-8 shadow-xl">
                <h1 className="mb-6 text-2xl font-bold">Sign In</h1>
                {/* TODO: Implement login form with NextAuth.js */}
                <p className="text-slate-400">Authentication coming soon...</p>
            </div>
        </main>
    );
}
'''

files['dashboard/src/app/dashboard/page.tsx'] = '''/**
 * Dashboard Home — /dashboard
 * Ward Overview: KPI cards, bed cards grouped by ward, live alert feed
 */
export default function DashboardPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Ward Overview</h1>
            {/* TODO: KPI Summary Cards */}
            {/* TODO: Ward sections with bed cards */}
            {/* TODO: Live alert feed */}
        </div>
    );
}
'''

files['dashboard/src/app/patients/page.tsx'] = '''/**
 * Patient Management — /patients
 * Full patient database with search, filter, pagination, and manual entry
 */
export default function PatientsPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Patient Management</h1>
            {/* TODO: Search & filter bar */}
            {/* TODO: Patient data table (TanStack Table) */}
            {/* TODO: Add New Patient modal */}
        </div>
    );
}
'''

files['dashboard/src/app/patients/[patientId]/page.tsx'] = '''/**
 * Patient Detail — /patients/[patientId]
 * Live monitoring, infusion history, clinical notes
 */
export default function PatientDetailPage({
    params,
}: {
    params: { patientId: string };
}) {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Patient Detail: {params.patientId}</h1>
            {/* TODO: Patient info + current IV card */}
            {/* TODO: Live telemetry (weight/flow charts) */}
            {/* TODO: Infusion history table */}
            {/* TODO: Clinical notes section */}
        </div>
    );
}
'''

files['dashboard/src/app/alerts/page.tsx'] = '''/**
 * Alert Center — /alerts
 * Centralized alarm management: acknowledge, resolve, escalate
 */
export default function AlertsPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Alert Center</h1>
            {/* TODO: Active alerts (unacknowledged) */}
            {/* TODO: Acknowledged / resolved alerts */}
            {/* TODO: Filter by severity, ward, date */}
        </div>
    );
}
'''

files['dashboard/src/app/analytics/page.tsx'] = '''/**
 * Analytics & Reports — /analytics
 * Historical trends, ward statistics, exportable reports
 */
export default function AnalyticsPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Analytics & Reports</h1>
            {/* TODO: KPI summary cards */}
            {/* TODO: Alerts per day bar chart */}
            {/* TODO: Fluid usage by ward pie chart */}
            {/* TODO: Device uptime bars */}
            {/* TODO: Export CSV / PDF buttons */}
        </div>
    );
}
'''

files['dashboard/src/app/devices/page.tsx'] = '''/**
 * Device Management — /devices
 * Register, configure, update, and monitor all ESP32 devices
 */
export default function DevicesPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Device Management</h1>
            {/* TODO: Device list table */}
            {/* TODO: Register new device dialog */}
            {/* TODO: Bulk OTA update button */}
            {/* TODO: Device detail modal */}
        </div>
    );
}
'''

files['dashboard/src/app/settings/page.tsx'] = '''/**
 * Settings — /settings
 * System-wide configuration: roles, notifications, thresholds
 */
export default function SettingsPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Settings</h1>
            {/* TODO: Hospital profile */}
            {/* TODO: User roles (RBAC) */}
            {/* TODO: Notification rules */}
            {/* TODO: Default alert thresholds */}
            {/* TODO: Theme toggle */}
            {/* TODO: MQTT broker config */}
        </div>
    );
}
'''

# Dashboard — Components
files['dashboard/src/components/layout/Sidebar.tsx'] = '''/**
 * Sidebar navigation component
 * Links: Home, Patients, Devices, Alerts, Analytics, Settings
 */
export default function Sidebar() {
    return (
        <aside className="w-64 bg-slate-800 min-h-screen p-4">
            <h2 className="text-xl font-bold mb-8">Drip-Sense</h2>
            <nav className="space-y-2">
                {/* TODO: Nav links with active state */}
            </nav>
        </aside>
    );
}
'''

files['dashboard/src/components/layout/Header.tsx'] = '''/**
 * Header bar with notifications, user avatar, theme toggle
 */
export default function Header() {
    return (
        <header className="h-16 bg-slate-800 border-b border-slate-700 px-6 flex items-center justify-between">
            {/* TODO: Notification bell, user menu, theme toggle */}
        </header>
    );
}
'''

files['dashboard/src/components/cards/BedCard.tsx'] = '''/**
 * Bed card component showing patient status, fluid level, flow rate
 */
interface BedCardProps {
    bedNumber: number;
    patientName: string;
    fluidPercent: number;
    flowRate: number;
    eta: string;
    status: "normal" | "warning" | "critical" | "offline";
}

export default function BedCard(props: BedCardProps) {
    return (
        <div className="rounded-xl bg-slate-800/60 backdrop-blur-xl border border-slate-700/50 p-4">
            {/* TODO: Implement bed card UI */}
        </div>
    );
}
'''

files['dashboard/src/components/cards/KpiCard.tsx'] = '''/**
 * KPI summary card (active devices, alerts, avg flow, etc.)
 */
interface KpiCardProps {
    title: string;
    value: string | number;
    icon: React.ReactNode;
    trend?: string;
}

export default function KpiCard(props: KpiCardProps) {
    return (
        <div className="rounded-xl bg-slate-800/60 backdrop-blur-xl border border-slate-700/50 p-4">
            {/* TODO: Implement KPI card */}
        </div>
    );
}
'''

files['dashboard/src/components/charts/WeightChart.tsx'] = '''/**
 * Weight vs Time area chart (Recharts)
 */
export default function WeightChart() {
    return (
        <div className="rounded-xl bg-slate-800/60 p-4">
            {/* TODO: Recharts AreaChart for weight telemetry */}
        </div>
    );
}
'''

files['dashboard/src/components/charts/FlowRateChart.tsx'] = '''/**
 * Flow Rate vs Time line chart with reference line (Recharts)
 */
export default function FlowRateChart() {
    return (
        <div className="rounded-xl bg-slate-800/60 p-4">
            {/* TODO: Recharts LineChart for flow rate telemetry */}
        </div>
    );
}
'''

files['dashboard/src/components/charts/AlertsBarChart.tsx'] = '''/**
 * Alerts per day stacked bar chart (Recharts)
 */
export default function AlertsBarChart() {
    return (
        <div className="rounded-xl bg-slate-800/60 p-4">
            {/* TODO: Recharts BarChart for daily alert counts */}
        </div>
    );
}
'''

files['dashboard/src/components/ui/Badge.tsx'] = '''/**
 * Status badge component (pill-shaped, color-coded)
 */
interface BadgeProps {
    variant: "success" | "warning" | "danger" | "info" | "neutral";
    children: React.ReactNode;
}

export default function Badge({ variant, children }: BadgeProps) {
    return (
        <span className="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium">
            {children}
        </span>
    );
}
'''

files['dashboard/src/components/ui/Button.tsx'] = '''/**
 * Button component with primary, danger, ghost variants
 */
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "primary" | "danger" | "ghost";
}

export default function Button({ variant = "primary", children, ...props }: ButtonProps) {
    return (
        <button className="rounded-lg px-4 py-2 font-medium transition-all duration-300" {...props}>
            {children}
        </button>
    );
}
'''

# Dashboard — Lib, Hooks, Types, Styles
files['dashboard/src/lib/mqtt.ts'] = '''/**
 * MQTT.js WebSocket client for real-time telemetry
 */
// TODO: Initialize MQTT.js client
// TODO: Subscribe to telemetry and alert topics
// TODO: Parse incoming JSON payloads
export {};
'''

files['dashboard/src/lib/api.ts'] = '''/**
 * REST API client for dashboard backend
 */
// TODO: Implement fetch wrappers for all API endpoints
// - patients CRUD
// - infusion sessions
// - alerts
// - devices
// - analytics
export {};
'''

files['dashboard/src/lib/auth.ts'] = '''/**
 * NextAuth.js configuration for role-based auth
 */
// TODO: Configure providers (credentials)
// TODO: Set up RBAC (admin, doctor, nurse)
export {};
'''

files['dashboard/src/hooks/useTelemetry.ts'] = '''/**
 * Custom hook for real-time device telemetry via WebSocket
 */
// TODO: Subscribe to telemetry:update events
// TODO: Return latest weight, flow, eta, rssi per device
export {};
'''

files['dashboard/src/hooks/useAlerts.ts'] = '''/**
 * Custom hook for real-time alert notifications
 */
// TODO: Subscribe to alert:new and alert:resolved events
// TODO: Manage alert state with Zustand
export {};
'''

files['dashboard/src/types/index.ts'] = '''/**
 * TypeScript type definitions for Drip-Sense Dashboard
 */

export interface Patient {
    id: string;
    fullName: string;
    age: number;
    gender: string;
    bloodGroup: string;
    phone: string;
    emergencyContact: string;
    diagnosis: string;
    allergies: string;
    admittedAt: string;
    ward: string;
    bedNumber: number;
    status: "active" | "discharged";
}

export interface Device {
    deviceId: string;
    macAddress: string;
    firmwareVersion: string;
    wardId: string;
    bedNumber: number;
    lastSeen: string;
    status: "online" | "offline" | "updating";
    rssi: number;
}

export interface TelemetryData {
    deviceId: string;
    sessionId: string;
    weightG: number;
    flowRate: number;
    timeToEmpty: number;
    rssi: number;
    heapFree: number;
    receivedAt: string;
}

export interface Alert {
    id: string;
    deviceId: string;
    patientId: string;
    severity: "critical" | "warning" | "info";
    type: "low_fluid" | "free_flow" | "air_detect" | "device_offline";
    message: string;
    status: "active" | "acknowledged" | "resolved" | "escalated";
    triggeredAt: string;
    acknowledgedAt?: string;
    resolvedAt?: string;
}

export interface InfusionSession {
    id: string;
    patientId: string;
    deviceId: string;
    fluidType: string;
    volumeMl: number;
    prescribedRate: number;
    startedAt: string;
    endedAt?: string;
    totalDeliveredMl: number;
    alertCount: number;
    status: "active" | "completed" | "interrupted";
}
'''

files['dashboard/src/styles/globals.css'] = '''@tailwind base;
@tailwind components;
@tailwind utilities;

@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400&display=swap");

:root {
    --color-primary: #6366f1;
    --color-accent: #06b6d4;
    --color-success: #22c55e;
    --color-warning: #f59e0b;
    --color-danger: #ef4444;
}

body {
    font-family: "Inter", sans-serif;
}
'''

# Dashboard — Prisma schema
files['dashboard/prisma/schema.prisma'] = '''generator client {
    provider = "prisma-client-js"
}

datasource db {
    provider = "postgresql"
    url      = env("DATABASE_URL")
}

model Patient {
    id               String   @id @default(cuid())
    fullName         String
    age              Int
    gender           String
    bloodGroup       String?
    phone            String?
    emergencyContact String?
    emergencyPhone   String?
    diagnosis        String?
    allergies        String?
    photoUrl         String?
    admittedAt       DateTime @default(now())
    dischargedAt     DateTime?
    status           String   @default("active")

    sessions      InfusionSession[]
    clinicalNotes ClinicalNote[]
    alerts        Alert[]
}

model Device {
    deviceId        String   @id
    macAddress      String?  @unique
    firmwareVersion String?
    wardId          String?
    bedNumber       Int?
    lastSeen        DateTime?
    status          String   @default("offline")
    calOffset       Float?
    calScale        Float?
    calibratedAt    DateTime?

    sessions  InfusionSession[]
    telemetry Telemetry[]
    alerts    Alert[]
}

model InfusionSession {
    id              String    @id @default(cuid())
    patientId       String
    deviceId        String
    fluidType       String
    volumeMl        Int
    prescribedRate  Float
    startedAt       DateTime  @default(now())
    endedAt         DateTime?
    totalDeliveredMl Float    @default(0)
    alertCount      Int       @default(0)
    status          String    @default("active")

    patient   Patient     @relation(fields: [patientId], references: [id])
    device    Device      @relation(fields: [deviceId], references: [deviceId])
    telemetry Telemetry[]
    alerts    Alert[]
}

model Telemetry {
    id          BigInt   @id @default(autoincrement())
    deviceId    String
    sessionId   String
    weightG     Float
    flowRate    Float
    timeToEmpty Float
    rssi        Int?
    heapFree    Int?
    receivedAt  DateTime @default(now())

    device  Device          @relation(fields: [deviceId], references: [deviceId])
    session InfusionSession @relation(fields: [sessionId], references: [id])

    @@index([deviceId, receivedAt])
}

model Alert {
    id             String    @id @default(cuid())
    deviceId       String
    sessionId      String?
    patientId      String?
    severity       String
    type           String
    message        String
    status         String    @default("active")
    acknowledgedBy String?
    triggeredAt    DateTime  @default(now())
    acknowledgedAt DateTime?
    resolvedAt     DateTime?

    device  Device           @relation(fields: [deviceId], references: [deviceId])
    session InfusionSession? @relation(fields: [sessionId], references: [id])
    patient Patient?         @relation(fields: [patientId], references: [id])
}

model ClinicalNote {
    id        String   @id @default(cuid())
    patientId String
    authorId  String
    content   String
    createdAt DateTime @default(now())

    patient Patient @relation(fields: [patientId], references: [id])
}

model User {
    id           String  @id @default(cuid())
    name         String
    email        String  @unique
    role         String  @default("nurse")
    wardId       String?
    passwordHash String
}
'''

# Dashboard README
files['dashboard/README.md'] = '''# Drip-Sense Dashboard

Real-time web-based control center for monitoring all IV drip devices.

## Tech Stack

- **Next.js 14** (React, App Router)
- **Tailwind CSS 3** (styling)
- **Recharts** (charts & visualization)
- **Socket.IO / MQTT.js** (real-time data)
- **Zustand** (state management)
- **Prisma** (database ORM)
- **NextAuth.js** (authentication)

## Pages

| Page | URL | Description |
|---|---|---|
| Login | `/login` | Role-based authentication |
| Dashboard Home | `/dashboard` | Ward overview with bed cards |
| Patient Management | `/patients` | Patient database (CRUD) |
| Patient Detail | `/patients/[patientId]` | Live monitoring & history |
| Alert Center | `/alerts` | Alarm management |
| Analytics | `/analytics` | Reports & trends |
| Device Management | `/devices` | ESP32 device config |
| Settings | `/settings` | System configuration |

## Getting Started

```bash
npm install
cp .env.example .env.local
npx prisma migrate dev
npm run dev
```

Dashboard available at http://localhost:3000
'''

# ============================================================
# Create all files
# ============================================================
created = 0
for fpath, content in files.items():
    full = os.path.join(BASE, fpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(content)
    created += 1
    print(f'  [{created:3d}] {fpath}')

print(f'\n=== Total files created: {created} ===')
