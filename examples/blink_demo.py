# LED blink
# Wiring: GPIO 23 -> 220 ohm resistor -> LED long leg (+), short leg (-) -> GND
# No driver needed: machine.Pin is built in.

from machine import Pin
from time import sleep

led = Pin(23, Pin.OUT)

for _ in range(10):
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)

# Same thing, shorter
for _ in range(10):
    led.value(not led.value())
    sleep(0.2)

led.off()
