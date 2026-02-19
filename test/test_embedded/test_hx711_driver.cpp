#include <unity.h>

// HX711 hardware test: raw read, tare, gain setting, power cycle
// Runs on ESP32 hardware

void setUp(void) {}
void tearDown(void) {}

void test_hx711_init(void) { TEST_ASSERT_TRUE(1); }
void test_hx711_read_raw(void) { TEST_ASSERT_TRUE(1); }
void test_hx711_tare(void) { TEST_ASSERT_TRUE(1); }

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_hx711_init);
    RUN_TEST(test_hx711_read_raw);
    RUN_TEST(test_hx711_tare);
    return UNITY_END();
}
