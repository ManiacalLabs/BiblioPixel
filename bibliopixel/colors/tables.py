"""
Tables of named colors
"""

import itertools, re
from . import juce, classic


def canonical_name(name):
    return name.replace(' ', '').lower()


def to_triplet(color):
    rg, b = color // 256, color % 256
    r, g = rg // 256, rg % 256
    return r, g, b


def set_user_colors(colors):
    from . import names

    _TO_NAME_USER.clear()
    _TO_COLOR_USER.clear()

    for name, color in colors.items():
        color = names.to_color(color)
        _TO_NAME_USER[color] = name
        _TO_COLOR_USER[canonical_name(name)] = color


def get_color(name):
    name = canonical_name(name)
    return _TO_COLOR_USER.get(name) or _TO_COLOR.get(name)


def get_name(color):
    return _TO_NAME_USER.get(color) or _TO_NAME.get(color)


def all_named_colors():
    """Return an iteration over all name, color pairs in tables"""
    yield from _TO_COLOR_USER.items()
    for name, color in _TO_COLOR.items():
        if name not in _TO_COLOR_USER:
            yield name, color


def contains(x):
    """Return true if this string or integer tuple appears in tables"""
    if isinstance(x, str):
        x = canonical_name(x)
        return x in _TO_COLOR_USER or x in _TO_COLOR
    else:
        x = tuple(x)
        return x in _TO_NAME_USER or x in _TO_NAME


def _classic_pairs():
    find = re.compile(r'[A-Z][a-z0-9]+').finditer

    for name in dir(classic):
        if name == 'Green_HTML':
            yield 'green html', classic.Green_HTML

        elif len(name) > 1 and name[0].isupper() and name[1].islower():
            key = ' '.join(i.group(0).lower() for i in find(name))
            yield key, getattr(classic, name)


_JUCE_COLORS = {k: to_triplet(v) for k, v in juce.COLORS.items()}
_CLASSIC_COLORS = dict(_classic_pairs())

"""
A dictionary of every color by name.
"""

COLOR_DICT = dict(_CLASSIC_COLORS, **_JUCE_COLORS)
CANONICAL_DICT = {canonical_name(k): v for k, v in COLOR_DICT.items()}

_SECONDARY_NAMES = juce.SECONDARY_NAMES.union({'off', 'on'})
_TO_NAME = {v: k for k, v in COLOR_DICT.items() if k not in _SECONDARY_NAMES}
_TO_COLOR = {canonical_name(k): v for k, v in COLOR_DICT.items()}
_TO_NAME_USER = {}
_TO_COLOR_USER = {}
