import functools, numbers
from . names import COLORS
from . import palette

# This global variable is changed by the Project to allow color settings
# in Animations and other classes to use palette names.  TODO: figure out
# a way to avoid doing this.
PALETTES = {}


@functools.singledispatch
def color(c):
    raise ValueError('Don\'t understand color name "%s"' % c, _COLOR_USAGE)


@color.register(tuple)
def _(c):
    if len(c) != 3:
        raise ValueError('Length %d is not 3' % len(c), _COLOR_USAGE)

    if not all(0 <= x <= 255 for x in c):
        raise ValueError('All components must be between 0 and 255', _COLOR_USAGE)

    return c


@color.register(list)
def _(c):
    return color(tuple(c))


@color.register(numbers.Number)
def _(c):
    if not (0 <= c <= 255):
        raise ValueError('All components must be between 0 and 255', _COLOR_USAGE)
    return (c, c, c)


@color.register(str)
def _(c):
    try:
        return COLORS[c]
    except:
        raise ValueError('Don\'t understand color name "%s"' % c, _COLOR_USAGE)


@functools.singledispatch
def colors(c):
    raise ValueError("Don't understand type %s" % type(c), _COLORS_USAGE)


@colors.register(tuple)
@colors.register(list)
def _(c):
    return _colors(c)


@colors.register(str)
def _(s):
    return PALETTES.get(s) or _colors(s.split(','))


@colors.register(dict)
def _(d):
    return _colors(**d)


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


def _colors(colors=(), **kwds):
    colors = (color(c) for c in to_triplets(colors))
    return palette.Palette(colors, **kwds)


_COLOR_USAGE = """
A Color can be initialized with:

* A list of three numbers: [0, 0, 0] or [255, 0, 255].
* A single number which represents a brightness/gray level: 0, 255, 127
* A string:  "red", "yellow", "gold" naming a color from ...colors.COLORS.

All numbers must be in the range [0, 256) - 0 <= x < 256"""

_COLORS_USAGE = """
Colors is a list of colors.  Each color can be:

* A list of three numbers: [0, 0, 0] or [255, 0, 255].
* A single number which represents a brightness/gray level: 0, 255, 127
* A string:  "red", "yellow", "gold" naming a color from ...colors.COLORS.

All numbers must be in the range [0, 256) - 0 <= x < 256"""
