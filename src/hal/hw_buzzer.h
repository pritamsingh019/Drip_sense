#ifndef HW_BUZZER_H
#define HW_BUZZER_H

typedef enum {
    BUZZER_PATTERN_SINGLE,
    BUZZER_PATTERN_DOUBLE,
    BUZZER_PATTERN_INTERMITTENT,
    BUZZER_PATTERN_CONTINUOUS,
    BUZZER_PATTERN_OFF
} buzzer_pattern_t;

void buzzer_init(void);
void buzzer_play(buzzer_pattern_t pattern);
void buzzer_stop(void);

#endif // HW_BUZZER_H
