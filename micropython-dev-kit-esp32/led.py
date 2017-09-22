from machine import Pin

class Led(object):
    def __init__(self, pinNumber):
        self.pin = Pin(pinNumber, Pin.OUT)
        self.low()
    def low(self):
        self.pin.value(0)
    def high(self):
        self.pin.value(1)
    def toggle(self):
        self.pin.value(not self.pin.value())
