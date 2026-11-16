# Parts that need no driver

These use modules already built into MicroPython. See the matching example.

| Part | MicroPython | Example |
|---|---|---|
| LED | `Pin(23, Pin.OUT)`, `.on()`, `.off()` | `blink_demo.py` |
| Button | `Pin(39, Pin.IN)`, `.value()`, `.irq()` | `button_demo.py` |
| RGB LED | `PWM(Pin(25), freq=1000)`, `.duty_u16(0-65535)` | `rgb_led_demo.py` |
| Active buzzer | `Pin(27, Pin.OUT)`, `.on()` | `active_buzzer_demo.py` |
| Potentiometer | `ADC(Pin(36))`, `.read_u16()` | `potentiometer_demo.py` |
| Photoresistor | `ADC(Pin(35))` + 10k divider | `photoresistor_demo.py` |
| PIR motion | `Pin(14, Pin.IN)`, 1 = motion | `pir_demo.py` |
| DHT11 | `dht.DHT11(Pin(4))`, `.measure()`, `.temperature()`, `.humidity()` | `dht11_demo.py` |
| S8050 transistor | `Pin(25, Pin.OUT)` on the base through 1k | `transistor_demo.py` |

## Quick reference

```python
from machine import Pin, PWM, ADC

led = Pin(23, Pin.OUT)
led.value(1)                  # on
button = Pin(39, Pin.IN)
button.value()                # 0 or 1

pwm = PWM(Pin(23), freq=1000)
pwm.duty_u16(32768)           # half brightness

adc = ADC(Pin(36))
adc.atten(ADC.ATTN_11DB)      # full 0-3.3V range
adc.read_u16()                # 0-65535
adc.read_uv()                 # microvolts
```

## Button modules vs bare buttons

The kit's button modules have their own resistor and read **1 when pressed**.
A bare 4-leg push button wired to GND reads **0 when pressed**, using
`Pin(32, Pin.IN, Pin.PULL_UP)` (not on GPIO 34-39, which have no pull-up).

Buttons bounce: one press can look like several. See `button_demo.py`
or `helpers/debounce.py`.
