#ifndef OTA_MGR_H
#define OTA_MGR_H

#include <stdbool.h>

void ota_init(void);
bool ota_check(void);
void ota_start_update(const char *url);
void ota_rollback(void);
void ota_get_partition_info(char *active, char *inactive);

#endif // OTA_MGR_H
