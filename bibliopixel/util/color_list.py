import copy

try:
    import numpy
    numpy_array = numpy.ndarray

except:
    numpy = None
    numpy_array = ()


class Base:
    def __init__(self, color_list):
        self.color_list = color_list

    def __len__(self):
        return len(self.color_list)

    def __getitem__(self, i):
        return self.color_list[i]


class List(Base):
    def clear(self):
        if self.color_list:
            black = tuple(0 for i in self[0])
            self.color_list[:] = (black for i in self.color_list)

    def add(self, source, level):
        def add(colors):
            return tuple(int(c + level * s) for (c, s) in zip(*colors))

        if level:
            self.color_list[:] = map(add, zip(self.color_list, source))

    def copy_from(self, source):
        self.color_list[:] = source


class Numpy(Base):
    _buffer = None

    def clear(self):
        self.color_list.fill(0)

    def add(self, source, level):
        if level:
            self._buffer = numpy.multiply(
                level, source, out=self._buffer, casting='unsafe')
            print(self._buffer)
            self.color_list += self._buffer

    def copy_from(self, source):
        numpy.copyto(self.color_list, source, casting='unsafe')


def ColorList(color_list):
    maker = Numpy if isinstance(color_list, numpy_array) else List
    return maker(color_list)


class Mixer:
    def __init__(self, color_list, sources, levels=None):
        self.color_list = ColorList(color_list)
        self.sources = sources

        cl = len(self.sources)
        padded_levels = (levels or []) + [0] * cl
        self.levels = padded_levels[:cl]
        self.clear = self.color_list.clear

    def mix(self):
        for source, level in zip(self.sources, self.levels):
            self.color_list.add(source, level)
