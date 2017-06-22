from . import strip


class Segment(strip.Strip):
    """Represents an offset, length segment within a strip."""

    def __init__(self, strip, length, offset=0):
        if offset < 0 or length < 0:
            raise ValueError('Segment indices are non-negative.')

        if offset + length > len(strip):
            raise ValueError('Segment too long.')

        self.strip = strip
        self.offset = offset
        self.length = length

    def __getitem__(self, index):
        return self.strip[self._fix_index(index)]

    def __setitem__(self, index, value):
        self.strip[self._fix_index(index)] = value

    def __len__(self):
        return self.length

    def next(self, length):
        """Return a new segment starting right after self in the same buffer."""
        return Segment(self.strip, length, self.offset + self.length)

    def _fix_index(self, index):
        if isinstance(index, slice):
            raise ValueError('Slicing segments not implemented.')
        if index < 0:
            index += self.length
        if index >= 0 and index < self.length:
            return self.offset + index
        raise IndexError('Index out of range')


def make_segments(strip, length):
    """Return a list of Segments that evenly split the strip."""
    if len(strip) % length:
        raise ValueError('The length of strip must be a multiple of length')

    s = []
    try:
        while True:
            s.append(s[-1].next(length) if s else Segment(strip, length))
    except ValueError:
        return s
