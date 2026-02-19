#ifndef HW_SERVO_H
#define HW_SERVO_H

#include <stdint.h>

void servo_init(void);
void servo_set_angle(uint8_t angle);
void servo_clamp(void);
void servo_release(void);
void servo_detach(void);
void servo_smooth_clamp(uint16_t step_delay_ms);

#endif // HW_SERVO_H
