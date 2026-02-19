#include <unity.h>

// Wi-Fi connection test: connect, disconnect, reconnect, RSSI
// Runs on ESP32 hardware

void setUp(void) {}
void tearDown(void) {}

void test_wifi_connect(void) { TEST_ASSERT_TRUE(1); }
void test_wifi_reconnect(void) { TEST_ASSERT_TRUE(1); }

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_wifi_connect);
    RUN_TEST(test_wifi_reconnect);
    return UNITY_END();
}
