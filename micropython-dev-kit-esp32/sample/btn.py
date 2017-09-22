from machine import Pin
from time import sleep

button = Pin(12, Pin.IN, Pin.PULL_UP)

button.value()

    