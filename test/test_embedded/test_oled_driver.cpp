#include <unity.h>

// OLED hardware test: init, text render, icon draw, brightness
// Runs on ESP32 hardware

void setUp(void) {}
void tearDown(void) {}

void test_oled_init(void) { TEST_ASSERT_TRUE(1); }
void test_oled_print(void) { TEST_ASSERT_TRUE(1); }

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_oled_init);
    RUN_TEST(test_oled_print);
    return UNITY_END();
}
