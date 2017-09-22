import time
from dht import DHT22
from machine import Pin, Timer

dhtPn = Pin(17)
d = DHT22(dhtPn)

tim0 = Timer(0)

def callback():
    try:
        d.measure()
        print(d.temperature(), d.humidity()) 
        
    except OSError as e:
        print('sensor read error')
    time.sleep(2)


tim0.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:callback())

    

