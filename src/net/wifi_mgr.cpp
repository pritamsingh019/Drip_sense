#include "wifi_mgr.h"

// TODO: Implement Wi-Fi connection manager
// - wifi_init(): initialize ESP32 Wi-Fi in STA mode
// - wifi_connect(): non-blocking connect with retry logic (exponential backoff)
// - wifi_disconnect(): clean disconnection
// - wifi_event_handler(): handle STA_CONNECTED, GOT_IP, DISCONNECTED events
// - wifi_get_rssi(): return current signal strength (dBm)
// - wifi_scan(): scan for nearby APs, return SSID list
