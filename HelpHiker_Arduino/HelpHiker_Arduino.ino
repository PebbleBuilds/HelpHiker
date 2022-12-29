#include <ros.h>
#include <std_msgs/Empty.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <geometry_msgs/Vector2.h>
#include <math.h>

#include "Sweeper.h"
#include "Motor.h"

// Pinouts
// Servo 1: D5
// Servo 2: D6 
// Motor 1: D11 and D10
// Motor 2: D9 and D3

/////////////////////////////
// Define internal variables
/////////////////////////////

// Servo arms
bool bWavingArms = false;
int iServo1Angle = 0;
int c_iServoUpdateInterval = 50; // in ms
int c_iServo1Pin = 5;
int c_iServo2Pin = 6;
Sweeper servo1(c_iServoUpdateInterval, 1, 0);
Sweeper servo2(c_iServoUpdateInterval, -1, 180);

// Drive motors
int c_iMotor1Pin1 = 11;
int c_iMotor1Pin2 = 10;
int c_iMotor2Pin1 = 9;
int c_iMotor2Pin2 = 3;

Motor motor1(c_iMotor1Pin1, c_iMotor1Pin2);
Motor motor2(c_iMotor2Pin1, c_iMotor2Pin2);


/////////////////////////////
// ROS stuff
/////////////////////////////

// Define ros node
ros::NodeHandle nh;

// ros subscriber callbacks and initializations
void toggle_led_cb( const std_msgs::Empty& toggle_led_msg){
    digitalWrite(LED_BUILTIN, HIGH-digitalRead(13));   // blink the led
}
ros::Subscriber<std_msgs::Empty> sub_toggle_led("toggle_led", &toggle_led_cb);

void driver_waving_cb( const std_msgs::Bool& driver_waving_msg){
    bWavingArms = driver_waving_msg.data;
}
ros::Subscriber<std_msgs::Bool> sub_driver_waving("driver_waving", &driver_waving_cb);

void motors_cb( const geometry_msgs::Vector2& motor_msg){
    motor1.Write(motor_msg.data.x);
    motor2.Write(motor_msg.data.y);
}
ros::Subscriber<geometry_msgs::Vector2> sub_motor_values("motors", &motors_cb)

// Initialize publishers
std_msgs::String chatter_msg;
ros::Publisher chatter("chatter", &chatter_msg);
char hello[13] = "hello world!";

/////////////////////////////
// Setup!
/////////////////////////////
void setup()
{
    // ROS stuff
    nh.initNode();
    nh.advertise(chatter);

    // Toggle LED
    pinMode(LED_BUILTIN, OUTPUT);
    nh.subscribe(sub_toggle_led);

    // Servos
    servo1.Attach(c_iServo1Pin);
    servo2.Attach(c_iServo2Pin);
    nh.subscribe(sub_driver_waving);

    // Motors
    motor1.Setup();
    motor2.Setup();
}

/////////////////////////////
// Loop!
/////////////////////////////
void loop()
{
    chatter_msg.data = hello;
    chatter.publish( &chatter_msg );
    nh.spinOnce();
    delay(1);

    if(bWavingArms)
    {
        servo1.Update();
        servo2.Update();
    }
}
