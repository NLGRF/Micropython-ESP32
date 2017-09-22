from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)

lcd = I2cLcd(i2c, 0x3F, 4, 20)
lcd.clear()
lcd.putstr("       ESP32        ")
lcd.putstr("     MicroPython    ")
