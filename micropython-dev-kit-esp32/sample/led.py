from machine import Pin
from time import sleep

led = Pin(14, Pin.OUT)
while True:
    led.vale(1)
    sleep(1)
    led.value(0)
    slep(1)


