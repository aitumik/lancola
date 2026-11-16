# IR remote
# Wiring (receiver module): S / OUT -> GPIO 19, + -> 3.3V, - -> GND
#         LED: GPIO 23 -> 220 ohm -> LED -> GND
# Install: mpremote mip install github:aitumik/lancola/drivers/ir_nec

from machine import Pin
from time import sleep_ms
from ir_nec import IR, KEYS

ir = IR(19)
led = Pin(23, Pin.OUT)

# 1. Print every key. Use this to find codes for a different remote.
print("Press keys on the remote. Press OK to go on.")
while True:
    code = ir.read()
    if code is not None:
        name = KEYS.get(code, "unknown")
        print("code 0x{:02X} -> {}".format(code, name))
        if name == "OK":
            break
    sleep_ms(10)

# 2. Control the LED: 1 = on, 0 = off, OK = toggle. Press # to stop.
print("1 = LED on, 0 = LED off, OK = toggle, # = stop")
while True:
    key = ir.read_key()
    if key == "1":
        led.on()
    elif key == "0":
        led.off()
    elif key == "OK":
        led.value(not led.value())
    elif key == "#":
        break
    sleep_ms(10)

# 3. Callbacks: the driver calls your function for you.
#    Holding a key down sends repeats, handy for volume or motor speed.
level = 0

def changed(code):
    global level
    if code == 0x46 or (code == -1 and ir.last == 0x46):    # UP (held)
        level = min(10, level + 1)
    elif code == 0x15 or (code == -1 and ir.last == 0x15):  # DOWN (held)
        level = max(0, level - 1)

ir.on_press(changed)
print("Hold UP / DOWN for 10 seconds")
for _ in range(100):
    print("level", "#" * level, end="          \r")
    sleep_ms(100)
ir.stop()
led.off()
print()
