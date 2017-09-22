from umqtt import MQTTClient 
import machine, ubinascii
import time
import network

wlan  = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('HUAWEI', '0000000000') 

while not wlan.isconnected():
    print('Wait connection')
    time.sleep(1)

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(CLIENT_ID, '103.13.228.61', port=1883)
client.connect()

while True:
    client.publish('micro/python/test', 'Hello World')
    time.sleep(5)

