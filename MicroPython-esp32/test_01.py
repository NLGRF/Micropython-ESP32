from esp_board import Button, Led
led1 = Led(12)
led2 = Led(14)
btn1 = Button(4)
btn2 = Button(5)
def key_down(pin):
    if pin == 4:
        led1.toggle()
    if pin == 5:
        led2.toggle()

btn1.set_callback(key_down)
btn2.set_callback(key_down)
while True:
    btn1.process()
    btn2.process()
