#!/usr/bin/env python
from flask import Flask, render_template, Response
#import picamera
import cv2
import socket
import io

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Vector3

ROBOT_LINEAR_SPEED = 111
ROBOT_ANGULAR_SPEED = 111

app = Flask(__name__)
vc = cv2.VideoCapture(-1)
rospy.init_node("WebServer",anonymous=True)
motor_pub = rospy.Publisher('motors', Vector3, queue_size=10)

# set dimensions
#vc.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
#vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

def robot_stop():
	rospy.loginfo("Webserver stop pressed")
	motor_pub.publish(Vector3(0, 0, 0))

def robot_travel(forward):
	if forward:
		rospy.loginfo("Webserver fwd pressed")
		motor_pub.publish(Vector3(ROBOT_LINEAR_SPEED, ROBOT_LINEAR_SPEED, 0))
	else:
		rospy.loginfo("Webserver back pressed")
		motor_pub.publish(Vector3(-ROBOT_LINEAR_SPEED, -ROBOT_LINEAR_SPEED, 0))

def robot_turn(clockwise):
	if clockwise:
		rospy.loginfo("Webserver right pressed")
		motor_pub.publish(Vector3(-ROBOT_ANGULAR_SPEED, ROBOT_ANGULAR_SPEED, 0))
	else:
		rospy.loginfo("Webserver left pressed")
		motor_pub.publish(Vector3(ROBOT_ANGULAR_SPEED, -ROBOT_ANGULAR_SPEED, 0))

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


if __name__ == '__main__':
		robot_stop()
		app.run(host='0.0.0.0', debug=False, threaded=True)
			   