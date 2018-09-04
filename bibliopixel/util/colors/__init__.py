"""Functions to convert HSV colors to RGB colors lovingly ported from FastLED

The basically fall into two groups: spectra, and rainbows.

Spectra and rainbows are not the same thing.  Wikipedia has a good
illustration here

 http://upload.wikimedia.org/wikipedia/commons/f/f6/Prism_compare_rainbow_01.png

from this article

  http://en.wikipedia.org/wiki/Rainbow#Number_of_colours_in_spectrum_or_rainbow

that shows a 'spectrum' and a 'rainbow' side by side.  Among other
differences, you'll see that a 'rainbow' has much more yellow than
a plain spectrum.  "Classic" LED color washes are spectrum based, and
usually show very little yellow.

Wikipedia's page on HSV color space, with pseudocode for conversion
to RGB color space

  http://en.wikipedia.org/wiki/HSL_and_HSV

Note that their conversion algorithm, which is (naturally) very popular
is in the "maximum brightness at any given hue" style, vs the "uniform
brightness for all hues" style.

You can't have both; either purple is the same brightness as red, e.g

  red = #FF0000 and purple = #800080 -> same "total light" output

OR purple is 'as bright as it can be', e.g.

  red = #FF0000 and purple = #FF00FF -> purple is much brighter than red.

The colorspace conversions here try to keep the apparent brightness
constant even as the hue varies.

Adafruit's "Wheel" function, discussed here

  http://forums.adafruit.com/viewtopic.php?f=47&t=22483

is also of the "constant apparent brightness" variety.

More details here: https://github.com/FastLED/FastLED/wiki/FastLED-HSV-Colors
"""

from . arithmetic import color_blend, color_scale
from . conversions import hsv2rgb_spectrum, hsv2rgb_rainbow, hsv2rgb_360
from . conversions import hsv2rgb, hue2rgb, hue_gradient, hue2rgb_360
from . conversions import hue_helper, hue_helper360
from . wheel import wheel_color, wheel_helper
from . names import (
    COLORS, COLOR_DICT, color_to_name, name_to_color, to_color, toggle)

from .. import deprecated

if deprecated.allowed():  # pragma: no cover
    hex2rgb = COLORS.__getitem__
    from . import conversions as hue

    # Legacy color names
    from . classic import *  # noqa: F403
