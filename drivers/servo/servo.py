from machine import Pin, PWM
import time


class Servo:
    """SG90 hobby servo.

    A servo reads a pulse 50 times a second (every 20 ms). The pulse
    length sets the angle: about 0.5 ms = 0 degrees, 2.4 ms = 180 degrees.
    If your servo buzzes at the ends or doesn't reach them, adjust
    min_us and max_us.
    """

    FREQ = 50                    # pulses per second
    PERIOD_US = 1000000 // FREQ  # 20000 us per cycle

    def __init__(self, pin=13, min_us=500, max_us=2400, max_angle=180):
        # Create the PWM with just the frequency first, then set the duty.
        # Passing duty_ns in the constructor raises "PWM is inactive" on
        # some ESP32 builds.
        self.pwm = PWM(Pin(pin), freq=self.FREQ)
        self.pwm.duty_u16(0)
        self.min_us = min_us
        self.max_us = max_us
        self.max_angle = max_angle
        self.current = None

    def pulse_us(self, us):
        """Send a raw pulse length in microseconds."""
        # duty_u16 works on every ESP32 build: 65535 = 100% of the 20 ms cycle.
        self.pwm.duty_u16(int(us * 65535 / self.PERIOD_US))

    def angle(self, degrees=None):
        """Move to an angle (0 to 180). With no argument, return the last angle."""
        if degrees is None:
            return self.current
        degrees = max(0, min(self.max_angle, degrees))
        span = self.max_us - self.min_us
        self.pulse_us(self.min_us + span * degrees / self.max_angle)
        self.current = degrees

    def move_to(self, degrees, speed=60):
        """Move gradually to an angle. speed is in degrees per second."""
        degrees = max(0, min(self.max_angle, degrees))
        if self.current is None:      # position unknown, so jump there first
            self.angle(degrees)
            return
        step = 1 if degrees > self.current else -1
        delay = 1 / speed             # seconds per 1-degree step
        for a in range(int(self.current), int(degrees), step):
            self.angle(a + step)
            time.sleep(delay)
        self.angle(degrees)

    def off(self):
        """Stop sending pulses so the servo goes limp and quiet."""
        self.pwm.duty_u16(0)

    def deinit(self):
        self.pwm.deinit()
