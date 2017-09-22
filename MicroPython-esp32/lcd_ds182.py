from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd
import onewire, ds18x20

ow = onewire.OneWire(Pin(5))
ds = ds18x20.DS18X20(ow)
i2c = I2C(scl=Pin(2), sda=Pin(0), freq=100000)
roms = ds.scan()

lcd = I2cLcd(i2c, 0x27, 2, 16)
lcd.clear()
lcd.putstr("ESP32\nMicroPython")
time.sleep(5)
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Temperature: ") 
while True:
    ds.convert_temp()
    lcd.move_to(0, 1)
    lcd.putstr('    {0:.2f}'.format(ds.read_temp(roms[0])))
    time.sleep(5)
    
