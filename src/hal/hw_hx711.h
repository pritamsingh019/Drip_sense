#ifndef HW_HX711_H
#define HW_HX711_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint8_t pin_sck;
    uint8_t pin_dout;
    int32_t offset;
    float   scale;
} hx711_config_t;

void    hx711_init(hx711_config_t *cfg);
bool    hx711_is_ready(void);
int32_t hx711_read_raw(void);
float   hx711_read_grams(void);
void    hx711_tare(int samples);
void    hx711_set_gain(uint8_t gain);
void    hx711_power_down(void);
void    hx711_power_up(void);

#endif // HW_HX711_H
