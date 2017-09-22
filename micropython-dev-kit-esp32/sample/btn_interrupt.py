from machine import Pin
from time import sleep

def interrupt_func(e):
    print('Value: ', e.value())

button = Pin(12, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_func)


