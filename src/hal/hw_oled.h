#ifndef HW_OLED_H
#define HW_OLED_H

#include <stdint.h>
#include <stdbool.h>

void oled_init(void);
void oled_clear(void);
void oled_set_cursor(uint8_t x, uint8_t y);
void oled_print(const char *text, uint8_t font_size);
void oled_draw_icon(const uint8_t *bitmap, uint8_t x, uint8_t y);
void oled_draw_progress_bar(uint8_t x, uint8_t y, uint8_t w, uint8_t h, uint8_t percent);
void oled_display(void);
void oled_set_brightness(uint8_t level);
void oled_sleep(bool enable);

#endif // HW_OLED_H
