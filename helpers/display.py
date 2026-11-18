"""Traffic light display helper for a 16x2 (1602) LCD.

Made for the LCD class in lcd.py. It uses these methods:
    lcd.clear()
    lcd.move_to(col, row)
    lcd.write(text)
    lcd.custom_char(location, rows)

Example:
    from lcd import LCD
    from display import TrafficDisplay
    display = TrafficDisplay(LCD())
    display.show("RED", 12)                 # text style
    display.show("RED", 12, total=20)       # with progress bar
    display.message("NIGHT MODE", "Flashing amber")
"""

COLS = 16

# state: (meaning, next state)
STATES = {
    "RED": ("STOP", "Green"),
    "AMBER": ("SLOW", "Red"),
    "YELLOW": ("SLOW", "Red"),
    "GREEN": ("GO", "Amber"),
}


class TrafficDisplay:
    def __init__(self, lcd, cols=COLS):
        self.lcd = lcd
        self.cols = cols
        self._lines = [None, None]   # what is on screen now, to avoid rewriting
        self._make_bar_chars()
        lcd.clear()

    # ---------- public ----------

    def show(self, state, remaining, total=None):
        """Show a light state and seconds remaining.

        Without total:          With total (progress bar):
          RED     STOP            RED   STOP   12s
          Green in:   12s         ##########......
        """
        state = state.upper()
        meaning, nxt = STATES.get(state, ("", "Next"))
        remaining = max(0, int(remaining))

        if total:
            top = "{:<6}{:<6}{:>3}s".format(state, meaning, remaining)
            bottom = self._bar(remaining / total)
        else:
            top = "{:<8}{}".format(state, meaning)
            label = nxt + " in:"
            secs = "{:>3}s".format(remaining)
            bottom = label + " " * (self.cols - len(label) - len(secs) - 1) + secs

        self._write(0, top)
        self._write(1, bottom)

    def message(self, line1="", line2=""):
        """Show any two lines of text, e.g. NIGHT MODE or WAIT."""
        self._write(0, line1)
        self._write(1, line2)

    def redraw(self):
        """Call this if something else cleared or wrote to the LCD."""
        self._lines = [None, None]

    # ---------- internals ----------

    def _write(self, row, text):
        # Pad to the full width so old characters never get left behind,
        # and only touch the LCD when the line actually changed (no flicker).
        text = "{:<{w}}".format(text, w=self.cols)[: self.cols]
        if text != self._lines[row]:
            self.lcd.move_to(0, row)
            self.lcd.write(text)
            self._lines[row] = text

    def _make_bar_chars(self):
        # Custom characters 1-5: a block filled 1 to 5 pixels wide.
        # Each LCD character is 5 pixels wide and 8 rows tall.
        for width in range(1, 6):
            row = (0x1F << (5 - width)) & 0x1F
            self.lcd.custom_char(width, bytearray([row] * 8))

    def _bar(self, fraction):
        fraction = max(0.0, min(1.0, fraction))
        pixels = round(fraction * self.cols * 5)
        full, part = divmod(pixels, 5)
        bar = chr(5) * full
        if part:
            bar += chr(part)
        return bar
