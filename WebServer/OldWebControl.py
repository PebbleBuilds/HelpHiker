from flask import Flask, render_template, request, redirect, url_for, make_response
import time
import RPi.GPIO as GPIO

app = Flask(__name__) #set up flask server
#when the root IP is selected, return index.html page
@app.route('/')
def index():
    return render_template('index.html')
#recieve which pin to change from the button press on index.html
#each button returns a number that triggers a command in this function
#
#Uses methods from motors.py to send commands to the GPIO to operate the motors
@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):
    changePin = int(changepin) #cast changepin to an int
    if changePin == 1:
        print("Left")
    elif changePin == 2:
        print("Forward")
    elif changePin == 3:
        print("Right")
    elif changePin == 4:
        print("Reverse")
    else:
        print("Nothing")
    response = make_response(redirect(url_for('index')))
    return(response)
app.run(debug=True, host='0.0.0.0', port=8000) #set up the server in debug mode to the port 8000


