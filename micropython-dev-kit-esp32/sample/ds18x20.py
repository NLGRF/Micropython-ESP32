from machine import I2C, Pin, Timer
import onewire, ds18x20

ow = onewire.OneWire(Pin(5))
ds = ds18x20.DS18X20(ow) 
roms = ds.scan()

tim0 = Timer(0)

def callback():
    ds.convert_temp()
    print( ds.read_temp(roms[0]) ) 
if len(roms) > 0:
    tim0.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:callback())
else:
    print('Sensor not found')

    

