from machine import UART, Pin, I2C
import time, gc, json
from esp8266_i2c_lcd import I2cLcd
import network
from umqtt import MQTTClient
import machine, ubinascii
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
scl = Pin(22)
sda = Pin(21)
i2c = I2C(scl=scl, sda=sda, freq=100000)
lcd = I2cLcd(i2c, 0x3F, 4, 20)
lcd.clear()
lcd.putstr("--------------------")
lcd.putstr("       ESP32        ")
lcd.putstr("    MicroPython     ")
lcd.putstr("--------------------")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('see_dum', '0863219053')
while not wlan.isconnected():
    time.sleep(.5)
    print('wait connectio') 
print('WIFI Connected: ', wlan.ifconfig()[0])

def on_message(topic, msg):
    print(topic, msg)
time.sleep(2)
client = MQTTClient( CLIENT_ID, '103.13.228.61', port=1883, keepalive=15)
time.sleep(2)
client.set_callback(on_message)
client.connect()

def show_display(v, i, p, e):
    lcd.move_to(0, 0)
    lcd.putstr('Voltage: {0:.0f}   '.format(v))
    lcd.move_to(19, 0)
    lcd.putstr('V')
    lcd.move_to(0, 1)
    lcd.putstr('Current: {0:.2f}   '.format(i))
    lcd.move_to(19, 1)
    lcd.putstr('A')
    lcd.move_to(0, 2)
    lcd.putstr('Power  : {0:.0f}   '.format(p))
    lcd.move_to(19, 2)
    lcd.putstr('W')
    lcd.move_to(0, 3)
    lcd.putstr('Energy : {0:.0f}   '.format(e))
    lcd.move_to(18, 3)
    lcd.putstr('Wh')    

def run(e):
    lcd.clear()
    show_display(0.0,0.0,0.0,0.0)
    while True:
        try:
            s = uart.read()
            if s :
                o = json.loads(s.decode("utf-8"))
                print(o)
                show_display(o['v'], o['i'], o['p'], o['e'])
                topic = '/power/energy'
                client.publish(topic, s)
                gc.collect()
        except OSError as e:
            print('Error: ', e)
        time.sleep(e)
run(2) 
