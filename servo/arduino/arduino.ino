#include <Servo.h>
#include <SoftPWM.h>
#define CONTROL_PIN 5

int target = 0;
Servo myservo;

void setup()
{
    Serial.begin(9600);
    myservo.attach(CONTROL_PIN);
}

void loop()
{
    int result = Serial.read();
    if (result == '1')
    {
        myservo.write(45);
    }
    else if (result == '2')
    {
        myservo.write(90);
    }
}
