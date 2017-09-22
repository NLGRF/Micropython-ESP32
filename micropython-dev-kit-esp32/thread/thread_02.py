import _thread as th
import time
from machine import Pin

led1 = Pin(23, Pin.OUT)
led2 = Pin(22, Pin.OUT)
buzzer = Pin(21, Pin.OUT)
btn = Pin(19, Pin.IN)
def th1(e):
    print('thread 1 start', e)
    while True:
        led1.value(not led1.value())
        time.sleep(e)
def th2(e):
    print('thread 2 start', e)
    while True:
        led2.value(not led2.value())
        time.sleep(e)
def th3(e):
    print('thread 2 start')
    while True:
        if btn.value() == False:
            buzzer.value(1)
            time.sleep(.1)
            buzzer.value(0)
            while not btn.value():
                pass

th.start_new_thread(th1,  (3,))
th.start_new_thread(th3, (None,))
time.sleep(.5)
th.start_new_thread(th2, (.1,))


