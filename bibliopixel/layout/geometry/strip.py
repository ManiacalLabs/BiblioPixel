import abc


class Strip(abc.ABC):
    """Base class for contiguous strips.  You can also use a list as a Strip."""

    @abc.abstractmethod
    def __getitem__(self, index):
        """`index` must be an integer, not a slice."""
        pass

    @abc.abstractmethod
    def __setitem__(self, index, value):
        """`index` must be an integer, not a slice."""
        pass

    @abc.abstractmethod
    def __len__(self):
        pass


def fill(strip, item, start=0, stop=None, step=1):
    """Fill a portion of a strip from start to stop by step with a given item.
    If stop is not given, it defaults to the length of the strip.
    """
    if stop is None:
        stop = len(strip)

    for i in range(start, stop, step):
        strip[i] = item


def gen_strip(num):
    return [[x, 0, 0] for x in range(num)]
