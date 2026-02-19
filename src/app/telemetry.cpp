#include "telemetry.h"
#include "../net/mqtt_client.h"
#include "../middleware/event_bus.h"

// TODO: Implement MQTT telemetry publisher
// - telemetry_task(): pinned to Core 0, interval = 5s
//   1. Collect latest sensor data from monitor module
//   2. Build JSON payload (ArduinoJson)
//   3. Publish to dripsense/{device_id}/telemetry (QoS 0)
// - telemetry_publish_immediate(): for alerts (QoS 1)
