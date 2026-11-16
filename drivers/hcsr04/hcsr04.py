from machine import Pin, time_pulse_us
from time import sleep_us

SOUND_CM_PER_US = 0.0343  # speed of sound at about 20 C


class HCSR04:
    """HC-SR04 ultrasonic distance sensor.

    The sensor sends a burst of sound when TRIG gets a 10 us pulse.
    ECHO then stays HIGH for as long as the sound takes to go out and
    come back, so distance = time x speed of sound / 2.
    """

    def __init__(self, trig=18, echo=34, timeout_us=30000):
        # 30 ms timeout is about 5 m, past the sensor's range
        self.trig = Pin(trig, Pin.OUT, value=0)
        self.echo = Pin(echo, Pin.IN)
        self.timeout = timeout_us

    def pulse_us(self):
        """Echo time in microseconds, or a negative number if nothing came back."""
        self.trig.value(0)
        sleep_us(2)
        self.trig.value(1)
        sleep_us(10)
        self.trig.value(0)
        return time_pulse_us(self.echo, 1, self.timeout)

    def distance_cm(self):
        """Distance in cm, or None when nothing is in range."""
        t = self.pulse_us()
        if t < 0:
            return None
        return t * SOUND_CM_PER_US / 2

    def distance_mm(self):
        cm = self.distance_cm()
        return None if cm is None else int(cm * 10)
