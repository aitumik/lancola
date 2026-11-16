# Passive buzzer: plays notes and tunes
# Wiring: + -> GPIO 27, - -> GND
# (The active buzzer only beeps one pitch: see active_buzzer_demo.py)
# Install: mpremote mip install github:aitumik/lancola/drivers/buzzer

from time import sleep, sleep_ms
from buzzer import Buzzer

bz = Buzzer(27)

bz.beep()
sleep(0.5)

# Raw frequencies: a siren
for _ in range(3):
    for f in range(600, 1500, 20):
        bz.tone(f)
        sleep_ms(5)
    for f in range(1500, 600, -20):
        bz.tone(f)
        sleep_ms(5)
bz.off()
sleep(0.5)

# Notes by name: a C major scale
for n in ("C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"):
    bz.note(n, 250)
sleep(0.5)

# A tune: "note:beats", R is a rest
bz.play("C4:1 C4:1 G4:1 G4:1 A4:1 A4:1 G4:2 "
        "F4:1 F4:1 E4:1 E4:1 D4:1 D4:1 C4:2", tempo=160)
