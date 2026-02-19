#include "ble_prov.h"

// TODO: Implement BLE Wi-Fi provisioning
// - ble_prov_init(): set up GATT server with provisioning service
// - ble_prov_start(): advertise as "DRIPSENSE-XXXX"
// - Characteristics: SSID (write), Password (write),
//   Command (write: connect/scan), Status (notify)
// - ble_prov_stop(): stop advertising, free resources
