from machine import Pin
from neopixel import NeoPixel
from time import sleep, ticks_ms 

PIXEL_PIN = Pin(5, Pin.OUT)
PIXEL_COUNT = 8
PERIOD_MS = 500

colors = [(0,0,255),(16,0,128),(32,0,64),(64,0,32),(128,0,16),(255,0,0)]

colors.extend(list(reversed(colors))[1:-1])

def solid():
    elapsed = ticks_ms() // PERIOD_MS
    current = elapsed % len(colors)
    np.fill(colors[current])
    np.write()

def chase():
    elapsed = ticks_ms() // PERIOD_MS
    for i in range(PIXEL_COUNT):
        current = (elapsed+1) % len(colors)
        np[i] = colors[current]
    np.write()

np = NeoPixel(PIXEL_PIN, PIXEL_COUNT)
np.fill((0,0,0))
np.write()

while True:
    chase()
    sleep(0.01)


