from umqtt import MQTTClient 
import time, dht
from machine import Pin
import machine, ubinascii, gc, json
import network
gc.collect()
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
d = None
client = None
def wifi(cfg):
    global client
    global CLIENT_ID    
    client = MQTTClient(CLIENT_ID, cfg['broker'], port=cfg['port'], keepalive=cfg["keepalive"])
    client.connect() 
    print("MQTT client id:", CLIENT_ID)
    time.sleep(2)
    run()
def load_config():
    print('load configuration')
    f = open('config.json')
    cfg = json.loads(f.read())
    f.close()
    return cfg     
def setup():
    global d
    d = dht.DHT22(Pin(2)) 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    cfg = load_config()
    ap = cfg['ap']
    wlan.connect(ap['ssid'], ap['pwd'])
    while not wlan.isconnected():
        machine.idle()
    wifi(cfg['mqtt']) 
def get_temperature():
    global d 
    d.measure()
    return (d.temperature(), d.humidity())
def run():  
    global oled 
    global CLIENT_ID    
    while True:
        try:
            t, h = get_temperature()
            msg =  json.dumps({ 'Heap': gc.mem_free(),  'Type':7, 'id': CLIENT_ID, 'temperature': '{0:.2f}'.format(t), 'humidity': '{0:.2f}'.format(h)})
            print(msg)
            client.publish('micro/{0}/temperature'.format(CLIENT_ID.decode("utf-8")), msg)
        except OSError as e:
            if e.args[0] == errno.ETIMEDOUT:
                print('error dht: ', e)
        time.sleep(5)
setup()
