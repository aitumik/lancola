# keypad: 4x4 membrane keypad

    mpremote mip install github:aitumik/lancola/drivers/keypad

## Wiring

With the keypad face up and the ribbon pointing at you, wires 1-8 from left to right:

| Wire | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Meaning | Row 1 | Row 2 | Row 3 | Row 4 | Col 1 | Col 2 | Col 3 | Col 4 |
| ESP32 | 19 | 18 | 5 | 17 | 16 | 4 | 33 | 32 |

No resistors are needed. Column pins must support pull-ups, so don't use 34-39 for them.
If the keys come out wrong, the ribbon is reversed: reverse both tuples in your code.

## Usage

```python
from keypad import Keypad

keys = Keypad(rows=(19, 18, 5, 17), cols=(16, 4, 33, 32))

key = keys.get_key()            # in a loop: each press once, never waits
key = keys.wait_key()           # wait for one press
pin = keys.read_text()          # type, * deletes, # finishes
```

## API

| Method | What it does |
|---|---|
| `Keypad(rows, cols, layout=LAYOUT, debounce_ms=30)` | Set up |
| `scan()` | Key held right now, or None (no debouncing) |
| `get_key()` | New press, or None. Debounced, never blocks |
| `wait_key(timeout_ms=None)` | Wait for a press |
| `read_text(end="#", clear="*", max_len=16, echo=None)` | Collect a string; `echo(text)` after each key |

`layout` is a list of strings, one per row. A 3x4 keypad:

```python
Keypad(rows=(19, 18, 5, 17), cols=(16, 4, 33), layout=("123", "456", "789", "*0#"))
```

## How it works

Each key connects one row wire to one column wire. Columns are pulled HIGH.
The driver pulls one row LOW at a time; if a column reads LOW, the key at
that row and column is pressed. Idle rows are left as inputs, so pressing two
keys at once can't short two outputs together.
