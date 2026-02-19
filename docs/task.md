# Drip-Sense — Software Task Checklist

> **Total Tasks:** 142  
> **Phases:** 6  
> **Legend:** `[ ]` To-Do · `[/]` In Progress · `[x]` Done

---

## Phase 1: Firmware Foundation (Weeks 1–4)

### 1.1 Project Setup
- [ ] Create PlatformIO project with `platformio.ini`
- [ ] Configure custom `partitions.csv` (nvs, otadata, app0, app1, spiffs)
- [ ] Add `.clang-format` (LLVM-based, 4-space indent, 100 col)
- [ ] Add `.gitignore` for `.pio/`, `build/`, credentials
- [ ] Define `config.h` with all GPIO pin mappings
- [ ] Define `config.h` sensor settings (sample rate, EMA alpha, tare samples)
- [ ] Define `config.h` safety thresholds (low fluid, free-flow, stall)
- [ ] Define `config.h` network settings (MQTT broker, Wi-Fi retry, OTA URL)
- [ ] Create `include/version.h` with FW_VERSION macros and build date
- [ ] Install all library dependencies (HX711, SSD1306, ESP32Servo, PubSubClient, ArduinoJson)
- [ ] Verify clean build: `pio run -e esp32dev` with zero warnings

### 1.2 HAL — HX711 Load Cell Driver
- [ ] Create `src/hal/hw_hx711.h` — structs and function declarations
- [ ] Implement `hx711_init()` — configure GPIO 18 (SCK) and GPIO 19 (DOUT)
- [ ] Implement `hx711_is_ready()` — check DOUT LOW
- [ ] Implement `hx711_read_raw()` — 24-bit bit-bang read (MSB first)
- [ ] Implement `hx711_read_grams()` — apply `(raw - offset) / scale`
- [ ] Implement `hx711_tare()` — average N samples → store as zero offset
- [ ] Implement `hx711_set_gain()` — 128/64/32 via extra clock pulses
- [ ] Implement `hx711_power_down()` — SCK HIGH > 60µs
- [ ] Implement `hx711_power_up()` — SCK LOW pulse
- [ ] Test: reads stable raw ADC values on breadboard

### 1.3 HAL — SSD1306 OLED Driver
- [ ] Create `src/hal/hw_oled.h` — function declarations
- [ ] Implement `oled_init()` — I2C at 400 kHz, address 0x3C
- [ ] Implement `oled_clear()` — zero out frame buffer
- [ ] Implement `oled_set_cursor()` — text cursor positioning
- [ ] Implement `oled_print()` — render text (1× and 2× size)
- [ ] Implement `oled_draw_icon()` — blit bitmap sprite
- [ ] Implement `oled_draw_progress_bar()` — filled rect for fluid level
- [ ] Implement `oled_display()` — flush buffer to SSD1306
- [ ] Implement `oled_set_brightness()` — contrast command (0–255)
- [ ] Implement `oled_sleep()` — display ON/OFF for power saving
- [ ] Test: text renders correctly on 128×64 display

### 1.4 HAL — Servo Motor Driver
- [ ] Create `src/hal/hw_servo.h` — function declarations
- [ ] Implement `servo_init()` — LEDC timer 0 at 50 Hz on GPIO 13
- [ ] Implement `servo_set_angle()` — map 0°–180° to 1000–2000 µs
- [ ] Implement `servo_clamp()` — move to CLAMP_ANGLE (90°)
- [ ] Implement `servo_release()` — move to OPEN_ANGLE (0°)
- [ ] Implement `servo_detach()` — stop PWM to save power
- [ ] Implement `servo_smooth_clamp()` — graduated step movement
- [ ] Test: servo moves to specified angles accurately

### 1.5 HAL — Buzzer Driver
- [ ] Create `src/hal/hw_buzzer.h` — pattern enum and declarations
- [ ] Implement `buzzer_init()` — GPIO 15 as OUTPUT
- [ ] Implement `buzzer_play()` — FreeRTOS timer for pattern (SINGLE, DOUBLE, INTERMITTENT, CONTINUOUS)
- [ ] Implement `buzzer_stop()` — cancel timer, GPIO LOW
- [ ] Implement `_buzzer_timer_cb()` — internal timer callback
- [ ] Test: all 4 patterns audibly distinct

### 1.6 NVS Configuration Manager
- [ ] Create `src/middleware/config_mgr.h` — function declarations
- [ ] Implement `config_init()` — open NVS namespaces (cal, net, dev, safety)
- [ ] Implement `config_load()` — read all params into runtime struct
- [ ] Implement `config_save()` — write modified params to NVS
- [ ] Implement `config_get_float()` / `config_set_float()` — typed accessors
- [ ] Implement `config_get_string()` / `config_set_string()`
- [ ] Implement `config_factory_reset()` — erase all namespaces, reboot
- [ ] Test: persists across reboot; factory reset erases all

### 1.7 Main Entry Point
- [ ] Create `src/main.cpp` — `setup()` with HAL init, NVS load, splash screen
- [ ] Create FreeRTOS task creation stubs (sensor, safety, UI, telemetry)
- [ ] Verify: device boots, shows splash, enters idle state

---

## Phase 2: Sensor Pipeline & Safety System (Weeks 5–7)

### 2.1 EMA Filter
- [ ] Create `src/middleware/sensor_fusion.h` — structs and declarations
- [ ] Implement `ema_init()` — set alpha, clear initialized flag
- [ ] Implement `ema_update()` — `y = α·x + (1−α)·y_prev`
- [ ] Write unit test `test_ema_filter.cpp` — init, convergence, step response, noise rejection
- [ ] Verify: noise reduced by ≥ 60% at default α=0.3

### 2.2 Kalman Filter
- [ ] Implement `kalman_init()` — set Q, R, initial P=1.0
- [ ] Implement `kalman_update()` — predict → update cycle
- [ ] Write unit test `test_kalman_filter.cpp` — convergence, Q/R tuning, outlier handling
- [ ] Verify: converges within 20 samples on constant signal

### 2.3 Flow Rate Calculator
- [ ] Implement `flow_calc_update()` — sliding window Δweight/Δtime
- [ ] Convert g/s → mL/min using configurable fluid density
- [ ] Implement time-to-empty: `weight / (rate × density)`
- [ ] Write unit test `test_flow_calc.cpp` — linear drain, no flow, free flow, partial buffer
- [ ] Verify: accuracy within ±10% of known pump rate

### 2.4 Safety Controller
- [ ] Create `src/middleware/safety_ctrl.h` — structs and declarations
- [ ] Implement `detect_low_fluid()` — weight < threshold with 3-sample debounce
- [ ] Implement `detect_free_flow()` — rate > expected × multiplier with 5-sample debounce
- [ ] Implement `detect_flow_stall()` — Δweight < 0.5g for timeout period
- [ ] Implement sensor fault detection — HX711 data-ready timeout > 1s
- [ ] Implement `evaluate_safety()` — master function calling all detectors
- [ ] Write unit test `test_anomaly_detection.cpp` — all 4 anomaly types + debounce
- [ ] Verify: low fluid triggers reliably; no false positives from vibration

### 2.5 State Machine
- [ ] Create `src/middleware/state_machine.h` — state enum and declarations
- [ ] Implement `state_init()` — set initial state to IDLE
- [ ] Implement `state_transition()` — validate allowed transitions, log changes
- [ ] Implement `state_get_current()` / `state_get_name()`
- [ ] Write unit test `test_state_machine.cpp` — valid, invalid, edge cases
- [ ] Verify: invalid transitions rejected; valid ones logged

### 2.6 Event Bus
- [ ] Create `src/middleware/event_bus.h` — event types, data union, callback type
- [ ] Implement `event_bus_init()` — clear subscriber list
- [ ] Implement `subscribe()` — register callback for event type (max 8)
- [ ] Implement `publish()` — invoke callbacks with FreeRTOS queue for cross-core delivery
- [ ] Write unit test `test_event_bus.cpp` — subscribe, publish, multi-subscriber
- [ ] Verify: events delivered within 10ms across cores

### 2.7 Monitoring Task
- [ ] Create `src/app/monitor.h` / `monitor.cpp`
- [ ] Implement `monitor_task()` — pinned to Core 1, 10 Hz loop
- [ ] Pipeline: wait semaphore → read ADC → calibrate → filter → flow → safety → publish
- [ ] Implement `monitor_get_weight()` / `monitor_get_flow_rate()` / `monitor_get_time_to_empty()`
- [ ] Verify: stable 10 Hz cadence; no deadline misses

---

## Phase 3: User Interface & Cloud Connectivity (Weeks 8–9)

### 3.1 OLED UI Manager
- [ ] Create `src/app/ui_mgr.h` / `ui_mgr.cpp`
- [ ] Implement `ui_task()` — pinned to Core 0, 2 Hz (500 ms)
- [ ] Subscribe to WEIGHT_UPDATE, ALARM, STATE_CHANGE events
- [ ] Implement main display: status bar + weight + flow + ETA + progress bar
- [ ] Implement Wi-Fi icon (RSSI-based: 4/2/1 bars, disconnected)
- [ ] Implement `ui_show_splash()` — logo + version for 2s on boot
- [ ] Implement `ui_show_calibration()` — step-by-step calibration screen
- [ ] Implement `ui_show_alarm()` — flashing alarm screen + alarm type
- [ ] Implement screen saver — dim after 60s of no alarms
- [ ] Implement page cycling (button short press: 4 pages)
- [ ] Verify: all values readable at arm's length

### 3.2 Buzzer Integration
- [ ] Map buzzer patterns to alarm types (cal complete, low fluid, emergency, Wi-Fi)
- [ ] Verify: patterns audibly distinct at 2m distance

### 3.3 Button Handler
- [ ] Implement button ISR with debounce
- [ ] Short press: cycle display pages
- [ ] Hold 3s: enter calibration mode
- [ ] Hold 10s: factory reset (with countdown)
- [ ] Verify: all 3 modes work reliably

### 3.4 Wi-Fi Manager
- [ ] Create `src/net/wifi_mgr.h` / `wifi_mgr.cpp`
- [ ] Implement `wifi_init()` — STA mode
- [ ] Implement `wifi_connect()` — non-blocking with exponential backoff
- [ ] Implement `wifi_event_handler()` — CONNECTED, GOT_IP, DISCONNECTED → event bus
- [ ] Implement `wifi_get_rssi()` / `wifi_get_ip()` / `wifi_is_connected()`
- [ ] Verify: connects within 10s; auto-reconnects on dropout

### 3.5 MQTT Client
- [ ] Create `src/net/mqtt_client.h` / `mqtt_client.cpp`
- [ ] Implement `mqtt_init()` — broker URL, port 8883, TLS cert
- [ ] Implement `mqtt_connect()` — device_id + token auth
- [ ] Implement `mqtt_publish()` — topic + payload + QoS
- [ ] Implement `mqtt_subscribe()` — config/set and ota/notify topics
- [ ] Implement `mqtt_callback()` — handle config push and OTA trigger
- [ ] Verify: publishes telemetry at 5s intervals; alerts at QoS 1

### 3.6 Telemetry Publisher
- [ ] Create `src/app/telemetry.h` / `telemetry.cpp`
- [ ] Implement `telemetry_task()` — Core 0, 5s interval
- [ ] Build JSON payload with ArduinoJson (matching API spec schema)
- [ ] Publish to `dripsense/{device_id}/telemetry` (QoS 0)
- [ ] Implement `telemetry_publish_immediate()` — for alerts (QoS 1)
- [ ] Verify: valid JSON; all fields present; alert reaches broker within 500ms

### 3.7 BLE Provisioning
- [ ] Create `src/net/ble_prov.h` / `ble_prov.cpp`
- [ ] Implement GATT server with provisioning service
- [ ] Advertise as "DRIPSENSE-XXXX"
- [ ] Characteristics: SSID (write), Password (write), Command (write), Status (notify)
- [ ] Verify: phone app connects and provisions Wi-Fi

### 3.8 AT Command Interface
- [ ] Create `lib/at_command/at_parser.h` / `at_parser.cpp`
- [ ] Implement AT+HELP, AT+VERSION, AT+REBOOT (built-in)
- [ ] Register all 17 debug commands (STATUS, WEIGHT, FLOW, HEAP, etc.)
- [ ] Verify: all commands respond correctly via serial

---

## Phase 4: Integration, Testing & Validation (Weeks 10–11)

### 4.1 Integration Tests
- [ ] T-INT-01: Place known weight → OLED shows ±1g
- [ ] T-INT-02: Gradually remove weight → clamp triggers within 2s
- [ ] T-INT-03: Rapid weight decrease → clamp + MQTT alert published
- [ ] T-INT-04: Press override button → servo releases, monitoring resumes
- [ ] T-INT-05: Wi-Fi → MQTT full publish cycle
- [ ] T-INT-06: Wi-Fi dropout → auto-reconnect → MQTT resumes
- [ ] T-INT-07: Calibrate → reboot → calibration intact from NVS
- [ ] T-INT-08: Alarm triggers OLED + buzzer + MQTT within 500ms

### 4.2 Hardware-in-the-Loop Tests
- [ ] Set up HIL bench (peristaltic pump + reservoir + test PC)
- [ ] T-HIL-01: Weight accuracy sweep (50, 100, 200, 500, 1000g) → ±1g
- [ ] T-HIL-02: Flow rate at 1, 2, 5, 10 mL/min → ±10%
- [ ] T-HIL-03: Run bag to empty → auto-clamp at threshold
- [ ] T-HIL-05: OTA update while monitoring → update succeeds, monitoring resumes
- [ ] T-HIL-07: Power cycle recovery → resumes within 6s

### 4.3 Safety Validation
- [ ] T-SAFE-01: HX711 disconnect → clamp + alarm within 2s
- [ ] T-SAFE-02: OLED disconnect → monitoring continues, buzzer works
- [ ] T-SAFE-04: Wi-Fi AP off → local monitoring continues
- [ ] T-SAFE-05: NVS corrupt → boots with defaults, prompts recal
- [ ] T-SOAK-01: 72-hour soak test → no crashes, heap stable, no false alarms
- [ ] T-ENV-01: Operation at 10°C → weight drift < 2g
- [ ] T-ENV-02: Operation at 45°C → weight drift < 2g
- [ ] Generate JUnit XML test report

---

## Phase 5: Production & Dashboard (Weeks 12–13)

### 5.1 OTA Manager
- [ ] Create `src/net/ota_mgr.h` / `ota_mgr.cpp`
- [ ] Implement `ota_init()` — register MQTT handler for `ota/notify`
- [ ] Implement `ota_check()` — compare current vs server version
- [ ] Implement `ota_start_update()` — download → SHA-256 verify → swap partition → reboot
- [ ] Implement `ota_rollback()` — switch boot to previous partition
- [ ] Implement auto-rollback after 3 crashes within 60s
- [ ] Verify: firmware updates successfully; rollback works

### 5.2 CI/CD Pipeline
- [ ] Create `ci/.github/workflows/build.yml` — compile on push
- [ ] Create `ci/.github/workflows/test.yml` — run native tests on push
- [ ] Create `ci/.github/workflows/release.yml` — build binary + deploy on tag
- [ ] Create `ci/Dockerfile` — reproducible CI container
- [ ] Verify: same binary locally and in CI

### 5.3 Dashboard — Project Setup
- [ ] Initialize Next.js 14 project in `dashboard/`
- [ ] Install shadcn/ui + Tailwind CSS 3 + Radix Primitives
- [ ] Configure dark theme as default (Slate-900 background)
- [ ] Set up Inter + JetBrains Mono fonts
- [ ] Set up NextAuth.js authentication (email/password + Google)
- [ ] Set up Prisma ORM + PostgreSQL schema
- [ ] Run initial migration: `npx prisma migrate dev`
- [ ] Seed database with sample patients, devices, sessions

### 5.4 Dashboard — Layout & Navigation
- [ ] Build sidebar layout (collapsible, icons + labels)
- [ ] Build top bar (hospital name, notifications bell, user avatar, theme toggle)
- [ ] Build mobile bottom tab navigation
- [ ] Set up Next.js file-based routing for all 7 pages
- [ ] Add page transition animations (fade + slide-up)

### 5.5 Dashboard — Ward Overview Page
- [ ] Build KPI summary cards (active devices, normal, alerts, avg flow)
- [ ] Build ward section with grouped bed cards
- [ ] Build bed card component (patient name, fluid bar, flow rate, ETA, status)
- [ ] Build live alert feed (scrolling, chronological)
- [ ] Integrate WebSocket for real-time data push (Socket.IO or MQTT.js)
- [ ] Auto-refresh every 3 seconds
- [ ] Color-coded status: 🟢 Normal, 🟡 Warning, 🔴 Critical, ⚫ Offline

### 5.6 Dashboard — Patient Management Page
- [ ] Build patient list table (TanStack Table: sort, search, filter, paginate)
- [ ] Build "Add New Patient" modal form
- [ ] Form fields: ID, name, age, gender, blood group, contact, emergency
- [ ] Form fields: ward, bed, doctor, diagnosis, allergies
- [ ] Form fields: fluid type, volume, prescribed rate, device link
- [ ] Implement `POST /api/patients` endpoint
- [ ] Implement `GET /api/patients` with pagination + search
- [ ] Implement `PUT /api/patients/:id` for edits
- [ ] Implement `DELETE /api/patients/:id` (soft delete / discharge)

### 5.7 Dashboard — Patient Detail Page
- [ ] Build patient info card (identity + admission details)
- [ ] Build current IV card (fluid, volume, device, start time)
- [ ] Build live telemetry cards (weight, flow, ETA, status)
- [ ] Build weight-over-time area chart (Recharts, gradient fill)
- [ ] Build flow-rate line chart with prescribed-rate reference line
- [ ] Build infusion history table (past sessions)
- [ ] Build clinical notes section (timestamped, add-note form)
- [ ] Implement `GET /api/patients/:id` with sessions + notes
- [ ] Implement `POST /api/patients/:id/notes`

### 5.8 Dashboard — Alert Center Page
- [ ] Build active alerts list (unacknowledged, sorted by severity)
- [ ] Build alert card (severity badge, time, patient, device, message)
- [ ] Build acknowledge / escalate / resolve action buttons
- [ ] Build acknowledged/resolved history section
- [ ] Implement `GET /api/alerts` with filters
- [ ] Implement `PUT /api/alerts/:id/acknowledge`
- [ ] Implement `PUT /api/alerts/:id/resolve`
- [ ] Push notification toast (Sonner) on new alert

### 5.9 Dashboard — Analytics Page
- [ ] Build KPI summary row (total sessions, avg duration, alert count, fluid consumed)
- [ ] Build alerts-per-day stacked bar chart
- [ ] Build fluid-usage-by-ward pie/donut chart
- [ ] Build device-uptime horizontal bar chart
- [ ] Build date range picker filter
- [ ] Implement `GET /api/analytics/summary`
- [ ] Implement CSV export: `GET /api/analytics/export?format=csv`

### 5.10 Dashboard — Device Management Page
- [ ] Build device list table (ID, ward, bed, firmware, status, RSSI)
- [ ] Build device detail modal (config, calibration, health, OTA, logs)
- [ ] Build remote config editor (push changes via MQTT)
- [ ] Build OTA trigger button (single device + bulk)
- [ ] Implement `GET/POST/PUT /api/devices` endpoints

### 5.11 Dashboard — Settings Page
- [ ] Build hospital profile editor
- [ ] Build user management (RBAC: Admin, Doctor, Nurse)
- [ ] Build notification rules editor (recipients per severity)
- [ ] Build default threshold editor (apply to all devices)
- [ ] Build theme toggle (dark/light)

---

## Phase 6: Deployment & Field Monitoring (Weeks 14–16)

### 6.1 Production Hardware
- [ ] Complete KiCad schematic capture and review
- [ ] Complete 4-layer PCB layout (DRC clean)
- [ ] Submit Gerber files to fabrication house
- [ ] Assemble 10 PCBs (5 pilot + 5 spare)
- [ ] 3D-print enclosures (top shell + bottom + servo bracket)
- [ ] Flash production firmware to all units
- [ ] Calibrate all units with certified weights

### 6.2 Pilot Deployment
- [ ] Site survey: verify Wi-Fi RSSI > -70 dBm at all bed positions
- [ ] Provision all devices (Wi-Fi + MQTT)
- [ ] Deploy 5 units on IV poles in one ward
- [ ] Conduct 30-min nurse training session
- [ ] Verify all 5 units publishing to cloud dashboard

### 6.3 Field Monitoring
- [ ] Monitor telemetry dashboard for 14 days
- [ ] Track: false alarm rate (target: < 1/device/day)
- [ ] Track: uptime (target: > 99.5%)
- [ ] Collect nurse feedback via Likert-scale survey (target: > 80% approval)
- [ ] Spot-check 3 devices with calibrated weights (target: ±1g)
- [ ] Triage and OTA-fix any bugs discovered

### 6.4 Documentation & Handoff
- [ ] Update docs with pilot learnings
- [ ] Create 5-minute training video script
- [ ] Publish docs to GitHub Pages
- [ ] Archive pilot telemetry data for analysis
- [ ] Write CHANGELOG.md for v1.0.0 release
- [ ] Tag `v1.0.0` release on GitHub

---

> **Last Updated:** 2026-02-19  
> **Total:** 142 tasks across 6 phases
