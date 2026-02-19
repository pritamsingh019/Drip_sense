#include "ota_mgr.h"

// TODO: Implement OTA update manager
// - ota_init(): register MQTT handler for ota/notify topic
// - ota_check(): compare current version with server latest
// - ota_start_update(): download binary -> write to inactive partition
//   -> SHA-256 verify -> set boot partition -> restart
// - ota_rollback(): switch boot back to previous partition
// - ota_get_partition_info(): return active/inactive partition labels
