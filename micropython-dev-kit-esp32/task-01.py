from usched import Sched
from machine import Pin
from time import sleep

led1 = Pin(4, Pin.OUT)
led2 = Pin(13, Pin.OUT)

def toggle1(objLED):
    while True: 
        sleep(1)
        yield
        objLED.value(not objLED.value()) 

def toggle2(objLED):
    while True: 
        sleep(.1)
        yield
        objLED.value(not objLED.value()) 

objSched = Sched()
objSched.add_thread(toggle1(led1))
objSched.add_thread(toggle2(led2))
objSched.run()



