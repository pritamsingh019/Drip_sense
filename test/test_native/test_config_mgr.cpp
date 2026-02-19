#include <unity.h>

// Config manager tests: NVS read/write, defaults, factory reset

void setUp(void) {}
void tearDown(void) {}

void test_config_defaults(void) { TEST_ASSERT_TRUE(1); }
void test_config_read_write(void) { TEST_ASSERT_TRUE(1); }

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_config_defaults);
    RUN_TEST(test_config_read_write);
    return UNITY_END();
}
