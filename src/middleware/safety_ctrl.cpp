#include "safety_ctrl.h"
#include "../config.h"

// TODO: Implement safety controller
// - detect_low_fluid(): weight < threshold with 3-sample debounce
// - detect_free_flow(): rate > expected*multiplier with 5-sample debounce
// - detect_flow_stall(): delta_weight < 0.5g for timeout period
// - evaluate_safety(): master function calling all detectors, returns safety_event_t
