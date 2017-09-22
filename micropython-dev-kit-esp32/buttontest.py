from usched import Sched, wait
from button import Button
from machine import Pin

p1 = Pin(14, Pin.IN, Pin.PULL_UP)
p2 = Pin(12, Pin.IN, Pin.PULL_UP)
objSched = Sched()

def p1Pressed(*args):
    print("p1 pressed ")
def p1Released(*args):
    print("p1 released ")
def p2Pressed(*args):
    print("p2 pressed ")
def p2Released(*args):
    print("p2 released ")

s1 = Button(objSched, p1)
s1.on_pressed(p1Pressed)
s1.on_released(p1Released)

s2 = Button(objSched, p2)
s2.on_pressed(p2Pressed)
s2.on_released(p2Released)

objSched.run()
