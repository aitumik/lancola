from machine import Pin, Timer
from time import ticks_us, ticks_diff
from array import array

# Key codes for the kit's 17-key remote (NEC protocol).
# If a key prints "unknown", run examples/ir_nec_demo.py, note its code
# and add it here.
KEYS = {
    0x46: "UP", 0x15: "DOWN", 0x44: "LEFT", 0x43: "RIGHT", 0x40: "OK",
    0x16: "1", 0x19: "2", 0x0D: "3",
    0x0C: "4", 0x18: "5", 0x5E: "6",
    0x08: "7", 0x1C: "8", 0x5A: "9",
    0x42: "*", 0x52: "0", 0x4A: "#",
}

REPEAT = -1  # code reported while a key is held down


class IR:
    """IR receiver for NEC remotes.

    The receiver output goes LOW while it sees infrared light. Every edge
    is timestamped by a pin interrupt; 80 ms after the first edge a timer
    decodes the whole message, so your own code never has to wait.

    A NEC message is:
      9 ms pulse, 4.5 ms gap, then 32 bits.
      Each bit is a 0.56 ms pulse followed by a gap:
        0.56 ms gap -> 0,  1.69 ms gap -> 1
      The 32 bits are: address, ~address, command, ~command.
    Holding a key sends a short "repeat" message instead: 9 ms pulse, 2.25 ms gap.
    """

    def __init__(self, pin=19, timer=0):
        self.pin = Pin(pin, Pin.IN)
        self.times = array("i", [0] * 70)
        self.edges = 0
        self.timer = Timer(timer)
        self.last = None        # last real command, used for repeats
        self.code = None        # newest code waiting to be read
        self.address = None
        self.callback = None
        self.pin.irq(handler=self._edge, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

    # ---- interrupt side: keep it tiny ----

    def _edge(self, pin):
        n = self.edges
        if n < 70:
            if n == 0:
                self.timer.init(mode=Timer.ONE_SHOT, period=80, callback=self._decode)
            self.times[n] = ticks_us()
            self.edges = n + 1

    def _width(self, i):
        return ticks_diff(self.times[i + 1], self.times[i])

    def _decode(self, timer):
        n = self.edges
        self.edges = 0
        if n < 4 or not 8000 < self._width(0) < 10000:
            return  # not a NEC start pulse: noise

        gap = self._width(1)
        if 1800 < gap < 2800:
            if self.last is None:
                return
            code = REPEAT
        elif 3800 < gap < 5200 and n >= 67:
            value = 0
            for bit in range(32):
                if self._width(3 + 2 * bit) > 1120:
                    value |= 1 << bit   # NEC sends the lowest bit first
            cmd = (value >> 16) & 0xFF
            if cmd ^ ((value >> 24) & 0xFF) != 0xFF:
                return  # checksum failed
            self.address = value & 0xFF
            self.last = cmd
            code = cmd
        else:
            return

        self.code = code
        if self.callback:
            self.callback(code)

    # ---- for students ----

    def read(self, repeat=False):
        """Newest key code, or None. Each press is returned once.

        repeat=True also returns the held key again while it is held down.
        """
        code = self.code
        self.code = None
        if code == REPEAT:
            return self.last if repeat else None
        return code

    def read_key(self, repeat=False):
        """Like read(), but returns the key name such as "OK" or "5"."""
        code = self.read(repeat)
        if code is None:
            return None
        return KEYS.get(code, "unknown 0x{:02X}".format(code))

    def on_press(self, func):
        """Call func(code) every time a message arrives (REPEAT while held)."""
        self.callback = func

    def stop(self):
        self.pin.irq(handler=None)
        self.timer.deinit()
