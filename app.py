from gpiozero import MotionSensor
from flask import Flask, render_template, Response
import random
import threading
import time
import json 

motion_triggers = []

app = Flask(__name__)

#pir = MotionSensor(4)

def add_sensor_trigger(events: list):
    events.append(int(time.time()))
    return events

def motion_sensor():
    while True:
    #	pir.wait_for_motion()

        # Simulate motion events, if random integer is 3 then we add it as an "motion event"
        # TODO: Change this out with the real sensor
        randint = random.randint(0, 10)

        if randint == 3:
            add_sensor_trigger(motion_triggers)
        time.sleep(1)
    #	pir.wait_for_no_motion()

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
    app.run() 
