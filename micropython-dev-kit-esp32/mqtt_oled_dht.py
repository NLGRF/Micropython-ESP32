from umqtt import MQTTClient
import machine, ubinascii
import time, gc
import network
import json, errno
from dht import DHT22
from machine import Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import _thread as th
a1 = ADC(Pin(32))
a2 = ADC(Pin(33))
a3 = ADC(Pin(34))
scl = Pin(22)
sda = Pin(21)
i2c = I2C(scl=scl, sda=sda, freq=100000) 
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text('ESP32', 45, 5)
oled.text('MicroPython', 20, 20)
oled.text('System Startimg', 3, 35) 
oled.show()
dhtPn = Pin(17)
d = DHT22(dhtPn)
tim0 = Timer(0)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('see_dum', '0863219053')
while not wlan.isconnected():
    print('Wait connection')
    time.sleep(1)
oled.text('{0}'.format(wlan.ifconfig()[0]), 3, 50) 
oled.show()
time.sleep(3)

def read_soil(o):
    AirValue = 736
    WaterValue = 480
    intervals = (AirValue - WaterValue)/3 
    soilMoistureValue = o.read()
    result = None
    if (soilMoistureValue > WaterValue) and (soilMoistureValue < (WaterValue + intervals)):
        print("Very Wet") 
        result = {'level': 1, 'msg': ':]'};
    elif (soilMoistureValue > (WaterValue + intervals)) and (soilMoistureValue < (AirValue - intervals)):
        print("Wet")
        result = {'level': 2, 'msg': ':)'}; 
    elif (soilMoistureValue < AirValue) and (soilMoistureValue > (AirValue - intervals)):
        print("Dry")
        result = {'level': 3, 'msg': ':('}; 
    else:
        result = {'level': 0, 'msg': ';('};
    return result

def on_message(topic, msg):
    print(topic, msg)


CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(CLIENT_ID, '103.13.228.61', port=1883)
client.set_callback(on_message)
client.connect()
client.subscribe('micro/python/switch')

def loop_dht(o):
  global d
  global oled
  global CLIENT_ID
  global client
  global a1
  global a2
  global a3
  delay = o
  topic = 'micro/{0}/temperature'.format(CLIENT_ID.decode("utf-8"))
  while True:
    try:
      d.measure()
      oled.fill(0)
      soils = [{'id': 1, 'value': read_soil(a1)},
        {'id': 2, 'value': read_soil(a2)},
        {'id': 3, 'value': read_soil(a3)}]
      oled.text('SOIL SENSOR', 20, 5) 
      oled.text('T: {0:.1f}C,{1:.1f}%'.format(d.temperature(), d.humidity()), 3, 20) 
      oled.text('A1:{0}     A2:{1}'.format(soils[0]['value']['msg'],soils[1]['value']['msg']), 3, 35)
      oled.text('A3:{0}'.format(soils[2]['value']['msg']), 3, 50)
      oled.show()
      msg =  json.dumps({
          'Id': CLIENT_ID,
          'heap': gc.mem_free(),
          'temperature': '{0:.2f}'.format(d.temperature()), 
          'humidity': '{0:.2f}'.format(d.humidity()),
          'soils': soils
      })
      print(msg) 
      client.publish(topic, msg)
    except OSError as e:
      if e.args[0] == errno.ETIMEDOUT:
        print('error dht: ', e)
    time.sleep(delay)

def loop_msg(e):
  global client
  while True:
      try:
          client.wait_msg()
      except OSError as e:
          print('wait_msg: ', e)       
th.start_new_thread(loop_msg, (None,))
th.start_new_thread(loop_dht, (10,))
