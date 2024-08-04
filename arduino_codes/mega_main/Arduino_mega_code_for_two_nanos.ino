#include <HardwareSerial.h>
#include <DHT.h>
#include <MovingAverageFloat.h>
#include <ODriveArduino.h>

// Constants and Variables
const float p0_max = 5.0, p0_min = -0.5;
const float p1_max = 7.4, p1_min = 1.1;
const int tavg = 10;
const int relay = 11;
const int a_max = 120, a_min = 0;

MovingAverageFloat<16> filter0, filter1;
HardwareSerial& odrive_serial = Serial1;
ODriveArduino odrive(odrive_serial);

#define joyX A7
#define joyY A7

char received_data[100], received_data2[100];
int angle_value, imu1_value, angle_value2, imu1_value2;
float m, k;

template<class T>
inline Print& operator <<(Print &obj, T arg) {
    obj.print(arg);
    return obj;
}

template<>
inline Print& operator <<(Print &obj, float arg) {
    obj.print(arg, 4);
    return obj;
}

void setup() {
    odrive_serial.begin(115200);
    Serial.begin(9600);
    Serial2.begin(9600);
    Serial3.begin(9600);

    while (!Serial2 || !Serial3);

    int requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL;
    Serial << "Axis0: Requesting state " << requested_state << '\n';
    if (!odrive.run_state(0, requested_state, false)) return;

    odrive_serial << "w axis0.controller.config.input_filter_bandwidth 5.0\n";
    odrive_serial << "w axis0.controller.config.input_mode 3\n";
}

void loop() {
    for (int i = 0; i < 10; i++) {
        int data0 = analogRead(A0);
        filter0.add(data0);
        delayMicroseconds(tavg);
    }

    float data0 = filter0.get();
    Serial.print(data0); Serial.print("\t");

    sensor_data2();

    int xValue = analogRead(joyX);
    float p = ((p0_max - p0_min) / 1023) * xValue + p0_min;
    odrive.SetPosition(0, p);
    delay(5);
}

float encoder() {
    odrive_serial << "r axis1.encoder.pos_estimate\n";
    String enc = odrive_serial.readStringUntil('\r');
    return enc.substring(0, 6).toFloat();
}

void sensor_data() {
    if (Serial3.available()) {
        int len = Serial3.readBytesUntil('\n', received_data, sizeof(received_data));
        received_data[len] = '\0';

        char* temPtr;
        unsigned int temp_value = strtoul(received_data, &temPtr, 10);
        angle_value = strtoul(temPtr + 1, &temPtr, 10);
        imu1_value = strtoul(temPtr + 1, &temPtr, 10);

        int mapped_angle = map(angle_value, 4189, 7800, 80, 0);

        if (temp_value != 0) {
            // Additional sensor handling can be added here
        }
    }
}

void sensor_data2() {
    if (Serial2.available()) {
        int len = Serial2.readBytesUntil('\n', received_data2, sizeof(received_data2));
        received_data2[len] = '\0';

        char* temPtr2;
        unsigned int temp_value2 = strtoul(received_data2, &temPtr2, 10);
        angle_value2 = strtoul(temPtr2 + 1, &temPtr2, 10);
        imu1_value2 = strtoul(temPtr2 + 1, &temPtr2, 10);
        int gz_value = strtoul(temPtr2 + 1, &temPtr2, 10);

        int mapped_angle2 = map(angle_value2, 4490, 7741, 0, 80);

        if (temp_value2 != 0) {
            Serial.print(angle_value2); Serial.print("\t");
            Serial.print(imu1_value2); Serial.print("\t");
            Serial.println(gz_value);
        }
    }
}
