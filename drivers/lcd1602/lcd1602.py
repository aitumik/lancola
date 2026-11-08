from time import sleep_ms
from machine import Pin,I2C,SoftI2C

ENABLE = 0x04
BACKLIGHT = 0x08
CLEAR = 0x1
ENTRY_MODE = 0x06
DISPLAY_ON = 0x0C
FOUR_BIT_2_LINES = 0x28

class LCD:
    def __init__(self,scl=None,sda=None,addr=0x27):
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(19), freq=100000)
        self.addr = addr

    def scan(self):
        devices = self.i2c.scan()
        print("connected devices : ",[hex(d) for d in devices])

    def write(self,value):
        self.i2c.writeto(addr,byte([value | BACKLIGHT]))

    def pulse(self,bits):
        self.write(bits | ENABLE)
        self.write(bits)

    def send(self,byte,mode=0):
        self.pulse((byte & 0xF0) | mode)
        self.pulse(((byte << 4) & 0xF0) | mode)

    def start(self):
        sleep_ms(50)
        for _ in range(3):
            # self.send(0x30) what will it be
            self.pulse(0x30)
            sleep_ms(5)
        self.pulse(0x20)

        self.send(FOUR_BIT_2_LINES)
        self.send(DISPLAY_ON)
        self.send(ENTRY_MODE)
        self.send(CLEAR)
        sleep_ms(5)
