from machine import Pin
from time import sleep

led = Pin(14, Pin.OUT)
button = Pin(12, Pin.IN, Pin.PULL_UP)
while True:
    led.value(not button.value())


    