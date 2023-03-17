#!/usr/bin/env python
from flask import Flask, render_template, Response
#import picamera
import cv2
import socket
import io

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Vector3

SPEED_1 = 50
SPEED_2 = 50
waving = False

app = Flask(__name__)
vc = cv2.VideoCapture(-1)
motor_pub = rospy.Publisher('motors', Vector3, queue_size=10)
waving_pub = rospy.Publisher('driver_waving', Bool, queue_size=10)
rospy.init_node("WebServer",anonymous=True)

# set dimensions
#vc.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
#vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

def robot_stop():
	rospy.loginfo("Webserver stop pressed")
	motor_pub.publish(Vector3(0, 0, 0))
	waving_pub.publish(Bool(False))

def robot_travel(forward):
	if forward:
		rospy.loginfo("Webserver fwd pressed")
		motor_pub.publish(Vector3(SPEED_1, SPEED_2, 0))
	else:
		rospy.loginfo("Webserver back pressed")
		motor_pub.publish(Vector3(-SPEED_1, -SPEED_2, 0))

def robot_turn(clockwise):
	if clockwise:
		rospy.loginfo("Webserver right pressed")
		motor_pub.publish(Vector3(SPEED_1, -SPEED_2, 0))
	else:
		rospy.loginfo("Webserver left pressed")
		motor_pub.publish(Vector3(-SPEED_1, SPEED_2, 0))

def robot_wave():
	rospy.loginfo("Webserver wave pressed")
	waving_pub.publish(Bool(True))
	rospy.loginfo("I finished")

@app.route('/')
def index():
	"""Video streaming"""
	return render_template('index.html')

def gen():
	"""Video streaming generator function."""
	while True:
		if not vc.isOpened():
			print("vc not open")
		rval, frame = vc.read()
		frame = cv2.flip(frame,-1)
		if not rval:
			print("read failed")
		cv2.imwrite('t.jpg', frame)
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
	"""Video streaming route. Put this in the src attribute of an img tag."""
	return Response(gen(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/forward", methods=['GET', 'POST'])
def forward():
	robot_travel(True)
	return ('', 204)

@app.route("/backward", methods=['GET', 'POST'])
def backward():
	robot_travel(False)
	return ('', 204)

@app.route("/turnRight", methods=['GET', 'POST'])
def turn_right():
	robot_turn(True)
	return ('', 204)

@app.route("/turnLeft", methods=['GET', 'POST'])
def turn_left():
	robot_turn(False)
	return ('', 204)

@app.route("/stop", methods=['GET', 'POST'])
def stop():
	robot_stop()
	return ('', 204)

@app.route("/wave", methods=['GET', 'POST'])
def wave():
	robot_wave()
	return ('', 204)


if __name__ == '__main__':
		robot_stop()
		app.run(host='0.0.0.0', debug=False, threaded=True)
			   