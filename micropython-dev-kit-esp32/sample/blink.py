from machine import Pin

led = Pin(23, Pin.OUT)
led.value(1)
led.value(0)
from time import sleep
while True:
    led.value(1)
    sleep(1)
    led.value(0)
    sleep(1)



