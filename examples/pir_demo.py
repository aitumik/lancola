# PIR motion sensor
# Wiring: OUT -> GPIO 14, VCC -> 5V, GND -> GND
#         LED: GPIO 23 -> 220 ohm -> LED -> GND
# After power-up the sensor needs up to a minute to settle.
# The orange knobs set sensitivity and how long OUT stays high.
# No driver needed.

from machine import Pin
from time import sleep, ticks_ms

pir = Pin(14, Pin.IN)
led = Pin(23, Pin.OUT)

print("Warming up...")
sleep(10)
print("Ready")

# Polling: check the pin in a loop
last = 0
for _ in range(600):          # about 60 seconds
    now = pir.value()
    if now and not last:
        print("Motion!", ticks_ms() // 1000, "s")
    if last and not now:
        print("...quiet")
    led.value(now)
    last = now
    sleep(0.1)

led.off()
