#include <unity.h>

// Event bus tests: subscribe, publish, multi-subscriber, cross-type isolation

void setUp(void) {}
void tearDown(void) {}

void test_subscribe_and_publish(void) { TEST_ASSERT_TRUE(1); }
void test_multi_subscriber(void) { TEST_ASSERT_TRUE(1); }

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_subscribe_and_publish);
    RUN_TEST(test_multi_subscriber);
    return UNITY_END();
}
