# sevenseg: 7-segment display (1 or 4 digits)

    mpremote mip install github:aitumik/lancola/drivers/sevenseg

## Wiring: single digit (10 pins)

```
  g   f  COM  a   b          front view,
 ┌───────────────┐           decimal point bottom right
 │       8.      │
 └───────────────┘
  e   d  COM  c  dp
```

Each segment through a 220 ohm resistor:
a 13, b 14, c 27, d 26, e 25, f 33, g 32, dp 23.
COM to GND (common cathode) or 3.3V (common anode).

## Wiring: 4-digit tube (12 pins)

```
 12  11  10   9   8   7
 D1   a   f  D2  D3   b
 ┌─────────────────────┐
 │  8.   8.   8.   8.  │
 └─────────────────────┘
  e   d  dp   c   g  D4
  1   2   3   4   5   6
```

Segments as above (with resistors). Digit pins D1 4, D2 16, D3 17, D4 18 (no resistors).

## Usage

```python
from sevenseg import SevenSeg

seg = SevenSeg()                # one digit, common cathode
seg.show(7)
seg.show("A.")                  # "." lights the decimal point

seg4 = SevenSeg(digits=(4, 16, 17, 18))
seg4.start()                    # keep it lit in the background
seg4.number(3.14, decimals=2)
seg4.show("HELP")
```

A 4-digit tube lights one digit at a time, switching fast enough that your eye
sees all four. Either let a timer do that with `start()`, or keep calling
`hold(ms)` / `refresh()` yourself.

## API

| Method | What it does |
|---|---|
| `SevenSeg(segments=(13,14,27,26,25,33,32,23), digits=(), common_anode=False)` | Set up |
| `show(text, align="right")` | Show digits/letters; `.` adds a decimal point |
| `number(value, decimals=0)` | Show a number |
| `set_segments(bits)` | Light segments directly: bit 0 = a ... bit 7 = dp |
| `clear()` | Blank |
| `start(timer=1, ms_per_digit=3)` | 4 digits: refresh in the background |
| `stop()` | Stop background refresh |
| `hold(ms)` | 4 digits: stay lit for ms (blocks) |
| `refresh()` | 4 digits: light each digit once |

`FONT` maps characters to segment bits; `SevenSeg.encode(ch)` looks one up.

Nothing lights, or the digits look inverted? Use `common_anode=True`.
