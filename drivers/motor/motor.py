from machine import Pin, PWM


class Motor:
    """DC motor on a two-input driver board (the kit's motor driver,
    L9110S, HR8833, DRV8833 and similar). Also drives the fan.

      IN1   IN2    motor
      PWM   0      forward, speed set by PWM
      0     PWM    reverse
      0     0      coast (free spin)
      1     1      brake

    Speed is a percentage, 0 to 100. Small motors often don't start
    below about 30 %.
    """

    def __init__(self, in1=25, in2=26, freq=1000):
        self.a = PWM(Pin(in1), freq=freq, duty_u16=0)
        self.b = PWM(Pin(in2), freq=freq, duty_u16=0)
        self.speed = 0

    @staticmethod
    def _duty(percent):
        percent = max(0, min(100, percent))
        return int(percent * 65535 / 100)

    def forward(self, speed=100):
        self.b.duty_u16(0)
        self.a.duty_u16(self._duty(speed))
        self.speed = speed

    def reverse(self, speed=100):
        self.a.duty_u16(0)
        self.b.duty_u16(self._duty(speed))
        self.speed = -speed

    def run(self, speed):
        """One call for both ways: -100 (full reverse) to 100 (full forward)."""
        if speed >= 0:
            self.forward(speed)
        else:
            self.reverse(-speed)

    def stop(self):
        """Cut power and let the motor coast."""
        self.a.duty_u16(0)
        self.b.duty_u16(0)
        self.speed = 0

    def brake(self):
        """Short the motor so it stops quickly."""
        self.a.duty_u16(65535)
        self.b.duty_u16(65535)
        self.speed = 0

    def deinit(self):
        self.stop()
        self.a.deinit()
        self.b.deinit()
