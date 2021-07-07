#Libraries
import RPi.GPIO as GPIO
import time
from web_app import db
from database.models import ExperimentData

#Setam modul Pin-urilor
GPIO.setmode(GPIO.BCM)
 
#setarea pin-urilor
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#setarea directiei de transmitere a datelor
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # transmitem semnal ultrasonic
    GPIO.output(GPIO_TRIGGER, True)
 
    # dupa 0.01ms oprim semnalul
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartTime = time.time()
    StopTime = time.time()
 
    # salvam timpul de pornire StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # salvam timpul cand ajunge semnalul
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # realizam diferenta intre timpuri
    TimeElapsed = StopTime - StartTime
    #inmultim cu 34300 cm/s (viteza sunetului)
    # impartim la 2 deoarece semnalul se duce si se intoarce
    distance = (TimeElapsed * 34300) / 2
    
    ex = ExperimentData(data_colected=distance, experiment_id_relation=1)
    time.sleep(2)
    db.session.add(ex)
    db.session.commit()
    
    return distance
 
def run():
    try:
        while True:
            dist = distance()
            return dist
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()