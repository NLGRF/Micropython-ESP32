from machine import Pin
import uasyncio as asyncio
import gc
print('Start Free: ', gc.mem_free())
#create event loop
loop = asyncio.get_event_loop()
led1 = Pin(4, Pin.OUT)
led2 = Pin(23, Pin.OUT)

@asyncio.coroutine
def loop1():
    while True:
        led1.value(not led1.value())
        await asyncio.sleep(1)
        
@asyncio.coroutine
def loop2():
    while True:
        led2.value(not led2.value())
        await asyncio.sleep(3)

@asyncio.coroutine
def loop_mem():
    while True:
        print('Free: {0:.2f}Kb'.format(gc.mem_free()/1000))
        #gc.collect()
        await asyncio.sleep(2)
    
        
@asyncio.coroutine
def loop3():
    while True:
        yield

loop.create_task(loop1())
loop.create_task(loop2())
loop.create_task(loop_mem())
loop.run_forever()
#loop.run_until_complete(loop3())
loop.close()
