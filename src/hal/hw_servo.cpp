#include "hw_servo.h"
#include "../config.h"

// TODO: Implement Servo motor PWM driver
// - servo_init(): LEDC timer 0 at 50 Hz, 16-bit resolution on GPIO 13
// - servo_set_angle(): map 0-180 -> 1000-2000 us duty
// - servo_clamp(): move to SERVO_CLAMP_ANGLE (default 90)
// - servo_release(): move to SERVO_OPEN_ANGLE (default 0)
// - servo_detach(): stop PWM to eliminate jitter & save power
// - servo_smooth_clamp(): graduated step movement over time
