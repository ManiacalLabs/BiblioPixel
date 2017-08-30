import copy

try:
    import numpy
    numpy_array = numpy.ndarray

except:
    numpy = None
    numpy_array = ()


class ListMath:
    @staticmethod
    def clear(color_list):
        if color_list:
            black = tuple(0 for i in color_list[0])
            color_list[:] = (black for i in color_list)

    @staticmethod
    def add(color_list, source, level, buffer):
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
    def add(color_list, source, level, buffer):
        if level:
            buffer = numpy.multiply(source, level, out=buffer, casting='unsafe')
            color_list += buffer
        return buffer

    @staticmethod
    def copy(color_list, source):
        numpy.copyto(color_list, source, casting='unsafe')


def Math(color_list):
    return NumpyMath if isinstance(color_list, numpy_array) else ListMath


class ColorList:
    def __init__(self, color_list):
        self.color_list = color_list
        self.math = Math(color_list)
        self.buffer = None

    def clear(self):
        self.math.clear(self.color_list)

    def add(self, source, level):
        self.buffer = self.math.add(self.color_list, source, level, self.buffer)

    def copy_from(self, source):
        self.math.copy(self.color_list, source)

    def __len__(self):
        return len(self.color_list)

    def __getitem__(self, i):
        return self.color_list[i]


class Mixer:
    def __init__(self, color_list, sources, levels=None):
        self.color_list = ColorList(color_list)
        self.sources = sources
        self.levels = levels or []
        self.clear = self.color_list.clear

    def mix(self, master=1):
        for source, level in zip(self.sources, self.levels):
            self.color_list.add(source, level * master)
