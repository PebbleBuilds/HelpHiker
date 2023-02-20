#include <ros.h>
#include <std_msgs/Empty.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <geometry_msgs/Vector3.h>
#include <math.h>

#include "Sweeper.h"
#include "Motor.h"

// Pinouts
// Servo 1: D5 (PWM)
// Servo 2: D6 (PWM)
// Motor 1: D3 (PWM enable) and D2 + D4 (dir)
// Motor 2: D9 (PWM enable) and D8 + D7 (dir)

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
int c_iMotor1Pin1 = 2;
int c_iMotor1Pin2 = 4;
int c_iMotor1PinEnable = 3;

int c_iMotor2Pin1 = 8;
int c_iMotor2Pin2 = 7;
int c_iMotor2PinEnable = 9;

Motor motor1(c_iMotor1Pin1, c_iMotor1Pin2, c_iMotor1PinEnable);
Motor motor2(c_iMotor2Pin1, c_iMotor2Pin2, c_iMotor2PinEnable);


/////////////////////////////
// ROS stuff
/////////////////////////////

// Define ros node
ros::NodeHandle nh;

// Initialize publishers
std_msgs::String chatter_msg;
ros::Publisher chatter("chatter", &chatter_msg);

// ros subscriber callbacks and initializations
void driver_waving_cb( const std_msgs::Bool& driver_waving_msg){
    bWavingArms = driver_waving_msg.data;
    nh.loginfo("Waving toggled!");
}
ros::Subscriber<std_msgs::Bool> sub_driver_waving("driver_waving", &driver_waving_cb);

void motors_cb( const geometry_msgs::Vector3& motor_msg){
    motor1.Write(int(motor_msg.x));
    motor2.Write(int(motor_msg.y));
    String msg = "Received motor speeds:";
    msg += int(motor_msg.x);
    msg += " ";
    msg += int(motor_msg.y);
    nh.loginfo(msg.c_str());
}
ros::Subscriber<geometry_msgs::Vector3> sub_motors("motors", &motors_cb);

/////////////////////////////
// Setup!
/////////////////////////////
void setup()
{
    // ROS stuff
    nh.initNode();
    nh.advertise(chatter);

    // Servos
    servo1.Attach(c_iServo1Pin);
    servo2.Attach(c_iServo2Pin);
    nh.subscribe(sub_driver_waving);

    // Motors
    motor1.Setup();
    motor2.Setup();
    nh.subscribe(sub_motors);
}

/////////////////////////////
// Loop!
/////////////////////////////
void loop()
{
    nh.spinOnce();
    //delay(1);

    if(bWavingArms)
    {
        servo1.Update();
        servo2.Update();
    }
}
