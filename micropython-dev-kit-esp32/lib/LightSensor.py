
class LightSensor(object):
    
    BH1750_Continuous_H_resolution_Mode = 0x10

    BH1750_Power_On = 0x01
    BH1750_Power_Down = 0x00
    BH1750_Reset = 0x07
    
    def __init__(self, i2c, addr=0x23):
        self.i2c = i2c
        self.addr = addr
        self.write_cmd(self.BH1750_Power_On)
        self.setMode(self.BH1750_Continuous_H_resolution_Mode)
    def setMode(self, mode):
        self.write_cmd(mode)
    def reset(self):
        self.write_cmd(self.BH1750_Power_On)
        self.write_cmd(self.BH1750_Reset)
    def sleep(self):
        self.write_cmd(self.BH1750_Power_Down)
    def getLightIntensity(self):
         value = i2c.readfrom(0x23, 2)
         lux = value[0] << 8
         lux |= value[1]
         lux = lux / 1.2
         return lux
    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([cmd,]))
