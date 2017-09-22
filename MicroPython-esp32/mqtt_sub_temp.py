from simple_mqtt import MQTTClient
import onewire
import time,ssd1306
from esp_board import WifiStation
from machine import I2C, Pin
from ssd1306_gfx import *
import machine, ubinascii, gc, json
machine.freq(160000000)
gc.collect()
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
oled = None
client = None
def sub_cb(topic, msg):
    global oled
    print((topic, msg))
    _obj =  json.loads(msg);
    oled.fill(0) 
    oled.text('MicroPython', 20, 5)
    draw_line(oled , 2 , 18, 126, 18)
    oled.text('ID: {0}'.format(_obj['id']), 10, 25) 
    oled.text('Temp: {0}'.format(_obj['temperature']), 10, 40)
    if 'humidity' in _obj:
        oled.text('Humi: {0}'.format(_obj['humidity']), 10, 55)
    oled.show()     
    
def wifi():
    global client
    global CLIENT_ID    
    client = MQTTClient(CLIENT_ID, 'q.emqtt.com')
    client.set_callback(sub_cb)
    client.connect() 
    print("MQTT client id:", CLIENT_ID)
    time.sleep(2)
    run()
def setup(): 
    global oled 
    i2c = I2C(scl=Pin(2), sda=Pin(0), freq=100000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    wlan = WifiStation()
    wlan.connect('see_dum', '0863219053')
    wlan.wait_connection(wifi)     
def run():
    global client
    client.subscribe("micro/python/temperature")
    try:
        while True:
            client.wait_msg()
    finally:
        client.disconnect()
