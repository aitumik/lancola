# 1602 LCD
# Wiring: GND -> GND, VCC -> 5V, SDA -> 19, SCL -> 22
# Install: mpremote mip install github:aitumik/lancola/drivers/lcd1602

from time import sleep
from lcd1602 import LCD

lcd = LCD()          # use LCD(sda=21) if SDA is wired to pin 21
lcd.scan()           # should print ['0x27'] (some boards use 0x3f)

# Two lines of text
lcd.write("Hello, class!\nlancola LCD")
sleep(2)

# Write at a specific spot: column 0-15, row 0-1
lcd.clear()
lcd.write("Count:")

for n in range(11):
    lcd.move_to(7, 0)
    lcd.write(str(n) + " ")   # trailing space wipes the old digit
    sleep(0.5)

# Blink the backlight
lcd.move_to(0, 1)
lcd.write("Blink!")
for _ in range(3):
    lcd.backlight(False)
    sleep(0.3)
    lcd.backlight(True)
    sleep(0.3)
