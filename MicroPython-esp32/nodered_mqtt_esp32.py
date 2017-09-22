import time
from umqtt import MQTTClient
import machine, ubinascii, gc, json
from ssd1306 import SSD1306_I2C
from machine import I2C, Pin 
import dht
from usched import Sched, Timeout
import network

wlan = None
client = None
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
gpio4 = Pin(4, Pin.OUT)
gpio13 = Pin(5, Pin.OUT)
gpio23 = Pin(23, Pin.OUT)
gpios = [None, gpio4, gpio13]
gpio23.value(1)
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text('ESP32', 45, 5)
oled.text('MicroPython', 20, 20)
oled.show()
d = dht.DHT22(Pin(17))

def on_message(topic, msg):
    print(topic, msg)
    if topic == b'/device/12345/switch':
        obj = json.loads(msg)
        gpio = gpios[obj['gpio'] ]
        if not gpio is None:
            if obj['value'] == True:
                gpio.value(1)
            else:
                gpio.value(0)

def mqtt_loop():
    global client 
    while True:
        client.wait_msg()
        yield 0.1

def display():
    global client
    global oled 
    while True:
        try:
            d.measure()
            oled.fill(0)
            oled.text('ESP32', 45, 5)
            oled.text('MicroPython', 20, 20)
            oled.text('T:{0:.2f} C'.format(d.temperature()), 3, 35) 
            oled.text('H:{0:.2f} %'.format(d.humidity()), 3, 50)
            oled.show()
            msg =  json.dumps({
                'heap': gc.mem_free(), 'Type':7,
                'Id': CLIENT_ID, 'temperature': '{0:.2f}'.format(d.temperature()), 'humidity': '{0:.2f}'.format(d.humidity())
            })
            print(msg) 
            client.publish('micro/python/temperature', msg)
            yield 5
        except OSError as identifier:
            yield .5
def blink():
    while True:
        gpio23.value(not gpio23.value())
        yield 1

def connected():
    global client
    client = MQTTClient(CLIENT_ID, 'q.emqtt.com', port=1883, keepalive=20)
    will_msg = {'id': CLIENT_ID, 'status': False, 'msg': 'The connection from this device is lost:('}
    client.set_last_will('/device/will/status', json.dumps(will_msg))
    client.set_callback(on_message)
    client.connect()
    client.subscribe('/device/12345/switch', 0)
    client.subscribe('/device/4567/switch', 0)     

def run():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('HUAWEI', '0000000000')
    while not wlan.isconnected():
        print('.')
        time.sleep(.5)
    print(wlan.ifconfig())
    connected()
   
print('WIFI config...')
run()
objSched = Sched()
objSched.add_thread(mqtt_loop())
objSched.add_thread(display())
objSched.add_thread(blink())
objSched.run()
