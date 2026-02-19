#include "hw_buzzer.h"
#include "../config.h"

// TODO: Implement piezo buzzer driver
// - buzzer_init(): GPIO 15 as OUTPUT
// - buzzer_play(): start FreeRTOS software timer for pattern
// - buzzer_stop(): cancel timer, GPIO LOW
// - _buzzer_timer_cb(): internal timer callback for patterns
