#ifndef TELEMETRY_H
#define TELEMETRY_H

void telemetry_task(void *pvParameters);
void telemetry_publish_immediate(const char *topic, const char *payload);

#endif // TELEMETRY_H
