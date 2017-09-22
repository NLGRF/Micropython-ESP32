import onewire
import time, ds18x20, ssd1306 
from machine import I2C, Pin
import machine, gc
oled = None
ds = None
roms = None
machine.freq(160000000)
gc.collect()
def setup(): 
    global oled
    global ds
    global roms 
    i2c = I2C(scl=Pin(2), sda=Pin(0), freq=100000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    ow = onewire.OneWire(Pin(5))
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
def get_temperature():
    global ds
    global roms
    ds.convert_temp()
    return ds.read_temp(roms[0])
def run():  
    global oled 
    setup()
    if len(roms) != 0:    
        while True: 
            oled.fill(0)
            oled.text('ESP8266', 35, 5)
            oled.text('MicroPython', 15, 20)
            oled.text('TEMP: {0:.2f}'.format(get_temperature()), 2, 35)
            oled.text('HEAP: {0}'.format(gc.mem_free()), 2, 50)
            oled.show()
            gc.collect()
            print("HEAP: ", gc.mem_free())
            time.sleep(5)
run()
