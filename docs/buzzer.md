# buzzer: passive buzzer tones and melodies

    mpremote mip install github:aitumik/lancola/drivers/buzzer

## Wiring

| Passive buzzer | ESP32 |
|---|---|
| + | 27 |
| - | GND |

Active or passive? The active buzzer usually has a sealed bottom and beeps
with plain 3.3V. The passive one shows a circuit board underneath and is
silent on plain DC. This driver is for the passive one; for the active buzzer,
use `Pin(27, Pin.OUT).on()`.

## Usage

```python
from buzzer import Buzzer

bz = Buzzer(27)
bz.beep()
bz.tone(440, 500)               # Hz, ms
bz.note("C5", 300)
bz.play("C4:1 E4:1 G4:2 R:1 C5:2", tempo=120)
```

## API

| Method | What it does |
|---|---|
| `Buzzer(pin=27, volume=50)` | Set up; volume 0-50 is the PWM duty |
| `tone(freq, ms=None)` | Play a frequency; with `ms`, stop after that time |
| `note(name, ms=None)` | Play a note: `"A4"`, `"C#5"`, `"Bb3"` |
| `beep(ms=100, freq=2000)` | Short beep |
| `play(song, tempo=120)` | Melody: `"note:beats ..."` or `[(note, beats), ...]` |
| `off()` | Silence |
| `note_freq(name)` | Function: note name → Hz (`R` = rest = 0) |

## How it works

A passive buzzer is a small speaker. Switching it on and off `freq` times
a second makes a tone of that pitch. A4 is 440 Hz, and each octave up doubles
the frequency: `freq = 440 × 2^((note − 69) / 12)`.
