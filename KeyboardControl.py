import pygame
import sys
import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Vector3

import os

def main():
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

    # define internal variables
    speed = 255

    # initialising pygame
    pygame.init()
    pygame.display.init()
    pygame.event.set_grab(True)
    pygame.key.set_repeat(1)

    # ROS stuff
    motor_pub = rospy.Publisher('motors', Vector3, queue_size=10)
    waving_pub = rospy.Publisher('driver_waving', Bool, queue_size=10)
    rospy.init_node('keyboard_control', anonymous=True)
    rate = rospy.Rate(50) # 50hz
    
    # creating a running loop
    while not rospy.is_shutdown():
        # creating a loop to check events that
        # are occurring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_motor = -speed
                    right_motor = speed
                    print("Left pressed.")
                    motor_pub.publish(Vector3(left_motor, right_motor, 0))
                if event.key == pygame.K_RIGHT:
                    left_motor = speed
                    right_motor = -speed
                    print("Right pressed.")
                    motor_pub.publish(Vector3(left_motor, right_motor, 0))
                if event.key == pygame.K_UP:
                    left_motor = speed
                    right_motor = speed
                    print("Up pressed.")
                    motor_pub.publish(Vector3(left_motor, right_motor, 0))
                if event.key == pygame.K_DOWN:
                    left_motor = -speed
                    right_motor = -speed
                    print("Down pressed.")
                    motor_pub.publish(Vector3(left_motor, right_motor, 0))
                if event.key == pygame.K_SPACE:
                    left_motor = 0
                    right_motor = 0
                    print("Space pressed.")
                    motor_pub.publish(Vector3(left_motor, right_motor, 0))

                if event.key == pygame.K_z:
                    waving_pub.publish(True)
                    print("Start waving!")
                if event.key == pygame.K_x:
                    waving_pub.publish(False)
                    print("Stop waving!")
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print("ROS error.")