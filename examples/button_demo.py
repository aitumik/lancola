# Button toggles an LED
# Wiring:
#   Button module: S -> 39, + -> 3.3V, - -> GND  (reads 1 when pressed)
#   LED: GPIO 23 -> 220 ohm -> LED -> GND
# A bare push button instead: one leg -> GPIO 32, other leg -> GND,
#   use Pin(32, Pin.IN, Pin.PULL_UP) and PRESSED = 0.
# No driver needed.

from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff

button = Pin(39, Pin.IN)   # GPIO 34-39 have no internal pull-up/down
led = Pin(23, Pin.OUT)
PRESSED = 1

# 1. Read it directly: LED is on only while the button is held
for _ in range(300):          # about 3 seconds
    led.value(button.value() == PRESSED)
    sleep_ms(10)

# 2. Toggle on each press, with debouncing.
#    A button's metal contacts bounce for a few ms, which looks like
#    several presses. Ignoring changes for 50 ms after a press fixes that.
last = button.value()
last_time = ticks_ms()
presses = 0
while presses < 6:
    now = button.value()
    if now != last and ticks_diff(ticks_ms(), last_time) > 50:
        last_time = ticks_ms()
        last = now
        if now == PRESSED:
            led.value(not led.value())
            presses += 1
            print("press", presses)
    sleep_ms(5)

# 3. Interrupt: the ESP32 calls a function when the pin changes
count = 0

def pressed(pin):
    global count
    count += 1

button.irq(trigger=Pin.IRQ_RISING, handler=pressed)
print("Press the button for 5 seconds...")
sleep_ms(5000)
button.irq(handler=None)
print("Interrupt counted", count, "(more than your presses = bounce!)")
led.off()
