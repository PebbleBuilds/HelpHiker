import pygame
import sys
import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Vector3

def main():
    # define internal variables
    lin_speed = 100
    ang_speed = 100

    # initialising pygame
    pygame.init()

    # ROS stuff
    motor_pub = rospy.Publisher('motors', Vector3, queue_size=10)
    waving_pub = rospy.Publisher('driver_waving', bool, queue_size=10)
    rospy.init_node('keyboard_control', anonymous=True)
    rate = rospy.Rate(50) # 50hz
    
    # creating a running loop
    while not rospy.is_shutdown():

        # if no keys down, send x = 0, y = 0
        left_motor = 0
        right_motor = 0
        key_is_down = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            left_motor -= speed
            right_motor += speed
            key_is_down = True
        if keys[pygame.K_RIGHT]:
            left_motor += speed
            right_motor -= speed
            key_is_down = True
        if keys[pygame.K_UP]:
            left_motor += speed
            right_motor += speed
            key_is_down = True
        if keys[pygame.K_DOWN]:
            left_motor -= speed
            right_motor -= speed
            key_is_down = True
        if keys[pygame.K_z]:
            waving_pub.publish(True)
        if keys[pygame.K_x]:
            waving_pub.publish(False)

        
        if(key_is_down):
            print("A key has been pressed")

        # creating a loop to check events that
        # are occurring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        motor_pub.publish(Vector3(left_motor, right_motor, 0))
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print("ROS error.")