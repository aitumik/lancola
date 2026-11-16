from machine import Pin
from time import sleep_ms, sleep_us, ticks_ms, ticks_diff

LAYOUT = (
    "123A",
    "456B",
    "789C",
    "*0#D",
)


class Keypad:
    """4x4 membrane keypad (works for 3x4 or other sizes too).

    Each key joins one row wire to one column wire. To find a pressed key
    we drive one row LOW at a time and look for a column that reads LOW
    (columns are pulled HIGH inside the ESP32).

    rows: 4 pins, top to bottom.  cols: 4 pins, left to right.
    Looking at the front, the ribbon's 8 wires are usually
    rows 1-4 then columns 1-4, left to right.
    Column pins need internal pull-ups, so don't use GPIO 34-39 for them.
    """

    def __init__(self, rows=(19, 18, 5, 17), cols=(16, 4, 33, 32),
                 layout=LAYOUT, debounce_ms=30):
        # Idle rows are inputs so two pressed keys can't short two outputs.
        self.rows = [Pin(p, Pin.IN) for p in rows]
        self.cols = [Pin(p, Pin.IN, Pin.PULL_UP) for p in cols]
        self.layout = layout
        self.debounce_ms = debounce_ms
        self.held = None         # key currently held down
        self.changed = ticks_ms()

    def scan(self):
        """The key pressed right now, or None. No debouncing."""
        for r, row in enumerate(self.rows):
            row.init(Pin.OUT, value=0)
            sleep_us(10)  # let the wire settle
            for c, col in enumerate(self.cols):
                if col.value() == 0:
                    row.init(Pin.IN)
                    return self.layout[r][c]
            row.init(Pin.IN)
        return None

    def get_key(self):
        """A key once when it is pressed, otherwise None. Never waits.

        Call this often in your loop. Holding a key returns it only once.
        """
        key = self.scan()
        now = ticks_ms()
        if key == self.held:
            return None
        if ticks_diff(now, self.changed) < self.debounce_ms:
            return None  # contacts still bouncing
        self.changed = now
        self.held = key
        return key       # None when the key was just released

    def wait_key(self, timeout_ms=None):
        """Wait for a key press and return it (None after timeout_ms)."""
        start = ticks_ms()
        while True:
            key = self.get_key()
            if key:
                return key
            if timeout_ms is not None and ticks_diff(ticks_ms(), start) > timeout_ms:
                return None
            sleep_ms(5)

    def read_text(self, end="#", clear="*", max_len=16, echo=None):
        """Collect keys into a string until `end` is pressed.

        `clear` deletes the last character. echo(text) is called after each
        key, for example to show the text on the LCD.
        """
        text = ""
        while True:
            key = self.wait_key()
            if key == end:
                return text
            if key == clear:
                text = text[:-1]
            elif len(text) < max_len:
                text += key
            if echo:
                echo(text)
