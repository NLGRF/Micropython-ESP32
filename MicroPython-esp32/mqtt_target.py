from umqtt import MQTTClient 
import time
from esp_board import WifiStation, Button, Led
from machine import I2C, Pin
import machine, ubinascii, gc, json
machine.freq(160000000)
gc.collect()
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = None
btn = Button(0)
led = Led(2)
led.on();
def wifi():
    global client
    global CLIENT_ID    
    client = MQTTClient(CLIENT_ID, 'q.emqtt.com', port=1883)
    client.connect() 
    print("MQTT client id:", CLIENT_ID)
    time.sleep(2)
    run()
def setup():  
    wlan = WifiStation()
    wlan.connect('see_dum', '0863219053')
    wlan.wait_connection(wifi) 
def cb(pin):
    global CLIENT_ID
    try:
        if pin == 0:
            msg =  json.dumps({ 'Heap': gc.mem_free(),  'ModelId':7, 'id': CLIENT_ID,  'Model': 'DX-000-0001', 'Target': 1 })
            print(msg)
            client.publish('/target', msg)
            led.off()
            time.sleep(0.1)
            led.on()
    except OSError:
        print("connection error")
        client.connect()    

        
def run(): 
    global btn
    global client
    btn.set_callback(cb)
    while True:
        try:
            btn.process()
        except OSError:
            print("connection error") 
        

setup()
