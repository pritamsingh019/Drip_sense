#ifndef UI_MGR_H
#define UI_MGR_H

void ui_task(void *pvParameters);
void ui_show_splash(void);
void ui_show_calibration(void);
void ui_show_alarm(int alarm_type);

#endif // UI_MGR_H
