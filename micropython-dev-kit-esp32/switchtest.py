from usched import Sched, wait
from switch import Switch
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

s1 = Switch(objSched, p1, close_func = p1Pressed, open_func = p1Released)
s2 = Switch(objSched, p2, close_func = p2Pressed, open_func = p2Released)
objSched.run()
