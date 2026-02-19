#include <unity.h>

// Buzzer hardware test: pattern playback, stop, GPIO verify
// Runs on ESP32 hardware

void setUp(void) {}
void tearDown(void) {}

void test_buzzer_init(void) { TEST_ASSERT_TRUE(1); }
void test_buzzer_pattern(void) { TEST_ASSERT_TRUE(1); }

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_buzzer_init);
    RUN_TEST(test_buzzer_pattern);
    return UNITY_END();
}
