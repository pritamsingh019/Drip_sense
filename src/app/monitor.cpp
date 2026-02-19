#include "monitor.h"
#include "../middleware/sensor_fusion.h"
#include "../middleware/safety_ctrl.h"
#include "../middleware/event_bus.h"

// TODO: Implement monitoring engine task
// - monitor_task(): pinned to Core 1, runs at 10 Hz
//   1. Wait for HX711 data ready semaphore
//   2. Read raw ADC -> calibrate -> filter (EMA)
//   3. Update flow rate (sliding window)
//   4. Compute time-to-empty
//   5. Publish WEIGHT_UPDATE and FLOW_UPDATE events
// - monitor_get_weight(): return latest filtered weight
// - monitor_get_flow_rate(): return latest flow rate
// - monitor_get_time_to_empty(): return ETA in minutes
