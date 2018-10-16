from . import make


def pop_legacy_palette(kwds, *color_defaults):
    """
    Older animations in BPA and other areas use all sorts of different names for
    what we are now representing with palettes.

    This function mutates a kwds dictionary to remove these legacy fields and
    extract a palette from it, which it returns.
 """
    palette = kwds.pop('palette', None)
    if palette:
        legacy = [k for k, _ in color_defaults if k in kwds]
        if legacy:
            raise ValueError('Cannot set palette and ' + ', '.join(legacy))
        return palette

    values = [kwds.pop(k, v) for k, v in color_defaults]
    if values and color_defaults[0][0] in ('colors', 'palette'):
        values = values[0]

    return make.colors(values or None)
