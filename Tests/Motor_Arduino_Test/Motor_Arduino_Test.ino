//#include "Motor.h"

// Pinouts
// Servo 1: D5 (PWM)
// Servo 2: D6 (PWM)
// Motor 1: D3 (PWM enable) and D2 + D4 (dir)
// Motor 2: D9 (PWM enable) and D8 + D7 (dir)

/////////////////////////////
// Define internal variables
/////////////////////////////

// Drive motors
int c_iMotor1Pin1 = 2;
int c_iMotor1Pin2 = 4;
int c_iMotor1PinEnable = 3;

int c_iMotor2Pin1 = 8;
int c_iMotor2Pin2 = 7;
int c_iMotor2PinEnable = 9;

//Motor motor1(c_iMotor1Pin1, c_iMotor1Pin2, c_iMotor1PinEnable);
//Motor motor2(c_iMotor2Pin1, c_iMotor2Pin2, c_iMotor2PinEnable);
int iMotor1Speed = 128;
int iMotor2Speed = 128;

/////////////////////////////
// Setup!
/////////////////////////////
void setup()
{
    pinMode(c_iMotor1Pin1, OUTPUT);
    pinMode(c_iMotor1Pin2, OUTPUT);
    pinMode(c_iMotor1PinEnable, OUTPUT);

    digitalWrite(c_iMotor1Pin1, 0);
    digitalWrite(c_iMotor1Pin2, 0);
    analogWrite(c_iMotor1PinEnable, 0);
}

/////////////////////////////
// Loop!
/////////////////////////////
void loop()
{
    digitalWrite(c_iMotor1Pin1, 0);
    digitalWrite(c_iMotor1Pin2, 1);
    analogWrite(c_iMotor1PinEnable, 128);
}
