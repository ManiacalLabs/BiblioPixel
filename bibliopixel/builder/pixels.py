import itertools, weakref
from .. colors import make
from .. util import color_list, log


class Pixels:
    """
    Wrap pixels attached to a layout for easy access and
    better error reporting.
    """
    def __init__(self, builder):
        self.builder = weakref.ref(builder)

    def __getitem__(self, index):
        """
        Returns the r, g, b pixel at a location in the layout.  May only be
        called if self.is_running is true.
        """
        index = self._check_index(index)
        return self.layout.get(*index)

    def __setitem__(self, index, color):
        """
        Sets the r, g, b pixel at a location in the layout.  May only be called
        if self.is_running is true.
        """
        index = self._check_index(index)
        try:
            color = make.color(color)
        except:
            log.error('Do not understand color %s', color)
            raise
        index.append(color)
        return self.layout.set(*index)

    def clear(self):
        cl = self.layout.color_list
        color_list.Math(cl).clear(cl)

    @property
    def layout(self):
        b = self.builder()

        if not (b and b.project):
            raise ValueError('Cannot get layout before Builder has started')
        return b.project.layout

    @property
    def shape(self):
        return self.layout.shape

    def _check_index(self, index):
        if isinstance(index, int):
            index = [index]
        else:
            index = list(index)

        l1, l2 = len(self.shape), len(index)
        if l1 != l2:
            msg = 'Expected %d coordinates but got %d: %s'
            raise ValueError(msg % (l1, l2, index))

        for i, s in enumerate(self.shape):
            if index[i] < 0:
                index[i] += s
            if not (0 <= index[i] < s):
                raise IndexError('Index %d was out of range' % i)

        return index
