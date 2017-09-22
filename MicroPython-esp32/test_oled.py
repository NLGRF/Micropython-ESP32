import onewire
import time, ds18x20, ssd1306 
from machine import I2C, Pin 
i2c = I2C(scl=Pin(2), sda=Pin(0), freq=100000)

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text('Temp', 18, 10) 
oled.text('{0:.2f}'.format(30.34), 12, 20)
oled.show()
