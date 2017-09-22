from umqtt import MQTTClient
import onewire
import time, ds18x20, ssd1306
from esp_board import WifiStation
from machine import I2C, Pin
import machine, ubinascii, gc, json
import config
machine.freq(160000000)
gc.collect() 
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
oled = None
ds = None
roms = None
client = None
def wifi():
    global client
    global CLIENT_ID    
    client = MQTTClient(CLIENT_ID, config.BROKER)
    client.connect() 
    print("MQTT client id:", CLIENT_ID)
    time.sleep(2)
    run()
def setup(): 
    global oled
    global ds
    global roms
    i2c = I2C(scl=Pin(2), sda=Pin(0), freq=100000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    ow = onewire.OneWire(Pin(5))
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    wlan = WifiStation()
    wlan.connect(config.SSID, config.PWD)
    wlan.wait_connection(wifi) 
def get_temperature():
    global ds
    global roms
    ds.convert_temp()
    return ds.read_temp(roms[0])
def run():  
    global oled
    global roms
    global CLIENT_ID
    if len(roms) != 0:    
        while True:
            t = get_temperature()
            msg =  json.dumps({ 'Heap': gc.mem_free(),  'Type':7, 'Id': CLIENT_ID, 'Temperature': '{0:.2f}'.format(t)})
            print(msg)
            client.publish('/device/53211900/temperature', msg)
            oled.fill(0)
            oled.text('Temp', 18, 10) 
            oled.text('{0:.2f}'.format(t), 12, 20)
            oled.show()
            time.sleep(5)

setup()
