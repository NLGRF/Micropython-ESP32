from umqtt import MQTTClient
import machine, ubinascii
import time
import network
import json
from dht import DHT22
from machine import Pin, Timer

led = Pin(23, Pin.OUT)
dhtPn = Pin(17)
d = DHT22(dhtPn)

tim0 = Timer(0)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('HUAWEI', '0000000000')
while not wlan.isconnected():
    print('Wait connection')
    time.sleep(1)

def on_message(topic, msg):
    print(topic, msg)
    if topic == b'micro/python/switch':
        obj = json.loads(msg)
        gpio = obj['gpio']
        if gpio == 23:
            state = obj['state']
            led.value(state)

def tim_callback():
    d.measure()
    msg =  json.dumps({
        'Id': CLIENT_ID, 
        'temperature': float('{0:.2f}'.format(d.temperature())), 
        'humidity': float('{0:.2f}'.format(d.humidity()))
    })
    print(msg) 
    client.publish('micro/python/temperature', msg)


CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(CLIENT_ID, 'iot.eclipse.org', port=1883)
client.set_callback(on_message)
client.connect()
client.subscribe('micro/python/switch')

tim0.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:tim_callback())

while True:
    try:
        client.wait_msg()
    except OSError as e:
        print('wait_msg: ', e)
    

