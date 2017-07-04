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
    if name.startswith('(') and name.endswith(')'):
        name = name[1:-1]

    try:
        color = tuple(int(i) for i in name.split(','))
    except:
        pass
    else:
        if len(color) == 3:
            return color

        if len(color) == 1:
            return color[0], color[0], color[0]

        raise ValueError('Colors must have three components')

    try:
        return TO_COLOR[name.replace(' ', '').lower()]
    except:
        raise ValueError('Unknown color name')


def color_to_name(color):
    try:
        return TO_NAME[tuple(color)]
    except:
        return str(tuple(color))


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
