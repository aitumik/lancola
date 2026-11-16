# DHT11 temperature and humidity
# Wiring (3-pin module): S / DATA -> GPIO 4, + -> 3.3V, - -> GND
# No driver needed: the dht module is built into MicroPython.

import dht
from machine import Pin
from time import sleep

sensor = dht.DHT11(Pin(4))

for _ in range(10):
    try:
        sensor.measure()          # takes a reading
        t = sensor.temperature()  # degrees C
        h = sensor.humidity()     # % relative humidity
        print("Temperature: {} C  Humidity: {} %".format(t, h))
    except OSError:
        print("No answer from the sensor: check the wiring")
    sleep(2)                      # DHT11 can only read once a second or so
