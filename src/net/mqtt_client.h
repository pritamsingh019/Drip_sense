#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include <stdbool.h>
#include <stdint.h>

void mqtt_init(const char *broker_url, uint16_t port);
void mqtt_connect(const char *device_id, const char *token);
void mqtt_publish(const char *topic, const char *payload, int qos);
void mqtt_subscribe(const char *topic);
bool mqtt_is_connected(void);

#endif // MQTT_CLIENT_H
