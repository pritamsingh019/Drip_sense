#ifndef SENSOR_FUSION_H
#define SENSOR_FUSION_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    float alpha;
    float last_value;
    bool  initialized;
} ema_filter_t;

typedef struct {
    float x_est;
    float P;
    float Q;
    float R;
    float K;
} kalman_1d_t;

typedef struct {
    float   *ring_buffer;
    uint16_t index;
    bool     full;
} flow_calc_t;

void  ema_init(ema_filter_t *f, float alpha);
float ema_update(ema_filter_t *f, float new_value);
void  kalman_init(kalman_1d_t *k, float Q, float R);
float kalman_update(kalman_1d_t *k, float measurement);
float flow_calc_update(flow_calc_t *fc, float weight_g, uint32_t timestamp_ms);

#endif // SENSOR_FUSION_H
