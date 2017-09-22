from machine import I2C, Pin
import ssd1306
import gfx
import time
import gc

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
graphics = gfx.GFX(128, 64, display.pixel)
display.fill(0)

while True:
    # Clear screen and draw a red line.
    display.fill(0)
    graphics.line(0, 0, 128, 64, 1)
    graphics.line(0, 64, 128, 0, 1)
    display.show()
    time.sleep(.5)
    # Clear screen and draw a green rectangle.
    display.fill(0)
    graphics.rect(0, 0, 128, 64, 1)
    graphics.circle(60, 30, 20, 1)
    graphics.triangle(60, 5,  45, 40,  15, 40, 1)
    display.show()
    time.sleep(.5)
    # Clear screen and draw a filled green rectangle.
    display.fill(0)
    graphics.fill_rect(0, 0, 128, 64, 1)
    display.show()
    time.sleep(.5)
    # Clear screen and draw a blue circle.
    display.fill(0)
    graphics.circle(60, 30, 20, 1)
    display.show()
    time.sleep(.5)
    # Clear screen and draw a filled blue circle.
    display.fill(0)
    graphics.fill_circle(60, 20, 20, 1)
    display.show()
    time.sleep(.5)
    # Clear screen and draw a pink triangle.
    display.fill(0)
    graphics.triangle(60, 5,  45, 40,  15, 40, 1)
    display.show()
    time.sleep(.5)
    # Clear screen and draw a filled pink triangle.
    display.fill(0)
    graphics.fill_triangle(60, 5,  45, 40,  15, 40, 1)
    display.show()
    time.sleep(.5)
    
