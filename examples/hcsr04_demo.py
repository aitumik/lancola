# HC-SR04 ultrasonic distance sensor
# Wiring: VCC -> 5V, GND -> GND, TRIG -> GPIO 18, ECHO -> GPIO 34
#   ECHO is a 5V signal. Put a divider on it to be safe:
#   ECHO -> 1k -> GPIO 34 -> 2k (or 2 x 1k) -> GND
# Install: mpremote mip install github:aitumik/lancola/drivers/hcsr04

from machine import Pin
from time import sleep_ms
from hcsr04 import HCSR04

sensor = HCSR04(trig=18, echo=34)
led = Pin(23, Pin.OUT)

# Parking sensor: the LED blinks faster as things get closer
for _ in range(100):
    cm = sensor.distance_cm()
    if cm is None:
        print("nothing in range")
        led.off()
        sleep_ms(200)
        continue
    print("{:.1f} cm".format(cm))
    if cm < 10:
        led.on()
        sleep_ms(100)
    else:
        led.value(not led.value())
        sleep_ms(int(min(cm, 100) * 5))

led.off()
