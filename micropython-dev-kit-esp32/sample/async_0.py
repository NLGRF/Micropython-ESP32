import uasyncio as asyncio
from machine import Pin

led1 = Pin(23, Pin.OUT)
led2 = Pin(4, Pin.OUT)

loop = asyncio.get_event_loop()

async def loop1():
    while True:
        led1.value(not led1.value())
        await asyncio.sleep(.1)

async def loop2():
    while True:
        led2.value(not led2.value())
        await asyncio.sleep(1)

loop.create_task(loop1())
loop.create_task(loop2())
loop.run_forever()



