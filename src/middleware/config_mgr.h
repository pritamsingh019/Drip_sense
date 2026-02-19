#ifndef CONFIG_MGR_H
#define CONFIG_MGR_H

#include <stdbool.h>

void  config_init(void);
bool  config_load(void);
bool  config_save(void);
float config_get_float(const char *ns, const char *key, float default_val);
bool  config_set_float(const char *ns, const char *key, float value);
const char* config_get_string(const char *ns, const char *key, const char *default_val);
bool  config_set_string(const char *ns, const char *key, const char *value);
void  config_factory_reset(void);

#endif // CONFIG_MGR_H
