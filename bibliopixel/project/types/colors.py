import functools
from . import color
from ... util import color_list

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
    return [color.make(i) for i in color_list.to_triplets(c)]


@make.register(str)
def _(s):
    return make([s])
