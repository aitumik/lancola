# Photoresistor (light sensor): night light
# Wiring (voltage divider):
#   3.3V -> photoresistor -> GPIO 35 -> 10k resistor -> GND
#   LED: GPIO 23 -> 220 ohm -> LED -> GND
# More light = lower resistance = higher reading.
# No driver needed.

from machine import Pin, ADC
from time import sleep_ms

light = ADC(Pin(35))
light.atten(ADC.ATTN_11DB)
led = Pin(23, Pin.OUT)

DARK = 20000   # cover the sensor with your hand and adjust this

for _ in range(200):
    level = light.read_u16()
    led.value(level < DARK)
    bar = "#" * (level // 2048)
    print("{:5d} {}".format(level, bar))
    sleep_ms(100)

led.off()
