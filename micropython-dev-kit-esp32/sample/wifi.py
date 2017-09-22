import time
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('HUAWEI', '0000000000')
while not wlan.isconnected():
    print('Wait connection')
    time.sleep(1)

print(wlan.ifconfig()[0])
