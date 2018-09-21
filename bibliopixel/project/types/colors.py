import functools
from . import color
from ... util import color_list
from ... util.colors import palette

USAGE = """
Colors is a list of colors.  Each color can be:

* A list of three numbers: [0, 0, 0] or [255, 0, 255].
* A single number which represents a brightness/gray level: 0, 255, 127
* A string:  "red", "yellow", "gold" naming a color from ...colors.COLORS.

All numbers must be in the range [0, 256) - 0 <= x < 256"""


@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(tuple)
@make.register(list)
def _(c):
    return _make(c)


@make.register(str)
def _(s):
    return _make(s.split(','))


@make.register(dict)
def _(d):
    return _make(**d)


def _make(colors=(), **kwds):
    colors = (color.make(i) for i in color_list.to_triplets(colors))
    return palette.Palette(colors, **kwds)
