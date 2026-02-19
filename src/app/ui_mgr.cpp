#include "ui_mgr.h"
#include "../hal/hw_oled.h"
#include "../hal/hw_buzzer.h"
#include "../middleware/event_bus.h"

// TODO: Implement UI manager (OLED + Buzzer)
// - ui_task(): pinned to Core 0, runs at 2 Hz (500 ms)
//   1. Subscribe to WEIGHT_UPDATE, ALARM, STATE_CHANGE events
//   2. Compose OLED frame: status bar + weight + flow + ETA
//   3. Draw Wi-Fi icon based on RSSI
//   4. Flush to display
// - ui_show_splash(): logo + version for 2s on boot
// - ui_show_calibration(): step-by-step calibration UI
// - ui_show_alarm(): flashing alarm screen + buzzer pattern
