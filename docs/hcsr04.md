# hcsr04: ultrasonic distance sensor

    mpremote mip install github:aitumik/lancola/drivers/hcsr04

## Wiring

| HC-SR04 | ESP32 |
|---|---|
| VCC | 5V |
| TRIG | 18 |
| ECHO | 34, through a divider: ECHO → 1k → pin 34 → 2k → GND |
| GND | GND |

ECHO outputs 5V, and the ESP32 is a 3.3V chip. The divider brings it down to about 3.3V.

## Usage

```python
from hcsr04 import HCSR04

sensor = HCSR04(trig=18, echo=34)
cm = sensor.distance_cm()       # None if nothing is in range
```

## API

| Method | What it does |
|---|---|
| `HCSR04(trig=18, echo=34, timeout_us=30000)` | Set up |
| `distance_cm()` | Distance in cm (float) or None |
| `distance_mm()` | Distance in mm (int) or None |
| `pulse_us()` | Raw echo time in µs (negative on timeout) |

## How it works

A 10 µs pulse on TRIG sends 8 bursts of 40 kHz sound. ECHO stays high until
the sound bounces back. Sound travels about 0.0343 cm per µs, and it went
there and back, so `distance = time × 0.0343 / 2`.

Range is about 2 cm to 4 m. Soft or angled surfaces may not echo.
