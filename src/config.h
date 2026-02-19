#ifndef CONFIG_H
#define CONFIG_H

// GPIO Pin Definitions
#define PIN_HX711_SCK       18
#define PIN_HX711_DOUT      19
#define PIN_OLED_SDA        21
#define PIN_OLED_SCL        22
#define PIN_SERVO_PWM       13
#define PIN_BUZZER          15
#define PIN_BUTTON_OVERRIDE  4

// Sensor Settings
#define SENSOR_SAMPLE_RATE_HZ   10
#define EMA_ALPHA               0.3f
#define TARE_SAMPLES            20

// Safety Thresholds
#define LOW_FLUID_THRESHOLD_G   10.0f
#define FREE_FLOW_MULTIPLIER    1.5f
#define FLOW_STALL_TIMEOUT_MS   30000

// Network Settings
#define MQTT_BROKER_URL     "mqtts://broker.dripsense.io"
#define MQTT_PORT           8883
#define WIFI_RETRY_MAX      5
#define MQTT_PUBLISH_INTERVAL_MS 5000

// Display Settings
#define OLED_I2C_ADDR       0x3C
#define OLED_WIDTH          128
#define OLED_HEIGHT         64
#define SCREENSAVER_TIMEOUT_MS 60000

// Servo Settings
#define SERVO_CLAMP_ANGLE   90
#define SERVO_OPEN_ANGLE    0

// Watchdog
#define WDT_TIMEOUT_SEC     5

#endif // CONFIG_H
