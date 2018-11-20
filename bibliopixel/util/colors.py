from . import deprecated
if deprecated.allowed():  # pragma: no cover
    from .. colors import *  # noqa: F403
    from .. colors import (
        arithmetic, classic, closest_colors, conversions, gamma, juce,
        legacy_palette, make, names, palettes, printer, wheel)
