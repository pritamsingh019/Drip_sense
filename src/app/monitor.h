#ifndef MONITOR_H
#define MONITOR_H

void  monitor_task(void *pvParameters);
float monitor_get_weight(void);
float monitor_get_flow_rate(void);
float monitor_get_time_to_empty(void);

#endif // MONITOR_H
