from machine import Pin
import time
led = Pin(23, Pin.OUT)

def run():
    while True:
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)
run()


