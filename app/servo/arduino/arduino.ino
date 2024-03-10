#include <Servo.h>
#define CONTROL_PIN 5

int default_state = 65;

int wait_time = 500;

Servo my_servo;

void deploy() {
    my_servo.write(180);
    delay(150);
    my_servo.write(default_state);
}

void setup() {
    Serial.begin(9600);
    my_servo.attach(CONTROL_PIN);
    my_servo.write(default_state);
}

void loop() {
    int result = Serial.read();
    if (result == '1') {
        deploy();
    }
}
