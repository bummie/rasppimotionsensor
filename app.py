from gpiozero import MotionSensor
from flask import Flask, render_template, Response
import random
import threading
import time
import json 

motion_triggers = []

app = Flask(__name__)

pir = MotionSensor(4)

def add_sensor_trigger(events: list):
    events.append(int(time.time()))
    return events

def motion_sensor():
    while True:
        pir.wait_for_motion()
        add_sensor_trigger(motion_triggers)
        pir.wait_for_no_motion()

@app.route('/events')
def events():
    return Response(json.dumps(motion_triggers[-50:]),  mimetype='application/json')

@app.route('/')
def hello(): 
    return render_template('index.html')
  
if __name__=='__main__': 

    # Start thread looking for motion sensor triggering
    threading.Thread(target=motion_sensor).start()
    
    # Start flask webserver
    app.run(host="0.0.0.0")