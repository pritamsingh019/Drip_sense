#include "hw_hx711.h"
#include "../config.h"

// TODO: Implement HX711 ADC driver
// - hx711_init(): configure GPIO 18 (SCK) and GPIO 19 (DOUT)
// - hx711_is_ready(): check DOUT LOW for data ready
// - hx711_read_raw(): read 24-bit signed value (MSB first)
// - hx711_read_grams(): apply (raw - offset) / scale_factor
// - hx711_tare(): average N samples -> store as zero_offset
// - hx711_set_gain(): set 128/64/32 via extra clock pulses
// - hx711_power_down(): SCK HIGH > 60us
// - hx711_power_up(): SCK LOW pulse
