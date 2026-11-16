# ir_nec: IR receiver and remote

    mpremote mip install github:aitumik/lancola/drivers/ir_nec

## Wiring

| Receiver module | ESP32 |
|---|---|
| S / OUT | 19 |
| + | 3.3V |
| - | GND |

## Usage

```python
from ir_nec import IR

ir = IR(19)
while True:
    key = ir.read_key()         # "OK", "UP", "5", ... or None
    if key:
        print(key)
```

Or let the driver call a function:

```python
def pressed(code):
    print(hex(code))

ir.on_press(pressed)
```

## API

| Method | What it does |
|---|---|
| `IR(pin=19, timer=0)` | Start listening (uses a pin interrupt and a hardware timer) |
| `read(repeat=False)` | Newest command code (0-255), or None. Each press once |
| `read_key(repeat=False)` | Same, as a name from `KEYS` |
| `on_press(func)` | Call `func(code)` per message; `REPEAT` (-1) while a key is held |
| `stop()` | Stop listening |
| `last` / `address` | Last command and remote address |

`repeat=True` keeps returning the held key, useful for volume or speed.

## How it works

NEC sends a 9 ms burst, a 4.5 ms gap, then 32 bits. Every bit starts with a
0.56 ms burst; a short gap after it means 0 and a long gap (1.69 ms) means 1.
The bits are address, inverted address, command, inverted command, so the
receiver can check the command arrived correctly.

The pin interrupt only records the time of each edge. A timer then decodes
the message 80 ms later, outside the interrupt.

## A different remote

Run `examples/ir_nec_demo.py`, press each key and add the printed codes
to `KEYS` in your own code:

```python
from ir_nec import KEYS
KEYS[0x45] = "POWER"
```
