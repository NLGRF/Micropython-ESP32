from machine import UART, Pin, I2C
import time, gc, json
from ssd1306 import SSD1306_I2C
import _thread as th

uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
scl = Pin(22)
sda = Pin(21)
i2c = I2C(scl=scl, sda=sda, freq=100000)
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text('ESP32', 45, 5)
oled.text('MicroPython', 20, 20)
oled.show()
def run(e):
    while True:
        try:
            s = uart.read()
            if s :
                o = json.loads(s.decode("utf-8"))
                oled.fill(0)
                oled.text('ESP32', 45, 5)
                oled.text('Voltage: {0:.2f}V'.format(o['v']), 1, 20) 
                oled.text('Current: {0:.2f}A'.format(o['i']), 1, 30)
                oled.text('Power:   {0:.2f}W'.format(o['p']), 1, 40)
                oled.text('Energy:  {0:.2f}Wh'.format(o['e']), 1, 50)
                oled.show()
                print(o)
                gc.collect()
        except OSError as e:
            print('Error: ', e)
        time.sleep(e)
run(1)

th.start_new_thread(run, (1,))
