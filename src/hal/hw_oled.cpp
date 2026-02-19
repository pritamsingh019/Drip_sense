#include "hw_oled.h"
#include "../config.h"

// TODO: Implement SSD1306 OLED display driver
// - oled_init(): I2C bus setup on GPIO 21 (SDA) / 22 (SCL) at 400 kHz, address 0x3C
// - oled_clear(): zero out 1 KB frame buffer
// - oled_set_cursor(): position text cursor (x, y)
// - oled_print(): render text with font size (1x or 2x)
// - oled_draw_icon(): blit bitmap sprite at (x, y)
// - oled_draw_progress_bar(): filled rect for fluid level %
// - oled_display(): flush frame buffer to SSD1306 over I2C
// - oled_set_brightness(): send contrast command (0-255)
// - oled_sleep(): display ON/OFF for power saving
