from machine import Pin, ADC
import time

a1 = ADC(Pin(32))

AirValue = 736
WaterValue = 480
intervals = (AirValue - WaterValue)/3
soilMoistureValue = 0
while True:
    soilMoistureValue = a1.read()
    if (soilMoistureValue > WaterValue) and (soilMoistureValue < (WaterValue + intervals)):
        print("Very Wet")
    elif (soilMoistureValue > (WaterValue + intervals)) and (soilMoistureValue < (AirValue - intervals)):
        print("Wet")
    elif (soilMoistureValue < AirValue) and (soilMoistureValue > (AirValue - intervals)):
        print("Dry")
    time.sleep(1)
    

