from machine import Pin, PWM


class Servo:
    """SG90 hobby servo.

    A servo reads a pulse 50 times a second (every 20 ms). The pulse
    length sets the angle: about 0.5 ms = 0 degrees, 2.4 ms = 180 degrees.
    If your servo buzzes at the ends or doesn't reach them, adjust
    min_us and max_us.
    """

    def __init__(self, pin=13, min_us=500, max_us=2400, max_angle=180):
        self.pwm = PWM(Pin(pin), freq=50, duty_ns=0)
        self.min_us = min_us
        self.max_us = max_us
        self.max_angle = max_angle
        self.current = None

    def pulse_us(self, us):
        """Send a raw pulse length in microseconds."""
        self.pwm.duty_ns(int(us * 1000))

    def angle(self, degrees=None):
        """Move to an angle (0 to 180). With no argument, return the last angle."""
        if degrees is None:
            return self.current
        degrees = max(0, min(self.max_angle, degrees))
        span = self.max_us - self.min_us
        self.pulse_us(self.min_us + span * degrees / self.max_angle)
        self.current = degrees

    def off(self):
        """Stop sending pulses so the servo goes limp and quiet."""
        self.pwm.duty_ns(0)

    def deinit(self):
        self.pwm.deinit()
