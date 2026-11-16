# 4x4 membrane keypad
# Wiring, ribbon facing you, wires 1-8 left to right:
#   1-4 are rows    -> GPIO 19, 18, 5, 17
#   5-8 are columns -> GPIO 16, 4, 33, 32
# No resistors needed: the columns use the ESP32's internal pull-ups.
# Install: mpremote mip install github:aitumik/lancola/drivers/keypad

from machine import Pin
from time import sleep_ms
from keypad import Keypad

keys = Keypad(rows=(19, 18, 5, 17), cols=(16, 4, 33, 32))
led = Pin(23, Pin.OUT)

# 1. Print keys as they are pressed (D to go on)
print("Press keys, D to continue")
while True:
    key = keys.get_key()       # never waits, returns each press once
    if key:
        print("key", key)
        if key == "D":
            break
    sleep_ms(10)

# 2. Type a number: * deletes, # is enter
print("Type a number and press #  (* = delete)")
text = keys.read_text(echo=lambda t: print("  >", t))
print("You typed", text)

# 3. A simple lock: the LED turns on for the right PIN
PIN = "1234"
for attempt in range(3):
    print("Enter PIN then #")
    if keys.read_text(max_len=8) == PIN:
        print("Unlocked!")
        led.on()
        sleep_ms(2000)
        led.off()
        break
    print("Wrong PIN")
else:
    print("Locked out")

# With the LCD:
#   from lcd1602 import LCD
#   lcd = LCD()
#   def show(t):
#       lcd.clear()
#       lcd.write("PIN:\n" + "*" * len(t))
#   keys.read_text(echo=show)
