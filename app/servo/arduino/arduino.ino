#include <Servo.h>
#include <SoftPWM.h>
#define CONTROL_PIN 5

int deploy_state = 90;
int default_state = 0;

int wait_time = 500;

Servo myservo;

void deploy()
{
    myservo.write(deploy_state);
    delay(wait_time);
    myservo.write(default_state);
}

void setup()
{
    Serial.begin(9600);
    myservo.attach(CONTROL_PIN);
    myservo.write(default_state);
}

void loop()
{
    int result = Serial.read();
    if (result == '1')
    {
        deploy();
    }
}
