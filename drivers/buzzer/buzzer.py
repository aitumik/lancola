from machine import Pin, PWM
from time import sleep_ms

# Semitones above C in the same octave
_STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def note_freq(note):
    """Frequency in Hz for a note name such as "A4", "C#5" or "Bb3".

    Returns 0 for a rest ("R" or "-"). A4 is 440 Hz; each octave doubles.
    """
    note = note.strip()
    if note in ("R", "-", ""):
        return 0
    step = _STEPS[note[0].upper()]
    rest = note[1:]
    if rest[:1] == "#":
        step += 1
        rest = rest[1:]
    elif rest[:1] == "b":
        step -= 1
        rest = rest[1:]
    octave = int(rest) if rest else 4
    midi = 12 * (octave + 1) + step   # MIDI note number, A4 = 69
    return int(440 * 2 ** ((midi - 69) / 12) + 0.5)


class Buzzer:
    """Passive buzzer. It only makes sound when we switch it on and off
    quickly; the switching speed (frequency) sets the pitch.

    (The active buzzer has its own oscillator: just use Pin.on()/off().)
    """

    def __init__(self, pin=27, volume=50):
        self.pwm = PWM(Pin(pin), freq=1000, duty_u16=0)
        self.volume = volume  # 0-100, really the duty cycle; 50 is loudest

    def tone(self, freq, ms=None):
        """Play freq Hz. With ms, play for that long then stop."""
        if freq <= 0:
            self.off()
        else:
            self.pwm.freq(int(freq))
            self.pwm.duty_u16(int(65535 * min(50, self.volume) / 100))
        if ms is not None:
            sleep_ms(ms)
            self.off()

    def note(self, name, ms=None):
        """Play a note by name, for example buzzer.note("C5", 300)."""
        self.tone(note_freq(name), ms)

    def beep(self, ms=100, freq=2000):
        self.tone(freq, ms)

    def off(self):
        self.pwm.duty_u16(0)

    def play(self, song, tempo=120):
        """Play a melody.

        song is a string of "note:beats" separated by spaces, for example
            "C4:1 D4:1 E4:2 R:1"
        or a list of (note, beats) pairs. Beats can be fractions (0.5).
        tempo is beats per minute.
        """
        if isinstance(song, str):
            song = [part.split(":") if ":" in part else (part, 1)
                    for part in song.split()]
        beat_ms = 60000 / tempo
        for name, beats in song:
            length = int(float(beats) * beat_ms)
            self.note(name, int(length * 0.9))  # short gap between notes
            sleep_ms(length - int(length * 0.9))

    def deinit(self):
        self.off()
        self.pwm.deinit()
