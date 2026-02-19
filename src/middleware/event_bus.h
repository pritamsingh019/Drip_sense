#ifndef EVENT_BUS_H
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

#endif // EVENT_BUS_H
