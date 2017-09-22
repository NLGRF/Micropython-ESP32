from usched import Sched
from machine import Pin

led1 = Pin(4, Pin.OUT)
led2 = Pin(13, Pin.OUT)

def toggle1(objLED, period):
    while True:
        yield period
        objLED.value(not objLED.value())

def toggle2(objLED, period):
    while True:
        yield period
        objLED.value(not objLED.value())

objSched = Sched()
objSched.add_thread(toggle1(led1, .2))
objSched.add_thread(toggle1(led2, 1))
objSched.run()
