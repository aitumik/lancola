# DC motor (or the fan) on the kit's motor driver board
# Wiring:
#   Driver IN1 (A-1A) -> GPIO 25, IN2 (A-1B) -> GPIO 26
#   Driver VCC -> 5V (or battery pack +), GND -> GND (shared with the ESP32)
#   Motor (with the fan blade if you like) -> driver motor A screw terminals
# Never power a motor straight from a GPIO pin.
# Install: mpremote mip install github:aitumik/lancola/drivers/motor

from time import sleep, sleep_ms
from motor import Motor

motor = Motor(25, 26)

print("forward full speed")
motor.forward(100)
sleep(2)

print("stop")
motor.stop()
sleep(1)

print("reverse half speed")
motor.reverse(50)
sleep(2)
motor.brake()
sleep(1)

print("speed up, then slow down")
for speed in range(30, 101, 5):
    motor.forward(speed)
    sleep_ms(150)
for speed in range(100, 29, -5):
    motor.forward(speed)
    sleep_ms(150)

# run() takes -100 ... 100 in one number
for speed in (60, -60, 0):
    motor.run(speed)
    sleep(1.5)

motor.stop()
