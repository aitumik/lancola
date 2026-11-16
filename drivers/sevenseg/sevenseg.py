from time import sleep_ms, ticks_ms, ticks_diff
from machine import Pin, Timer

# Segment bits: bit 0 = a ... bit 6 = g, bit 7 = dp
#
#      aaa
#     f   b
#      ggg
#     e   c
#      ddd  dp

DP = 0x80

FONT = {
    "0": 0x3F, "1": 0x06, "2": 0x5B, "3": 0x4F, "4": 0x66,
    "5": 0x6D, "6": 0x7D, "7": 0x07, "8": 0x7F, "9": 0x6F,
    "A": 0x77, "B": 0x7C, "C": 0x39, "D": 0x5E, "E": 0x79,
    "F": 0x71, "G": 0x3D, "H": 0x76, "I": 0x30, "J": 0x1E,
    "L": 0x38, "N": 0x54, "O": 0x5C, "P": 0x73, "Q": 0x67,
    "R": 0x50, "S": 0x6D, "T": 0x78, "U": 0x3E, "Y": 0x6E,
    "-": 0x40, "_": 0x08, " ": 0x00, "=": 0x48, "'": 0x02,
}

# a, b, c, d, e, f, g, dp
SEGMENTS = (13, 14, 27, 26, 25, 33, 32, 23)


class SevenSeg:
    """Seven-segment LED display wired straight to GPIO pins.

    segments: 7 or 8 pins in order a, b, c, d, e, f, g, (dp).
    digits:   common pins for a multi-digit display, left to right.
              Leave empty for a single digit with its common pin tied
              to GND (common cathode) or 3.3V (common anode).
    common_anode: True if the shared pin goes to + instead of GND.
    """

    def __init__(self, segments=SEGMENTS, digits=(), common_anode=False):
        self.segs = [Pin(p, Pin.OUT) for p in segments]
        self.digs = [Pin(p, Pin.OUT) for p in digits]
        self.anode = common_anode
        self.buf = [0] * max(1, len(self.digs))
        self.all_off()

    def __len__(self):
        return len(self.buf)

    def all_off(self):
        off = 1 if self.anode else 0
        for s in self.segs:
            s.value(off)
        for d in self.digs:
            d.value(1 - off)

    def set_segments(self, bits):
        on = 0 if self.anode else 1
        for i, s in enumerate(self.segs):
            s.value(on if bits & (1 << i) else 1 - on)

    def select(self, idx):
        # Digit common pin is active low for common cathode, high for anode
        active = 1 if self.anode else 0
        for i, d in enumerate(self.digs):
            d.value(active if i == idx else 1 - active)

    @staticmethod
    def encode(ch):
        return FONT.get(str(ch).upper(), 0)

    def show(self, text, align="right"):
        """Put text in the buffer. A '.' lights the dot of the previous char."""
        cells = []
        for ch in str(text):
            if ch == "." and cells and not cells[-1] & DP:
                cells[-1] |= DP
            elif ch == ".":
                cells.append(DP)
            else:
                cells.append(self.encode(ch))

        n = len(self.buf)
        cells = cells[-n:] if align == "right" else cells[:n]
        pad = [0] * (n - len(cells))
        self.buf = pad + cells if align == "right" else cells + pad

        if not self.digs:
            self.set_segments(self.buf[0])

    def number(self, value, decimals=0):
        if decimals:
            self.show("{:.{}f}".format(value, decimals))
        else:
            self.show(str(int(value)))

    def clear(self):
        self.buf = [0] * len(self.buf)
        self.all_off()

    def refresh(self, ms_per_digit=2):
        """Scan all digits once. Call this in a loop for multi-digit displays."""
        if not self.digs:
            return
        for i, bits in enumerate(self.buf):
            self.all_off()
            self.set_segments(bits)
            self.select(i)
            sleep_ms(ms_per_digit)
        self.all_off()

    def hold(self, ms):
        """Keep the display lit for ms milliseconds (multiplexes if needed)."""
        if not self.digs:
            sleep_ms(ms)
            return
        start = ticks_ms()
        while ticks_diff(ticks_ms(), start) < ms:
            self.refresh()

    def start(self, timer=1, ms_per_digit=3):
        """Multiplex in the background with a hardware timer.

        After start(), show()/number() just change the buffer and the
        display stays lit while your code does other things (sleep,
        read sensors...). Each timer tick lights the next digit.
        """
        if not self.digs:
            return
        self._pos = 0
        self._timer = Timer(timer)
        self._timer.init(mode=Timer.PERIODIC, period=ms_per_digit,
                         callback=self._tick)

    def _tick(self, t):
        i = self._pos % len(self.buf)
        self.all_off()
        self.set_segments(self.buf[i])
        self.select(i)
        self._pos = i + 1

    def stop(self):
        """Stop background multiplexing and blank the display."""
        timer = getattr(self, "_timer", None)
        if timer:
            timer.deinit()
            self._timer = None
        self.all_off()
