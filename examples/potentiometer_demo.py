# Potentiometer: dims an LED
# Wiring:
#   Potentiometer: outer legs -> 3.3V and GND, middle leg -> GPIO 36 (VP)
#   LED: GPIO 23 -> 220 ohm -> LED -> GND
# Use ADC1 pins (GPIO 32-39) for analog: ADC2 pins stop working when Wi-Fi is on.
# No driver needed.

from machine import Pin, ADC, PWM
from time import sleep_ms

pot = ADC(Pin(36))
pot.atten(ADC.ATTN_11DB)     # measure the full 0-3.3V range

led = PWM(Pin(23), freq=1000, duty_u16=0)

for _ in range(200):          # about 20 seconds
    value = pot.read_u16()    # 0 ... 65535
    volts = pot.read_uv() / 1000000
    percent = value * 100 // 65535
    print("raw", value, " volts {:.2f}".format(volts), " ", percent, "%")
    led.duty_u16(value)
    sleep_ms(100)

led.duty_u16(0)
