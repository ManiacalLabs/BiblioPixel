import copy, numpy
from . limit import Limit


def is_numpy(x):
    return isinstance(x, numpy.ndarray)


class ListMath:
    @staticmethod
    def clear(color_list):
        if color_list:
            black = tuple(0 for i in color_list[0])
            color_list[:] = (black for i in color_list)

    @staticmethod
    def add(color_list, source, level=1, buffer=None):
        def add(color, src):
            return tuple(int(c + level * s) for (c, s) in zip(color, src))

        if level:
            color_list[:] = (add(c, s) for (c, s) in zip(color_list, source))

        return buffer

    @staticmethod
    def copy(color_list, source):
        color_list[:] = source

    @staticmethod
    def scale(color_list, gain):
        color_list[:] = [tuple(gain * i for i in c) for c in color_list]

    @staticmethod
    def sum(color_list):
        return sum(sum(c) for c in color_list)


class NumpyMath:
    @staticmethod
    def clear(color_list):
        color_list.fill(0)

    @staticmethod
    def add(color_list, source, level=1, buffer=None):
        if level:
            buffer = numpy.multiply(source, level, out=buffer, casting='unsafe')
            color_list += buffer
        return buffer

    @staticmethod
    def copy(color_list, source):
        numpy.copyto(color_list, source, casting='unsafe')

    @staticmethod
    def scale(color_list, gain):
        color_list *= gain

    @staticmethod
    def sum(color_list):
        return sum(sum(c) for c in color_list)


def Math(color_list):
    return NumpyMath if is_numpy(color_list) else ListMath


class Mixer:
    def __init__(self, color_list, sources, levels=None):
        self.color_list = color_list
        self.math = Math(color_list)
        self.sources = sources
        self.levels = list(levels or [])
        needed = len(self.sources) - len(self.levels)
        self.levels.extend(0 for i in range(needed))
        self.buffer = None

    def clear(self):
        self.math.clear(self.color_list)

    def mix(self, master=1):
        for source, level in zip(self.sources, self.levels):
            self.buffer = self.math.add(
                self.color_list, source, level * master, self.buffer)


def to_triplets(colors):
    """
    Coerce a list into a list of triplets.

    If `colors` is a list of lists or strings, return it as is.  Otherwise,
    divide it into tuplets of length three, silently discarding any extra
    elements beyond a multiple of three.
    """
    try:
        colors[0][0]
        return colors
    except:
        pass

    # It's a 1-dimensional list
    extra = len(colors) % 3
    if extra:
        colors = colors[:-extra]
    return list(zip(*[iter(colors)] * 3))
