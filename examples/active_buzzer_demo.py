# Active buzzer: has its own oscillator, so it beeps when given power.
# Wiring: + (long leg / marked +) -> GPIO 27, - -> GND
# No driver needed. For tunes use the passive buzzer: see buzzer_demo.py

from machine import Pin
from time import sleep, sleep_ms

buzzer = Pin(27, Pin.OUT, value=0)

buzzer.on()
sleep(0.5)
buzzer.off()
sleep(0.5)

# Morse code SOS
DOT, DASH = 150, 450
for symbol in "...---...":
    buzzer.on()
    sleep_ms(DOT if symbol == "." else DASH)
    buzzer.off()
    sleep_ms(DOT)
