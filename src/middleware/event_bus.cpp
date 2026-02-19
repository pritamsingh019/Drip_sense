#include "event_bus.h"

// TODO: Implement event publish/subscribe system
// - event_bus_init(): clear subscriber list
// - subscribe(): register callback for event type (max 8 per type)
// - publish(): iterate registered callbacks, invoke with event data
// - Uses FreeRTOS queue for thread-safe cross-core delivery
