import functools, numbers
from ... util import colors

USAGE = """
A Color can be initialized with:

* A list of three numbers: [0, 0, 0] or [255, 0, 255].
* A single number which represents a brightness/gray level: 0, 255, 127
* A string:  "red", "yellow", "gold" naming a color from ...colors.COLORS.

All numbers must be in the range [0, 256) - 0 <= x < 256"""


@functools.singledispatch
def make(c):
    raise ValueError('Don\'t understand color name "%s"' % c, USAGE)


@make.register(tuple)
def _(c):
    if len(c) != 3:
        raise ValueError('Length %d is not 3' % len(c), USAGE)

    if not all(0 <= x <= 255 for x in c):
        raise ValueError('All components must be between 0 and 255', USAGE)

    return c


@make.register(list)
def _(c):
    return make(tuple(c))


@make.register(numbers.Number)
def _(c):
    if not (0 <= c <= 255):
        raise ValueError('All components must be between 0 and 255', USAGE)
    return (c, c, c)


@make.register(str)
def _(c):
    try:
        return colors.COLORS[c]
    except:
        raise ValueError('Don\'t understand color name "%s"' % c, USAGE)
