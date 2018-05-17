"""
Handle DMX and MIDI channel offsets
"""


class OffsetRange:
    def __init__(self, offset=0, begin=None, end=None):
        """
        Unlike a `range`, an OffsetRange includes both its begin *and* its end,
        so it's closer to how regular people think of a range - for example
        that DMX channels are in the range 1-512.
        """

        self.begin = self.BEGIN if begin is None else begin
        self.end = self.END if end is None else end

        if not (self.BEGIN <= self.begin <= self.end <= self.END):
            raise ValueError('Bad range: FAILED %s <= %s <=  %s <= %s' %
                             (self.BEGIN, self.begin, self.end, self.END))

        self.offset = offset

    def full_range(self):
        return self.END - self.BEGIN + 1

    def index(self, i, length=None):
        """Return an integer index or None"""
        if self.begin <= i <= self.end:
            index = i - self.BEGIN - self.offset
            if length is None:
                length = self.full_range()
            else:
                length = min(length, self.full_range())

            if 0 <= index < length:
                return index

    def read_from(self, data, pad=0):
        """
        Returns a generator with the elements "data" taken by offset, restricted
        by self.begin and self.end, and padded on either end by `pad` to get
        back to the original length of `data`
        """
        for i in range(self.BEGIN, self.END + 1):
            index = self.index(i, len(data))
            yield pad if index is None else data[index]

    def copy_to(self, source, target):
        if not target:
            return

        offset = self.offset
        if offset < 0:
            source = source[-offset:]
            offset = 0

        begin = min(self.begin - self.BEGIN, len(target) - 1)
        end = min(self.end - self.BEGIN, len(target) - 1)
        length = min(len(source) - offset, end - begin + 1)

        target[begin:begin + length] = source[offset:offset + length]

    @classmethod
    def make(cls, x=0):
        try:
            return cls(**x)
        except TypeError:
            return cls(offset=x)


class MidiChannel(OffsetRange):
    BEGIN = 1
    END = 16


class MidiNote(OffsetRange):
    BEGIN = 0
    END = 127


class DMXChannel(OffsetRange):
    BEGIN = 1
    END = 512
