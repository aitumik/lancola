# SG90 servo
# Wiring: brown -> GND, red -> 5V, orange (signal) -> GPIO 13
# Install: mpremote mip install github:aitumik/lancola/drivers/servo

from machine import Pin, ADC
from time import sleep, sleep_ms
from servo import Servo

servo = Servo(13)

for angle in (0, 90, 180, 90):
    print("angle", angle)
    servo.angle(angle)
    sleep(1)

# Sweep slowly
for angle in range(0, 181, 2):
    servo.angle(angle)
    sleep_ms(15)
for angle in range(180, -1, -2):
    servo.angle(angle)
    sleep_ms(15)

# Steer with the potentiometer (middle leg -> GPIO 36)
pot = ADC(Pin(36))
pot.atten(ADC.ATTN_11DB)
print("Turn the potentiometer for 10 seconds")
for _ in range(500):
    servo.angle(pot.read_u16() * 180 // 65535)
    sleep_ms(20)

servo.off()
