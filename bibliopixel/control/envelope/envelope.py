import math, random
from ... project import importer
from . import segments as _segments

ENVELOPE_PATH = 'bibliopixel.control.envelope.functions'


class Envelope:
    def __init__(self, enabled=True, base_value=0, period=None, phase=0,
                 offset=0, scale=1, loops=0, symmetry=0.5, reverse=False,
                 serpentine=False, power=1, frequency=None, duty_cycle=0.5):
        self.enabled = enabled
        self.base_value = base_value
        self.phase = phase
        self.offset = offset
        self.scale = scale
        self.loops = loops
        self.symmetry = symmetry
        self.duty_cycle = duty_cycle
        self.reverse = reverse
        self.serpentine = serpentine
        self.power = power
        if period:
            self.period = period
        elif frequency:
            self.frequency = frequency
        else:
            self.period = 1

    @property
    def frequency(self):
        return 1 / self.period

    @frequency.setter
    def frequency(self, f):
        self.period = 1 / f

    def _call(self, x):
        raise NotImplementedError

    def __call__(self, delta_time):
        if self.enabled:
            loop = delta_time / self.period
            if not (self.loops and loop >= self.loops):
                x = ((delta_time + self.phase) / self.period) % 1
                if self.reverse:
                    x = 1 - x
                if self.serpentine and loop % 2:
                    x = 1 - x
                if self.power != 1:
                    x = x ** self.power
                x = _apply_skew(x, 1 - self.duty_cycle)
                x = self._call(x)
                x = _apply_skew(x, self.symmetry)
                return x * self.scale + self.offset

        return self.base_value


class Linear(Envelope):
    def _call(self, x):
        return x


class Sine(Envelope):
    def _call(self, x):
        return math.sin(x * 2 * math.pi)


class Triangular(Envelope):
    def _call(self, x):
        return 2 * x if x < 0.5 else 2 - 2 * x


class Square(Envelope):
    def _call(self, x):
        return 0 if x < 0.5 else 1


class Random(Envelope):
    def _call(self, x):
        return random.random()


class Gaussian(Envelope):
    def __init__(self, mean=0.5, stdev=0.25, **kwds):
        super().__init__(**kwds)
        self.stdev = stdev
        self.mean = mean

    def _call(self, x):
        return random.gauss(self.mean, self.stdev)


class Segments(Envelope):
    def __init__(self, segments=(), period=None, **kwds):
        """
        If period is None, then it is set to be the length of the
        segments.

        Each segment is either a single number, indicating a level, or a pair of
        numbers, indicating a level and a time.  Levels without a time are
        assigned the average delay.
        """
        self.segments = _segments.Segments(segments)
        period = period or self.segments.total_time
        super().__init__(period=period, **kwds)

    def _call(self, x):
        return self.segments(x * self.segments.total_time, self.base_value)


def _apply_skew(x, skew):
    if x == skew:
        return 0.5
    elif x < skew:
        return 0.5 * x / skew
    else:
        return 0.5 + 0.5 * (x - skew) / (1 - skew)
