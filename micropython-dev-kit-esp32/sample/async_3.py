import uasyncio as asyncio
from dht import DHT22
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import network, json
from umqtt import MQTTClient
import machine, ubinascii
import errno, time, gc

client = None
cfg = None
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
btn = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(23, Pin.OUT)
dthPn = Pin(17)
btn1 = Pin(5, Pin.IN)
btn2 = Pin(2, Pin.IN)
scl = Pin(22)
sda = Pin(21)
pins = [None, Pin(23, Pin.OUT), Pin(19, Pin.OUT), Pin(18, Pin.OUT), Pin(4, Pin.OUT)]
i2c = I2C(scl=scl, sda=sda, freq=100000)
oled = SSD1306_I2C(128, 64, i2c,  addr=0x3C)
oled.fill(0)
oled.text('ESP32', 45, 5)
oled.text('MicroPython', 20, 20)
oled.show()
loop = asyncio.get_event_loop()
d = DHT22(dthPn)

def btn_callback(e):
    global client
    global CLIENT_ID
    topic = 'micro/{0}/alarm'.format(CLIENT_ID.decode("utf-8"))
    msg = None
    if e is btn1:
      msg = json.dumps({'type': 'room1', 'msg': 'alarm'})
    else:
      msg = json.dumps({'type': 'room2', 'msg': 'alarm'})

    client.publish(topic, msg)

def on_message(topic, msg):
    global CLIENT_ID
    print(topic, msg)
    try:
        t = '/device/{0}/switch'.format(CLIENT_ID.decode("utf-8"))
        if t == topic.decode("utf-8"):
            obj = json.loads(msg)
            pin = pins[obj['gpio']]
            if not pin is None:
                pin.value(obj['value'])
    except OSError as e:
        print('JSON Error: ', e)    

def load_config():
    print('load configuration')
    f = open('config.json')
    cfg = json.loads(f.read())
    f.close()
    return cfg  

def mqtt_connection(cfg):
    global client
    global CLIENT_ID
    client = MQTTClient(
        CLIENT_ID, cfg["broker"], 
        port=cfg["port"], 
        keepalive=cfg["keepalive"])
    will_msg = {'id': CLIENT_ID, 
        'status': False, 
        'msg': 'The connection from this device is lost:('
    }
    client.set_last_will('/device/will/status', json.dumps(will_msg))
    client.set_callback(on_message)
    client.connect()
    client.subscribe('/device/{0}/switch'.format(CLIENT_ID.decode("utf-8")), 0)    

async def client_loop():
    global client 
    global loop
    while True:
        try:
            client.wait_msg()
        except OSError as e:
            loop.stop()
            print('error mqtt client: ', e)
            print('restart mqtt client') 
            cfg = load_config() 
            mqtt_cfg = cfg['mqtt']
            print('restart mqtt client: ', mqtt_cfg) 
            loop.run_until_complete(mqtt_connection(mqtt_cfg)) 
            loop.run_forever()
        yield

async def wifi_config():
    global cfg
    global client
    global CLIENT_ID 
    cfg = load_config()
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
    mqtt_connection(mqtt_cfg)

async def dth_read():
    global client
    global d
    global oled
    global CLIENT_ID
    global loop
    topic = 'micro/{0}/temperature'.format(CLIENT_ID.decode("utf-8"))
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
                'Id': CLIENT_ID, 
                'temperature': '{0:.2f}'.format(d.temperature()), 
                'humidity': '{0:.2f}'.format(d.humidity())
            })      
            print(topic, msg)
            client.publish(topic, msg)
        except OSError as e:
            if e.args[0] == errno.ETIMEDOUT:
                print('error dht: ', e)
            else:
                loop.stop()
                print('error mqtt client: ', e)
                print('restart mqtt client') 
                cfg = load_config() 
                mqtt_cfg = cfg['mqtt']
                print('restart mqtt client: ', mqtt_cfg) 
                loop.run_until_complete(mqtt_connection(mqtt_cfg)) 
                loop.run_forever()
                continue     

        await asyncio.sleep(5)

btn1.irq(trigger=Pin.IRQ_FALLING, handler=btn_callback)
btn2.irq(trigger=Pin.IRQ_FALLING, handler=btn_callback)
loop.run_until_complete(wifi_config())
loop.create_task(dth_read())
loop.create_task(client_loop())
loop.run_forever()

