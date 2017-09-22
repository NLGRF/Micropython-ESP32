import esp
import time
from umqtt import MQTTClient
import machine, ubinascii, gc, json
from ssd1306 import SSD1306_I2C
from machine import I2C
from machine import Pin
import dht

machine.freq(160000000)
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
gc.collect()
scl = Pin(22)
sda = Pin(21)
i2c = I2C(scl=scl, sda=sda, freq=100000)
oled = SSD1306_I2C(128, 64, i2c)
d = dht.DHT22(Pin(17))
client = MQTTClient(CLIENT_ID, 'q.emqtt.com')
client.connect() 

while True:
    d.measure()
    oled.fill(0)
    oled.text('ESP8266', 35, 5)
    oled.text('MicroPython', 20, 20)
    oled.text('T:{0:.2f}'.format(d.temperature()), 3, 35) 
    oled.text('H:{0:.2f}'.format(d.humidity()), 3, 50)
    oled.show()
    msg =  json.dumps({ 'heap': gc.mem_free(),  'Type':7, 'Id': CLIENT_ID, 'temperature': '{0:.2f}'.format(d.temperature()), 'humidity': '{0:.2f}'.format(d.humidity())})
    print(msg) 
    client.publish('micro/python/temperature', msg)
    time.sleep(5)

