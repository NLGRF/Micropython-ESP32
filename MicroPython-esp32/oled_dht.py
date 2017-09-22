from machine import I2C
from machine import Pin
from dht import DHT22
from ssd1306 impor SSD1306_I2C
import time 

scl = Pin(2)
sda = Pin(0)
i2c = I2C(scl=scl, sda=sda, freq=100000)
oled = ssd1306.SSD1306_I2C(64, 32, i2c)
d = DHT22(Pin(2))
while True:
    d.measure()
    oled.fill(0)
    oled.text('ESP8266', 35, 5)
    oled.text('MicroPython', 20, 20)
    oled.text('T:{0:.2f}'.format(d.temperature()), 3, 35) 
    oled.text('H:{0:.2f}'.format(d.humidity()), 3, 50)
    oled.show()
    time.sleep(5)
