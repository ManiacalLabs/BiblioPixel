"""
To get a color from a name, use

    COLORS.colorname

or if the name is a variable or has a space in it,

    COLORS['color name']

To get a name from a color, use

    COLOR((0, 255, 255))
"""

import re
from . import juce, classic


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


JUCE_COLORS = {k: _to_triplet(v) for k, v in juce.COLORS.items()}
CLASSIC_COLORS = dict(_classic_pairs())
COLOR_DICT = dict(CLASSIC_COLORS, **JUCE_COLORS)

SECONDARY_NAMES = juce.SECONDARY_NAMES.union({'off', 'on'})
TO_NAME = {v: k for k, v in COLOR_DICT.items() if k not in SECONDARY_NAMES}
TO_COLOR = {k.replace(' ', ''): v for k, v in COLOR_DICT.items()}


def name_to_color(name):
    def to_int(s):
        s = s.strip()
        try:
            if s.startswith('0x'):
                return int(s[2:], 16)
            return int(s)
        except:
            raise ValueError("Don't understand number " + s)

    name = name.lower()
    if ',' in name:
        if name.startswith('(') and name.endswith(')'):
            name = name[1:-1]

        parts = name.split(',')
        if len(parts) != 3:
            raise ValueError('Colors must have three components')

        color = tuple(to_int(p) for p in parts)

    elif name.startswith('0x'):
        color = _to_triplet(int(name, 16))

    else:
        try:
            color = TO_COLOR[name.replace(' ', '').lower()]
        except:
            raise ValueError('Unknown color name %s' % name)

    if not all(0 <= i <= 255 for i in color):
        raise ValueError('Component out of range: %s' % color)

    return color


def color_to_name(color):
    try:
        return TO_NAME[tuple(color)]
    except:
        return str(tuple(color))


def toggle(s):
    """Toggle between a name and a tuple representation."""
    c = name_to_color(s)
    return color_to_name(c) if ',' in s else str(c)


class Colors(object):
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


COLORS = Colors()
