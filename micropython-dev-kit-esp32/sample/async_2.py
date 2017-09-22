import uasyncio as asyncio
from dht import DHT22
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import network, json
from umqtt import MQTTClient
import machine, ubinascii
client = None
cfg = None
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
ิbtn = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(23, Pin.OUT)
dthPn = Pin(17)
scl = Pin(22)
sda = Pin(21)
i2c = I2C(scl=scl, sda=sda, freq=100000)
oled = SSD1306_I2C(128, 64, i2c,  addr=0x3C)
oled.fill(0)
oled.text('ESP32', 45, 5)
oled.text('MicroPython', 20, 20)
oled.show()
loop = asyncio.get_event_loop()
d = DHT22(dthPn)

def on_message(topic, msg):
    print(topic, msg)
    
async def wifi_config():
    global cfg
    global client
    global CLIENT_ID
    print('load configuration')
    f = open('config.json')
    cfg = json.loads(f.read())
    f.close()
    print(cfg)
    print('starting wifi connection')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(cfg['ap']['ssid'], cfg['ap']['pwd'])
    while not wlan.isconnected():
        print('wait connection...')
        await asyncio.sleep(1)
    wlan.ifconfig()
    mqtt_cfg = cfg['mqtt']
    client = MQTTClient(
        CLIENT_ID, mqtt_cfg["broker"], 
        port=mqtt_cfg["port"], 
        keepalive=mqtt_cfg["keepalive"])
    will_msg = {'id': CLIENT_ID, 
        'status': False, 
        'msg': 'The connection from this device is lost:('
    }
    client.set_last_will('/device/will/status', json.dumps(will_msg))
    client.set_callback(on_message)
    client.connect()
    client.subscribe('/device/{0}/switch'.format(CLIENT_ID.decode("utf-8")), 0)

async def dth_read():
    global client
    global d
    global oled
    global CLIENT_ID
    topic = 'micro/{0}/temperature'.format(CLIENT_ID.decode("utf-8"))
    while True:
        d.measure()
        oled.fill(0)
        oled.text('ESP32', 45, 5)
        oled.text('MicroPython', 20, 20)
        oled.text('T:{0:.2f} C'.format(d.temperature()), 3, 35) 
        oled.text('H:{0:.2f} %'.format(d.humidity()), 3, 50)
        oled.show()
        msg =  json.dumps({
            'heap': gc.mem_free(), 'Type':7,
            'Id': CLIENT_ID, 
            'temperature': '{0:.2f}'.format(d.temperature()), 
            'humidity': '{0:.2f}'.format(d.humidity())
        }) 
        print(topic, msg) 
        client.publish(topic, msg)
        await asyncio.sleep(5)

loop.run_until_complete(wifi_config())
loop.create_task(dth_read())
loop.run_forever()

