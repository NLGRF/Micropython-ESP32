# -*- coding: utf-8 -*-
import time
from umqtt import MQTTClient
import machine, ubinascii, gc, json
from ssd1306 import SSD1306_I2C
from machine import I2C
from machine import Pin
import dht
from machine import Timer

machine.freq(160000000)
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
gc.collect()
scl = Pin(2)
sda = Pin(0)
gpio4 = Pin(4, Pin.OUT)
gpio13 = Pin(13, Pin.OUT)
i2c = I2C(scl=scl, sda=sda, freq=100000)
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text('ESP8266', 35, 5)
oled.text('MicroPython', 20, 20)
oled.show()

d = dht.DHT22(Pin(5))
client = MQTTClient(CLIENT_ID, 'q.emqtt.com', port=1883, keepalive=20)
will_msg = {'id': CLIENT_ID, 'status': False, 'msg': 'The connection from this device is lost:('}
client.set_last_will('/device/will/status', json.dumps(will_msg))
client.connect()
tim0 = Timer(0)

def display():
    d.measure()
    oled.fill(0)
    oled.text('ESP8266', 35, 5)
    oled.text('MicroPython', 20, 20)
    oled.text('T:{0:.2f} C'.format(d.temperature()), 3, 35) 
    oled.text('H:{0:.2f} %'.format(d.humidity()), 3, 50)
    oled.show()
    msg =  json.dumps({
        'heap': gc.mem_free(),
        'Type':7,
        'Id': CLIENT_ID,
        'temperature': '{0:.2f}'.format(d.temperature()),
        'humidity': '{0:.2f}'.format(d.humidity())
        })
    print(msg) 
    client.publish('micro/python/temperature', msg)    

tim0.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:display())
display()
def on_message(topic, msg):
    print(topic, msg)
    if topic == b'/device/12345/switch':
        obj = json.loads(msg)
        if obj['gpio'] == 4:
            if obj['value'] == True:
                gpio4.value(1)
            else:
                gpio4.value(0)
        if obj['gpio'] == 13:
            if obj['value'] == True:
                gpio13.value(1)
            else:
                gpio13.value(0)

client.set_callback(on_message)
client.subscribe('/device/12345/switch', 0)
client.subscribe('/device/4567/switch', 0)
while True:
    client.wait_msg()
