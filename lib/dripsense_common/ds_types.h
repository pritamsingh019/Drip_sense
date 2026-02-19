#ifndef DS_TYPES_H
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
    ALARM_NONE,
    ALARM_LOW_FLUID,
    ALARM_FREE_FLOW,
    ALARM_AIR_DETECT,
    ALARM_SENSOR_FAIL
} alarm_event_t;

typedef struct {
    float    weight_g;
    float    flow_rate;
    float    eta_min;
    int8_t   rssi;
    uint32_t heap_free;
    uint32_t uptime_sec;
} device_status_t;

#endif // DS_TYPES_H
