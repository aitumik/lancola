# motor: DC motor and fan

    mpremote mip install github:aitumik/lancola/drivers/motor

## Wiring

| Motor driver | ESP32 / power |
|---|---|
| IN1 (A-1A) | 25 |
| IN2 (A-1B) | 26 |
| VCC | 5V, or the battery pack + |
| GND | GND (shared with the ESP32) |
| Motor A terminals | The DC motor (fit the fan blade for the fan) |

Never connect a motor straight to a GPIO pin. It draws far more current than
a pin can supply, and its voltage spikes can damage the ESP32.

## Usage

```python
from motor import Motor

m = Motor(25, 26)
m.forward(70)                   # 0-100 %
m.reverse(50)
m.stop()
```

## API

| Method | What it does |
|---|---|
| `Motor(in1=25, in2=26, freq=1000)` | Set up |
| `forward(speed=100)` | Spin forward, speed 0-100 % |
| `reverse(speed=100)` | Spin backwards |
| `run(speed)` | -100 to 100 in one number |
| `stop()` | Cut power, coast to a stop |
| `brake()` | Stop quickly |
| `speed` | Last speed set (negative = reverse) |

## How it works

| IN1 | IN2 | Motor |
|---|---|---|
| PWM | 0 | Forward |
| 0 | PWM | Reverse |
| 0 | 0 | Coast |
| 1 | 1 | Brake |

PWM switches the power on and off 1000 times a second. The share of time it's
on (duty cycle) sets the speed. Small motors often won't start below ~30 %.
