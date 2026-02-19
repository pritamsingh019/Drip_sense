#ifndef WIFI_MGR_H
#define WIFI_MGR_H

#include <stdbool.h>
#include <stdint.h>

void wifi_init(void);
void wifi_connect(const char *ssid, const char *password);
void wifi_disconnect(void);
int8_t wifi_get_rssi(void);
const char* wifi_get_ip(void);
bool wifi_is_connected(void);
void wifi_scan(void);

#endif // WIFI_MGR_H
