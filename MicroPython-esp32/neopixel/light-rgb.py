from machine import Pin
from neopixel import NeoPixel
from time import sleep

PIXEL_PIN = Pin(5, Pin.OUT)
PIXEL_COUNT = 8

np = NeoPixel(PIXEL_PIN, PIXEL_COUNT)
np.fill((0,0,0))
np.write()

np.fill((255,0,0))
np.write()
sleep(2)

np.fill((0,255,0))
np.write()
sleep(2)

np.fill((0,0,255))
np.write()
sleep(2)

np.fill((0,0,0))
np.write()
