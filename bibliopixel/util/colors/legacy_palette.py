from . import make, palettes
from . names import COLORS

LEGACY_FIELDS = (
    ('color',),
    ('color1', 'color2'),
    ('onColor', 'offColor'),
    ('colors',),
    ('palette',),
)


def pop_legacy_palette(kwds):
    """
    Older animations in BPA and other areas use all sorts of different names for
    what we are now representing with palettes.

    This function mutates a kwds dictionary to remove these legacy fields and
    extract a palette from it, which it returns.
    """

    cases = []
    for fields in LEGACY_FIELDS:
        if any(f in kwds for f in fields):
            cases.append(fields)

    if not cases:
        return palettes.get()

    if len(cases) > 1:
        raise ValueError('Cannot set all of ' + ', '.join(sum(cases, [])))

    first, *rest = cases[0]

    a = kwds.pop(first, COLORS.Red)
    if first == 'color':
        return make.colors((a,))

    if not rest:
        return a

    b = kwds.pop(rest[0], COLORS.Black)
    return make.colors((a, b))
