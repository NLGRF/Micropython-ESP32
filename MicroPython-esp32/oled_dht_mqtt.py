from umqtt import MQTTClient 
import time, dht, i2c_ssd1306
from esp_board import WifiStation
from machine import I2C, Pin
import machine, ubinascii, gc, json
machine.freq(160000000)
gc.collect()
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
oled = None
d = None
client = None
def wifi():
    global client
    global CLIENT_ID    
    client = MQTTClient(CLIENT_ID, '27.254.63.34', port=1883, user='5857725C', password='8DB24662')
    client.connect() 
    print("MQTT client id:", CLIENT_ID)
    time.sleep(2)
    run()
def setup(): 
    global oled
    global d 
    i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
    oled = i2c_ssd1306.SSD1306_I2C(64, 32, i2c)
    d = dht.DHT22(Pin(2)) 
    wlan = WifiStation()
    wlan.connect('see_dum', '0863219053')
    wlan.wait_connection(wifi) 
def get_temperature():
    global d 
    d.measure()
    return (d.temperature(), d.humidity())
def run():  
    global oled 
    global CLIENT_ID    
    while True:
        t, h = get_temperature()
        msg =  json.dumps({ 'Heap': gc.mem_free(),  'Type':7, 'id': CLIENT_ID, 'Temperature': '{0:.2f}'.format(t), 'Humidity': '{0:.2f}'.format(h)})
        print(msg)
        client.publish(CLIENT_ID + '/5857725C/temperature', msg)
        oled.fill(0)
        oled.text('T:{0:.2f}'.format(t), 5, 10) 
        oled.text('H:{0:.2f}'.format(h), 5, 20)
        oled.show()
        time.sleep(5)
setup()
