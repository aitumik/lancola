# S8050 NPN transistor as a switch
# A GPIO pin can only supply a few mA at 3.3V. A transistor lets that tiny
# current switch a bigger 5V load, here the active buzzer.
#
# S8050, flat side facing you, legs down: E  B  C (left to right)
# Wiring:
#   GPIO 25 -> 1k resistor -> B (base)
#   E (emitter) -> GND
#   C (collector) -> buzzer - ;  buzzer + -> 5V
# Do NOT drive a motor this way without a flyback diode; use the motor driver.
# No driver needed.

from machine import Pin
from time import sleep

base = Pin(25, Pin.OUT, value=0)

for _ in range(5):
    base.on()      # current into the base -> collector to emitter conducts
    sleep(0.3)
    base.off()     # no base current -> switch open
    sleep(0.7)
