"""
Convert back and forth between colors and string names.
"""

import numbers, re
from . import juce, classic


def name_to_color(name):
    """
    :param str name: a string identifying a color.  It might be a color name
                     from the two lists of color names, juce and classic; or
                     it might be a list of numeric r, g, b values separated by
                     commas.
    :returns: a color as an RGB 3-tuple
    """
    def to_color(name):
        name = name.lower()
        if ',' in name:
            if name.startswith('(') and name.endswith(')'):
                name = name[1:-1]

            r, g, b = name.split(',')
            return _from_number(r), _from_number(g), _from_number(b)

        try:
            n = _from_number(name)
        except:
            return TO_COLOR[name.replace(' ', '').lower()]

        return _to_triplet(n)

    try:
        color = to_color(name)
    except:
        raise ValueError('Unknown color name %s' % str(name))

    if not all(0 <= i <= 255 for i in color):
        raise ValueError('Component out of range: %s' % color)

    return color


def color_to_name(color, use_hex=False):
    """
    :param tuple color: an RGB 3-tuple of integer colors
    :returns: a string name for this color

    ``name_to_color(color_to_name(c)) == c`` is guaranteed to be true (but the
    reverse is not true, because name_to_color is a many-to-one function).
    """
    if isinstance(color, list):
        color = tuple(color)
    elif not isinstance(color, tuple):
        raise ValueError('Not a color')

    if use_hex:
        return '#%02x%02x%02x' % color

    try:
        return TO_NAME[color]
    except:
        return str(color)


def toggle(s):
    """
    Toggle back and forth between a name and a tuple representation.

    :param str s: a string which is either a text name, or a tuple-string:
                  a string with three numbers separated by commas

    :returns: if the string was a text name, return a tuple.  If it's a
              tuple-string and it corresponds to a text name, return the text
              name, else return the original tuple-string.
    """
    is_numeric = ',' in s or s.startswith('0x') or s.startswith('#')
    c = name_to_color(s)
    return color_to_name(c) if is_numeric else str(c)


class _Colors(object):
    def __getitem__(self, name):
        try:
            return name_to_color(name)
        except:
            raise KeyError(name)

    def __getattr__(self, name):
        try:
            return name_to_color(name)
        except:
            raise AttributeError("COLORS has no attribute' %s'" % name)

    def __call__(self, color):
        return color_to_name(color)


def _to_triplet(color):
    rg, b = color // 256, color % 256
    r, g = rg // 256, rg % 256
    return r, g, b


def _classic_pairs():
    find = re.compile(r'[A-Z][a-z0-9]+').finditer

    for name in dir(classic):
        if name == 'Green_HTML':
            yield 'green html', classic.Green_HTML

        elif len(name) > 1 and name[0].isupper() and name[1].islower():
            key = ' '.join(i.group(0).lower() for i in find(name))
            yield key, getattr(classic, name)


def _from_number(s):
    s = s.strip()
    for prefix in '0x', '#':
        if s.startswith(prefix):
            return int(s[len(prefix):], 16)

    return int(s)


def to_color(c):
    """Try to coerce the argument into a color - a 3-tuple of numbers-"""
    if isinstance(c, numbers.Number):
        return c, c, c

    if not c:
        raise ValueError('Cannot create color from empty "%s"' % c)

    if isinstance(c, str):
        return name_to_color(c)

    if isinstance(c, list):
        c = tuple(c)

    if isinstance(c, tuple):
        if len(c) > 3:
            return c[:3]
        while len(c) < 3:
            c += (c[-1],)
        return c

    raise ValueError('Cannot create color from "%s"' % c)


"""
COLOR is a "magic" color name variable.

 To get a color from a name, use ``COLORS.<colorname>`` - for example

::

    COLORS.red
    COLORS.ochre

or if the name is a variable or has a space in it,

::

    COLORS['violet red 4']

To get a name from a color, use

::

    COLOR((0, 255, 255))
"""
COLORS = _Colors()


_JUCE_COLORS = {k: _to_triplet(v) for k, v in juce.COLORS.items()}
_CLASSIC_COLORS = dict(_classic_pairs())

"""
A dictionary of every color by name.
"""

COLOR_DICT = dict(_CLASSIC_COLORS, **_JUCE_COLORS)

# TODO: integrate this better with COLOR
_SECONDARY_NAMES = juce.SECONDARY_NAMES.union({'off', 'on'})
TO_NAME = {v: k for k, v in COLOR_DICT.items() if k not in _SECONDARY_NAMES}
TO_COLOR = {k.replace(' ', ''): v for k, v in COLOR_DICT.items()}
