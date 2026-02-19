#include "config_mgr.h"

// TODO: Implement NVS configuration manager
// - config_init(): open NVS flash, create namespaces (cal, net, dev, safety)
// - config_load(): read all stored params into runtime struct
// - config_save(): write modified params back to NVS
// - config_get/set_float/string(): typed accessors with defaults
// - config_factory_reset(): erase all namespaces, reboot
