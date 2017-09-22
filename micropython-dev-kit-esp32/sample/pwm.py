from machine import PWM
from machine import Pin

pinPWM = Pin(4)
pwm = PWM(pinPWM)
pwm.freq(500)
pwm.duty(512)

