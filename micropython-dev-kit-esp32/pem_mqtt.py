from machine import UART, Pin, I2C
import time, gc, json
from ssd1306 import SSD1306_I2C
import _thread as th
import network
from umqtt import MQTTClient
import machine, ubinascii
import _thread as th

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
scl = Pin(22)
sda = Pin(21)
i2c = I2C(scl=scl, sda=sda, freq=100000)
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text('ESP32', 45, 5)
oled.text('MicroPython', 20, 20)
oled.show()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('<SSID>', '<PWD>')
while not wlan.isconnected():
    print('wait connection')
    time.sleep(.5)
print('WIFI Connected: ', wlan.ifconfig()[0])

def on_message(topic, msg):
    print(topic.decode('utf-8'), msg.decode('utf-8'))

client = MQTTClient( CLIENT_ID, '103.13.228.61', port=1883, keepalive=15)
time.sleep(2)
client.set_callback(on_message)
client.connect()
client.subscribe('/micro/switch/1')
client.subscribe('/micro/switch/2')

def run(e):
    while True:
        try:
            s = uart.read()
            if s :
                o = json.loads(s.decode("utf-8"))
                print(o)
                oled.fill(0)
                oled.text('ESP32', 45, 5)
                oled.text('Voltage: {0:.0f}V'.format(o['v']), 1, 20) 
                oled.text('Current: {0:.2f}A'.format(o['i']), 1, 30)
                oled.text('Power  : {0:.0f}W'.format(o['p']), 1, 40)
                oled.text('Energy : {0:.0f}Wh'.format(o['e']), 1, 50)
                oled.show()
                topic = '/power/energy'
                client.publish(topic, s)
                
                gc.collect()
        except OSError as e:
            print('Error: ', e)
        time.sleep(e)

def loop(e):
    client.wait_msg()

th.start_new_thread(loop, (None,))
th.start_new_thread(run, (1,)) 
