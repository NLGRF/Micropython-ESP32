from time import sleep, sleep_ms, ticks_ms
from machine import I2C, Pin
import ssd1306, time

i2c = None
oled = None

def setup():
    global i2c
    global oled
    i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c,  addr=0x3c, external_vcc=False)

def run():
    global oled
    cnt = 1
    setup()
    while True:
        oled.fill(0)
        oled.text('Count', 15, 10)
        oled.text('{0} xxxxx {1}'.format(cnt, 2), 25, 20)
        oled.show()
        cnt = cnt + 1
        time.sleep(.5)

run()