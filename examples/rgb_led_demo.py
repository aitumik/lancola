# RGB LED (common cathode: longest leg -> GND)
# Wiring, each colour leg through a 220 ohm resistor:
#   R -> 25, G -> 26, B -> 27, longest leg -> GND
# Common anode LED (longest leg -> 3.3V)? Set COMMON_ANODE = True.
# No driver needed: PWM is built in.

from machine import Pin, PWM
from time import sleep, sleep_ms

COMMON_ANODE = False

red = PWM(Pin(25), freq=1000, duty_u16=0)
green = PWM(Pin(26), freq=1000, duty_u16=0)
blue = PWM(Pin(27), freq=1000, duty_u16=0)


def colour(r, g, b):
    """Each value 0-255, like colours on the web."""
    for pwm, v in ((red, r), (green, g), (blue, b)):
        if COMMON_ANODE:
            v = 255 - v
        pwm.duty_u16(v * 257)   # 255 * 257 = 65535


for name, rgb in (("red", (255, 0, 0)), ("green", (0, 255, 0)),
                  ("blue", (0, 0, 255)), ("yellow", (255, 255, 0)),
                  ("cyan", (0, 255, 255)), ("purple", (255, 0, 255)),
                  ("white", (255, 255, 255))):
    print(name)
    colour(*rgb)
    sleep(0.7)

# Fade through the rainbow
for _ in range(2):
    for i in range(256):
        colour(255 - i, i, 0)
        sleep_ms(4)
    for i in range(256):
        colour(0, 255 - i, i)
        sleep_ms(4)
    for i in range(256):
        colour(i, 0, 255 - i)
        sleep_ms(4)

colour(0, 0, 0)
