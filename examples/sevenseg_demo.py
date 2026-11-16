# Seven-segment LED display (1 digit, common cathode)
# Wiring (through a 220 ohm resistor on each segment):
#   a -> 13, b -> 14, c -> 27, d -> 26, e -> 25, f -> 33, g -> 32, dp -> 23
#   common (COM) -> GND   (common anode: COM -> 3.3V and use common_anode=True)
# Install: mpremote mip install github:aitumik/lancola/drivers/sevenseg

from time import sleep
from sevenseg import SevenSeg

seg = SevenSeg()     # SevenSeg(common_anode=True) for a common anode display

# Count 0-9
for n in range(10):
    seg.show(n)
    sleep(0.5)

# Hex letters, with the dot on
for ch in "AbCdEF":
    seg.show(ch + ".")
    sleep(0.5)

# Light each segment in turn: a, b, c, d, e, f, g, dp
for i in range(8):
    seg.set_segments(1 << i)
    sleep(0.3)

seg.clear()

# 4-digit display: wire the 4 digit pins too (D1-D4, left to right).
# Only one digit is lit at a time, switched fast enough that you see all four.
#
# Option 1: hold() keeps the digits lit while it runs.
# seg4 = SevenSeg(digits=(4, 16, 17, 18))
# for n in range(100):
#     seg4.number(n / 10, decimals=1)   # shows "0.0" ... "9.9"
#     seg4.hold(200)
# seg4.clear()
#
# Option 2: start() lets a timer do it, so sleep() and sensors are fine.
# seg4 = SevenSeg(digits=(4, 16, 17, 18))
# seg4.start()
# for n in range(100):
#     seg4.number(n)
#     sleep(0.2)
# seg4.stop()
