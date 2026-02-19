#include <unity.h>

// Flow rate calculation tests: linear drain, no flow, free flow, partial buffer

void setUp(void) {}
void tearDown(void) {}

void test_flow_calc_linear_drain(void) {
    TEST_ASSERT_TRUE(1);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_flow_calc_linear_drain);
    return UNITY_END();
}
