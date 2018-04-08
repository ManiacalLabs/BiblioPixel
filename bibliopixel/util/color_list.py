import copy

try:
    import numpy

    def is_numpy(x):
        return isinstance(x, numpy.ndarray)

except:
    numpy = None

    def is_numpy(x):
        return False


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


def Math(is_numpy):
    return NumpyMath if is_numpy else ListMath


class Mixer:
    def __init__(self, color_list, sources, levels=None):
        self.color_list = color_list
        self.math = Math(is_numpy(color_list))
        self.sources = sources
        self.levels = list(levels or [])
        needed = len(self.sources) - len(self.levels)
        if needed > 0:
            self.levels.extend(0 for i in range(needed))
        self.buffer = None

    def clear(self):
        self.math.clear(self.color_list)

    def mix(self, master=1):
        for source, level in zip(self.sources, self.levels):
            self.buffer = self.math.add(
                self.color_list, source, level * master, self.buffer)
