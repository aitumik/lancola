# lancola

MicroPython drivers for the ACEBOTT ESP32 Basic Starter Kit (ESP32-WROOM-32E),
written for teaching: short, commented, and with no third-party dependencies.

## Install

Everything:

    mpremote mip install github:aitumik/lancola

One driver:

    mpremote mip install github:aitumik/lancola/drivers/ir_nec

From the Thonny shell (board on Wi-Fi):

    import mip
    mip.install("github:aitumik/lancola")

More options, including Thonny without internet: [docs/getting-started.md](docs/getting-started.md)

## Drivers

| Driver | Part | Import | Docs |
|---|---|---|---|
| lcd1602 | 16x2 I2C LCD | `from lcd1602 import LCD` | [docs](docs/lcd1602.md) |
| sevenseg | 7-segment display, 1 or 4 digits | `from sevenseg import SevenSeg` | [docs](docs/sevenseg.md) |
| ir_nec | IR receiver + remote | `from ir_nec import IR` | [docs](docs/ir_nec.md) |
| hcsr04 | Ultrasonic distance sensor | `from hcsr04 import HCSR04` | [docs](docs/hcsr04.md) |
| servo | SG90 servo | `from servo import Servo` | [docs](docs/servo.md) |
| motor | DC motor / fan on the motor driver | `from motor import Motor` | [docs](docs/motor.md) |
| buzzer | Passive buzzer tones and tunes | `from buzzer import Buzzer` | [docs](docs/buzzer.md) |
| keypad | 4x4 membrane keypad | `from keypad import Keypad` | [docs](docs/keypad.md) |

LEDs, buttons, the RGB LED, potentiometer, photoresistor, PIR, DHT11, active
buzzer and transistor need no driver: see [docs/basics.md](docs/basics.md).

Pin defaults and ESP32 pin rules: [docs/wiring.md](docs/wiring.md)

## Quick look

```python
from lcd1602 import LCD
from hcsr04 import HCSR04
from time import sleep

lcd = LCD()
sensor = HCSR04()

while True:
    cm = sensor.distance_cm()
    lcd.clear()
    lcd.write("Distance:\n" + ("--" if cm is None else "{:.1f} cm".format(cm)))
    sleep(0.5)
```

## Examples

One runnable file per part in [`examples/`](examples). Open it in Thonny and
press Run, or `mpremote run examples/servo_demo.py`. Examples aren't installed
on the board.
