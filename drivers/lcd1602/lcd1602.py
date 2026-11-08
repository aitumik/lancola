from time import sleep_ms
from machine import Pin,I2C,SoftI2C

RS = 0x01

ENABLE = 0x04
BACKLIGHT = 0x08
HOME = 0x02
CLEAR = 0x1
ENTRY_MODE = 0x06
DISPLAY_ON = 0x0C
FOUR_BIT_2_LINES = 0x28

SET_ADDRESS = 0x80

ROW_START = (0x00,0x40)

class LCD:
    def __init__(self,scl=None,sda=None,addr=0x27,freq=400000):
        self.i2c = SoftI2C(scl=Pin(scl), sda=Pin(sda), freq=freq)
        self.addr = addr
        self.light = BACKLIGHT
        self.start()

    def scan(self):
        devices = self.i2c.scan()
        print("connected devices : ",[hex(d) for d in devices])

    def pulse(self,bits):
        bits |= self.light
        self.i2c.writeto(self.addr,bytes((bits | ENABLE,bits)))

    def frame(self,value,mode):
        hi = (value & 0xF0) | mode | self.light
        lo = ((value << 4) & 0xF0) | mode | self.light
        return bytes((hi | ENABLE,hi,lo | ENABLE,lo))

    def send(self,value,mode=0):
        self.i2c.writeto(self.addr,self.frame(value,mode))

    def start(self):
        sleep_ms(50)
        for _ in range(3):
            self.pulse(0x30)
            sleep_ms(5)

        self.pulse(0x20)
        sleep_ms(1)

        self.send(FOUR_BIT_2_LINES)
        self.send(DISPLAY_ON)
        self.send(ENTRY_MODE)
        self.clear()

    def clear(self):
        self.send(CLEAR)
        sleep_ms(2)

    def home(self):
        self.send(HOME)
        sleep_ms(2)

    def move_to(self,col,row):
        self.send(SET_ADDRESS | (ROW_START[row] + col))

    def write(self,text):
        lines = str(text).split("\n")[:2]
        for idx,line in enumerate(lines):
            if idx > 0:
                self.move_to(0,1)
            buf = bytearray()
            for ch in line[:16]:
                buf += self.frame(ord(ch),RS)
            if buf:
                self.i2c.writeto(self.addr,buf)

    def backlight(self,on=True):
        self.light = BACKLIGHT if on else 0 
        self.i2c.writeto(self.addr,bytes((self.light,)))

