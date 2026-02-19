#include "sensor_fusion.h"

// TODO: Implement signal processing pipeline
// - ema_init(): set alpha, clear initialized flag
// - ema_update(): y = alpha*x + (1-alpha)*y_prev
// - kalman_init(): set Q, R, initial P=1.0
// - kalman_update(): predict -> update cycle
// - flow_calc_update(): sliding window delta_weight/delta_time, convert g/s -> mL/min
