import _thread as th
import time

def th1(e, o):
    print('thread 1 start', e, o)
    while True:
        print('thread 1 trick')
        time.sleep(e) 
def th2(e, o):
    print('thread 2 start', e, o)
    while True:
        print('thread 2 trick')
        time.sleep(e) 

th.start_new_thread(th1, (1,2,))
time.sleep(.5)
th.start_new_thread(th2, (.2,1,))