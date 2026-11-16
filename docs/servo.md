# servo: SG90 servo

    mpremote mip install github:aitumik/lancola/drivers/servo

## Wiring

| Servo wire | ESP32 |
|---|---|
| Brown | GND |
| Red | 5V |
| Orange | 13 |

## Usage

```python
from servo import Servo

s = Servo(13)
s.angle(90)
s.off()                         # stop holding position
```

## API

| Method | What it does |
|---|---|
| `Servo(pin=13, min_us=500, max_us=2400, max_angle=180)` | Set up |
| `angle(degrees)` | Move to 0-180; with no argument returns the last angle |
| `pulse_us(us)` | Send a raw pulse width |
| `off()` | Stop pulses (servo goes limp and quiet) |
| `deinit()` | Release the PWM channel |

## How it works

The servo expects a pulse every 20 ms (50 Hz). The pulse width sets the angle:
about 0.5 ms is 0° and 2.4 ms is 180°. If yours buzzes at the ends or
doesn't reach them, adjust `min_us`/`max_us`.

If the board resets when the servo moves, power the servo from the battery holder
(keep GND shared).
