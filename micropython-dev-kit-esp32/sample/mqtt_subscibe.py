from umqtt import MQTTClient
import machine, ubinascii
import time
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('HUAWEI', '0000000000')
while not wlan.isconnected():
    print('Wait connection')
    time.sleep(1)

def on_message(topic, msg):
    print(topic, msg)

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(CLIENT_ID, 'iot.eclipse.org', port=1883)
client.set_callback(on_message)
client.connect()
client.subscribe('micro/python/test')

while True:
    client.wait_msg()