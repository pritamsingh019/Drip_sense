#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

#include <stdbool.h>

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

#endif // STATE_MACHINE_H
