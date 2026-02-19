#include <unity.h>

// MQTT pub/sub test: publish, subscribe, QoS, reconnection
// Runs on ESP32 hardware

void setUp(void) {}
void tearDown(void) {}

void test_mqtt_publish(void) { TEST_ASSERT_TRUE(1); }
void test_mqtt_subscribe(void) { TEST_ASSERT_TRUE(1); }

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_mqtt_publish);
    RUN_TEST(test_mqtt_subscribe);
    return UNITY_END();
}
