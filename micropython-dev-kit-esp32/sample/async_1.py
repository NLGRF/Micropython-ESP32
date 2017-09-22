import uasyncio as asyncio
from machine import Pin

led1 = Pin(23, Pin.OUT)
led2 = Pin(4, Pin.OUT)
btn = Pin(5, Pin.IN, Pin.PULL_UP)
loop = asyncio.get_event_loop()
async def loop1():
    while True:
        led1.value(not led1.value())
        await asyncio.sleep(.1)

async def loop2():
    while True:
        led2.value(not led2.value())
        await asyncio.sleep(1)

async def loop3():
    while True:
        if btn.value() == 0:
            print('Button pressed...')
            while btn.value() == 0:
                yield
        await asyncio.sleep(.100)

loop.create_task(loop1())
loop.create_task(loop2())
loop.create_task(loop3())
loop.run_forever()
