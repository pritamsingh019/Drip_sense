#ifndef SAFETY_CTRL_H
#define SAFETY_CTRL_H

#include <stdint.h>
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

#endif // SAFETY_CTRL_H
