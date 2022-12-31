import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Vector3
import time

def main():
    # define internal variables
    speed = 100

    # ROS stuff
    motor_pub = rospy.Publisher('motors', Vector3, queue_size=10)
    waving_pub = rospy.Publisher('driver_waving', Bool, queue_size=10)
    rospy.init_node('keyboard_control', anonymous=True)
    
    # creating a running loop
    while not rospy.is_shutdown():
        motor_pub.publish(Vector3(255, -255, 0))
        waving_pub.publish(True)
        time.sleep(5)
        motor_pub.publish(Vector3(0, 0, 0))
        waving_pub.publish(False)
        time.sleep(5)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print("ROS error.")