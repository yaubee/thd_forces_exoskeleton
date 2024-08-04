#include <Adafruit_LSM6DSO32.h>
#include <Wire.h>
#include <MovingAverageFloat.h>
#include <DHT.h>
#include <AS5048A.h>

/***** Moving Average Configuration *****/
MovingAverageFloat<16> filter0;

/***** Temperature Sensor Configuration *****/
#define DHTPIN 9
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

/***** Angle Sensor Configuration *****/
AS5048A angleSensor(10, true);

/***** IMU Sensor Configuration *****/
Adafruit_LSM6DSO32 dso32;
Adafruit_LSM6DSO32 dso32_2; // To be used if you have a second sensor

#define TCAADDR 0x70
const int tavg_imu = 10; // Moving average time interval in microseconds

void tcaselect(uint8_t i) {
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(100);

  // Initialize sensors
  tcaselect(0);
  dso32.begin_I2C();
  dso32.setAccelRange(LSM6DSO32_ACCEL_RANGE_16_G);
  dso32.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  dso32.setAccelDataRate(LSM6DS_RATE_12_5_HZ);
  dso32.setGyroDataRate(LSM6DS_RATE_12_5_HZ);

  dht.begin();
  angleSensor.begin();
}

void loop() {
  float temperature = dht.readTemperature();
  float angle_value = angleSensor.getRotationInDegrees() * 100;

  char values_of_angle[10];
  dtostrf(angle_value, 3, 0, values_of_angle);

  float imu0_val = getAveragedIMUValue();

  Serial.print(temperature);
  Serial.print(',');
  Serial.print(values_of_angle);
  Serial.print(',');
  Serial.print(imu0_val);
  Serial.println();

  delay(50);
}

float getAveragedIMUValue() {
  tcaselect(0);

  sensors_event_t accel, gyro, temp;
  dso32.getEvent(&accel, &gyro, &temp);

  float data0;
  const int num_samples = 10;

  filter0.clear(); // Ensure filter is reset before new measurements

  for (int i = 0; i < num_samples; i++) {
    data0 = gyro.gyro.z * 100;
    filter0.add(data0);
    delayMicroseconds(tavg_imu);
  }

  return filter0.get();
}
