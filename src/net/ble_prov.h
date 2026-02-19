#ifndef BLE_PROV_H
#define BLE_PROV_H

#include <stdbool.h>

void ble_prov_init(void);
void ble_prov_start(void);
void ble_prov_stop(void);
bool ble_prov_is_active(void);

#endif // BLE_PROV_H
