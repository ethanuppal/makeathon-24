#include <Servo.h>
#include <SoftPWM.h>
#define CONTROL_PIN 5

int deploy_state = 90;
int default_state = 0;

int wait_time = 500;

Servo my_servo;

void deploy() {
    my_servo.write(deploy_state);
    delay(wait_time);
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
