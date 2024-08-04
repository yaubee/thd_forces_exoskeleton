#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <Adafruit_LSM6DSO32.h>
#include <MovingAverageFloat.h>
#include <DHT.h>
#include <AS5048A.h>

/***** Constants *****/
#define BNO055_SAMPLERATE_DELAY_MS (50)
#define DHTPIN 7
#define DHTTYPE DHT22
#define TCAADDR 0x70
#define MOVING_AVERAGE_SIZE 16
#define TAVG_IMU 10 // Microseconds for moving average time interval

/***** Sensor Instances *****/
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28);
Adafruit_LSM6DSO32 dso32;
DHT dht(DHTPIN, DHTTYPE);
AS5048A angleSensor(10, true);
MovingAverageFloat<MOVING_AVERAGE_SIZE> filter0;

/***** Function Declarations *****/
void tcaselect(uint8_t i);
float getAveragedIMUValue();

/***** Setup *****/
void setup() {
  Serial.begin(9600);
  Wire.begin();
  delay(100);

  // Initialize sensors
  dht.begin();
  angleSensor.begin();

  // Initialize BNO055 sensor
  if (!bno.begin()) {
    Serial.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }
}

/***** Main Loop *****/
void loop() {
  // Read temperature
  float temperature = dht.readTemperature();

  // Read angle
  int angle_value = angleSensor.getRawRotation();

  // Read sensor data from BNO055
  sensors_event_t orientationData, angVelocityData, linearAccelData, magnetometerData, accelerometerData, gravityData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_GYROSCOPE);
  bno.getEvent(&linearAccelData, Adafruit_BNO055::VECTOR_LINEARACCEL);
  bno.getEvent(&magnetometerData, Adafruit_BNO055::VECTOR_MAGNETOMETER);
  bno.getEvent(&accelerometerData, Adafruit_BNO055::VECTOR_ACCELEROMETER);
  bno.getEvent(&gravityData, Adafruit_BNO055::VECTOR_GRAVITY);

  // Process data
  float gx = angVelocityData.gyro.x;
  float gz = angVelocityData.gyro.z;
  float ax = accelerometerData.acceleration.x;
  float az = accelerometerData.acceleration.z;

  // Scale values
  int axx = ax * 100;
  int gzz = gz * 100;

  // Print results
  Serial.print(temperature); Serial.print(",");
  Serial.print(angle_value); Serial.print(",");
  Serial.print(axx); Serial.print(",");
  Serial.println(gzz);

  delay(BNO055_SAMPLERATE_DELAY_MS);
}

/***** Utility Functions *****/
void tcaselect(uint8_t i) {
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
}

float getAveragedIMUValue() {
  tcaselect(0);
  sensors_event_t accel, gyro, temp;
  dso32.getEvent(&accel, &gyro, &temp);

  filter0.clear();
  for (int i = 0; i < MOVING_AVERAGE_SIZE; i++) {
    float data = gyro.gyro.z * 100;
    filter0.add(data);
    delayMicroseconds(TAVG_IMU);
  }

  return filter0.get();
}
