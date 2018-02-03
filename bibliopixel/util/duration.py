"""
Convert a string duration to a number of seconds.
"""
import re

SI_PREFIXES = (
    (10 ** 24, 'yotta', 'Y'),
    (10 ** 21, 'zetta', 'Z'),
    (10 ** 18, 'exa', 'E'),
    (10 ** 15, 'peta', 'P'),
    (10 ** 12, 'tera', 'T'),
    (10 ** 9, 'giga', 'G'),
    (10 ** 6, 'mega', 'M'),
    (10 ** 3, 'kilo', 'k'),
    (10 ** 2, 'hecto', 'h'),
    (10 ** 1, 'deka', 'da'),
    (10 ** -1, 'deci', 'd'),
    (10 ** -2, 'centi', 'c'),
    (10 ** -3, 'milli', 'm'),
    (10 ** -6, 'micro', 'µ'),
    (10 ** -9, 'nano', 'n'),
    (10 ** -12, 'pico', 'p'),
    (10 ** -15, 'femto', 'f'),
    (10 ** -18, 'atto', 'a'),
    (10 ** -21, 'zepto', 'z'),
    (10 ** -24, 'yocto', 'y'),
)

SI_SCALES = dict(
    [(p[1], p[0]) for p in SI_PREFIXES] +
    [(p[2], p[0]) for p in SI_PREFIXES] +
    [['u', 10 ** -9]])  # Cheat to allow usec

UNITS = {
    'week': 7 * 24 * 60 * 60,
    'day': 24 * 60 * 60,

    'hour': 60 * 60,
    'hr': 60 * 60,

    'minute': 60,
    'min': 60,

    'second': 1,
    'sec': 1,
    's': 1,
}

PART_MATCH = re.compile(r'([0-9.]+)([a-zA-Z]+)').fullmatch


def _get_units(s):
    # Some subtleties to handle the possibility of plural units.
    if s.endswith('ss'):
        raise ValueError('Unknown unit')

    def split_unit(s):
        for u in UNITS:
            if s.endswith(u):
                return s[:-len(u)], u

    prefix, unit = (
        s.endswith('s') and split_unit(s[:-1]) or
        split_unit(s) or
        (s, ''))

    if not unit:
        raise ValueError('Unknown unit ' + s)

    scale = UNITS[unit]

    if not prefix:
        return scale

    if prefix not in SI_SCALES:
        raise ValueError('Unknown metric prefix ' + prefix)

    return SI_SCALES[prefix] * scale


def parse(s):
    """
    Parse a string representing a time interval or duration into seconds,
    or raise an exception

    :param str s: a string representation of a time interval
    :raises ValueError: if ``s`` can't be interpreted as a duration

    """

    parts = s.replace(',', ' ').split()
    if not parts:
        raise ValueError('Cannot parse empty string')

    pieces = []
    for part in parts:
        m = PART_MATCH(part)
        pieces.extend(m.groups() if m else [part])

    if len(pieces) == 1:
        pieces.append('s')

    if len(pieces) % 2:
        raise ValueError('Malformed duration %s: %s: %s' % (s, parts, pieces))

    result = 0
    for number, units in zip(*[iter(pieces)] * 2):
        number = float(number)
        if number < 0:
            raise ValueError('Durations cannot have negative components')
        result += number * _get_units(units)

    return result
