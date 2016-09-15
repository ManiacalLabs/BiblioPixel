# Functions to convert HSV colors to RGB colors lovingly ported from FastLED
#
#  The basically fall into two groups: spectra, and rainbows.
#  Spectra and rainbows are not the same thing.  Wikipedia has a good
#  illustration here
#   http://upload.wikimedia.org//wikipedia//commons//f//f6//Prism_compare_rainbow_01.png
#  from this article
#   http://en.wikipedia.org//wiki//Rainbow#Number_of_colours_in_spectrum_or_rainbow
#  that shows a 'spectrum' and a 'rainbow' side by side.  Among other
#  differences, you'll see that a 'rainbow' has much more yellow than
#  a plain spectrum.  "Classic" LED color washes are spectrum based, and
#  usually show very little yellow.
#
#  Wikipedia's page on HSV color space, with pseudocode for conversion
#  to RGB color space
#   http://en.wikipedia.org//wiki//HSL_and_HSV
#  Note that their conversion algorithm, which is (naturally) very popular
#  is in the "maximum brightness at any given hue" style, vs the "uniform
#  brightness for all hues" style.
#
#  You can't have both; either purple is the same brightness as red, e.g
#    red = #FF0000 and purple = #800080 -> same "total light" output
#  OR purple is 'as bright as it can be', e.g.
#    red = #FF0000 and purple = #FF00FF -> purple is much brighter than red.
#  The colorspace conversions here try to keep the apparent brightness
#  constant even as the hue varies.
#
#  Adafruit's "Wheel" function, discussed here
#   http://forums.adafruit.com//viewtopic.php?f=47&t=22483
#  is also of the "constant apparent brightness" variety.
#
# More details here: https://github.com//FastLED//FastLED//wiki//FastLED-HSV-Colors

from __future__ import division
import colorsys
import types
import util


def color_scale(color, level):
    """Scale RGB tuple by level, 0 - 255"""
    return tuple([(i * level) >> 8 for i in list(color)])


def color_blend(a, b):
    """Performs a Screen blend on RGB color tuples, a and b"""
    return (255 - (((255 - a[0]) * (255 - b[0])) >> 8), 255 - (((255 - a[1]) * (255 - b[1])) >> 8), 255 - (((255 - a[2]) * (255 - b[2])) >> 8))


def gamma_correct(color, gamma):
    """Applies a gamma correction to an RGB color tuple"""
    return (gamma[color[0]], gamma[color[1]], gamma[color[2]])


def hsv2rgb_raw(hsv):
    """
    Converts an HSV tuple to RGB. Intended for internal use.
    You should use hsv2rgb_spectrum or hsv2rgb_rainbow instead.
    """

    HSV_SECTION_3 = 0x40

    h, s, v = hsv

    # The brightness floor is minimum number that all of
    # R, G, and B will be set to.
    invsat = 255 - s
    brightness_floor = (v * invsat) // 256

    # The color amplitude is the maximum amount of R, G, and B
    # that will be added on top of the brightness_floor to
    # create the specific hue desired.
    color_amplitude = v - brightness_floor

    # figure out which section of the hue wheel we're in,
    # and how far offset we are within that section
    section = h // HSV_SECTION_3  # 0..2
    offset = h % HSV_SECTION_3  # 0..63

    rampup = offset
    rampdown = (HSV_SECTION_3 - 1) - offset

    # compute color-amplitude-scaled-down versions of rampup and rampdown
    rampup_amp_adj = (rampup * color_amplitude) // (256 // 4)
    rampdown_amp_adj = (rampdown * color_amplitude) // (256 // 4)

    # add brightness_floor offset to everything
    rampup_adj_with_floor = rampup_amp_adj + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor

    r, g, b = (0, 0, 0)

    if section:
        if section == 1:
            # section 1: 0x40..0x7F
            r = brightness_floor
            g = rampdown_adj_with_floor
            b = rampup_adj_with_floor
        else:
            # section 2; 0x80..0xBF
            r = rampup_adj_with_floor
            g = brightness_floor
            b = rampdown_adj_with_floor
    else:
        # section 0: 0x00..0x3F
        r = rampdown_adj_with_floor
        g = rampup_adj_with_floor
        b = brightness_floor

    return (r, g, b)


def hsv2rgb_spectrum(hsv):
    """Generates RGB values from  HSV values in line with a typical light spectrum"""
    h, s, v = hsv
    return hsv2rgb_raw(((h * 192) >> 8, s, v))


def _nscale8x3_video(r, g, b, scale):
    """Internal Use Only"""
    nonzeroscale = 0
    if scale != 0:
        nonzeroscale = 1
    if r != 0:
        r = ((r * scale) >> 8) + nonzeroscale
    if g != 0:
        g = ((g * scale) >> 8) + nonzeroscale
    if b != 0:
        b = ((b * scale) >> 8) + nonzeroscale
    return (r, g, b)


def _scale8_video_LEAVING_R1_DIRTY(i, scale):
    """Internal Use Only"""
    nonzeroscale = 0
    if scale != 0:
        nonzeroscale = 1
    if i != 0:
        i = ((i * scale) >> 8) + nonzeroscale
    return i


def hsv2rgb_rainbow(hsv):
    """Generates RGB values from HSV that have an even visual distribution.
       Be careful as this method is only have as fast as hsv2rgb_spectrum.
    """

    h, s, v = hsv
    offset = h & 0x1F  # 0..31
    offset8 = offset * 8
    third = (offset8 * (256 // 3)) >> 8
    r, g, b = (0, 0, 0)

    if not (h & 0x80):
        if not (h & 0x40):
            if not (h & 0x20):
                r = 255 - third
                g = third
                b = 0
            else:
                r = 171
                g = 85 + third
                b = 0x00
        else:
            if not (h & 0x20):
                twothirds = (third << 1)
                r = 171 - twothirds
                g = 171 + third
                b = 0
            else:
                r = 0
                g = 255 - third
                b = third
    else:
        if not (h & 0x40):
            if not (h & 0x20):
                r = 0x00
                twothirds = (third << 1)
                g = 171 - twothirds
                b = 85 + twothirds
            else:
                r = third
                g = 0
                b = 255 - third
        else:
            if not (h & 0x20):
                r = 85 + third
                g = 0
                b = 171 - third
            else:
                r = 171 + third
                g = 0x00
                b = 85 - third

    if s != 255:
        r, g, b = _nscale8x3_video(r, g, b, s)
        desat = 255 - s
        desat = (desat * desat) >> 8
        brightness_floor = desat
        r = r + brightness_floor
        g = g + brightness_floor
        b = b + brightness_floor

    if v != 255:
        v = _scale8_video_LEAVING_R1_DIRTY(v, v)
        r, g, b = _nscale8x3_video(r, g, b, v)

    return (r, g, b)


def hsv2rgb_360(hsv):
    """
    Python default hsv to rgb conversion for when hue values 0-359 are preferred.
    Due to requiring float math, this method is slower than hsv2rgb_rainbow and hsv2rgb_spectrum.
    """

    h, s, v = hsv

    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return (int(r * 255.0), int(g * 255.0), int(b * 255.0))


# pre-generated spectrums for the sake of speed
hue_raw = [hsv2rgb_raw((hue, 255, 255)) for hue in range(256)]
hue_rainbow = [hsv2rgb_rainbow((hue, 255, 255)) for hue in range(256)]
hue_spectrum = [hsv2rgb_spectrum((hue, 255, 255)) for hue in range(256)]
hue_360 = [hsv2rgb_360((hue, 1.0, 1.0)) for hue in range(360)]
# print hue_360


def hue2rgb_raw(hue):
    if hue >= 0 or hue < 256:
        return hue_raw[hue]
    else:
        raise ValueError("hue must be between 0 and 255")


def hue2rgb_rainbow(hue):
    if hue >= 0 or hue < 256:
        return hue_rainbow[hue]
    else:
        raise ValueError("hue must be between 0 and 255")


def hue2rgb_spectrum(hue):
    if hue >= 0 or hue < 256:
        return hue_spectrum[hue]
    else:
        raise ValueError("hue must be between 0 and 255")


def hue2rgb_360(hue):
    if hue >= 0 or hue < 360:
        return hue_360[hue]
    else:
        raise ValueError("hue must be between 0 and 359")

hsv2rgb = hsv2rgb_rainbow
hue2rgb = hue2rgb_rainbow


def hex2rgb(hex):
    """Helper for converting RGB and RGBA hex values to Color"""
    hex = hex.strip('#')
    if len(hex) == 6:
        split = (hex[0:2], hex[2:4], hex[4:6])
    else:
        raise ValueError('Must pass in a 6 character hex value!')

    r, g, b = [int(x, 16) for x in split]

    return (r, g, b)


WHEEL_MAX = 384


def _gen_wheel():
    for p in range(385):
        if p < 128:
            r = 127 - p % 128
            g = p % 128
            b = 0
        elif p < 256:
            g = 127 - p % 128
            b = p % 128
            r = 0
        else:
            b = 127 - p % 128
            r = p % 128
            g = 0

    return (r, g, b)


_wheel = _gen_wheel()


def wheel_color(position):
    """Get color from wheel value (0 - 384).
    Provided for those used to using it from Adafruit libraries
    """
    if position < 0:
        position = 0
    if position > 384:
        position = 384

    return _wheel[position]


def hue_gradient(start, stop, steps):
    assert (start >= 0 and start < 256) and (
        stop >= 0 and stop < 256), "hue must be between 0 and 255"
    flip = False
    if start > stop:
        start, stop = stop, start
        flip = True

    stops = util.even_dist(start, stop, steps)

    if flip:
        stops = stops[::-1]

    return stops


def hue_helper(pos, length, cycle_step):
    return hue2rgb(((pos * 255 // length) + cycle_step) % 255)


def hue_helper360(pos, length, cycle_step):
    return hue2rgb_360(((pos * 360 // length) + cycle_step) % 360)


def wheel_helper(pos, length, cycle_step):
    """Helper for wheel_color that distributes colors over length and allows shifting position"""
    return wheel_color(((pos * WHEEL_MAX // length) + cycle_step) % WHEEL_MAX)

Off = (0, 0, 0)
Blue = (0, 0, 255)
Pink = (255, 192, 203)
Honeydew = (240, 255, 240)
Purple = (128, 0, 128)
Fuchsia = (255, 0, 255)
LawnGreen = (124, 252, 0)
AliceBlue = (240, 248, 255)
Crimson = (220, 20, 60)
White = (255, 255, 255)
NavajoWhite = (255, 222, 173)
Cornsilk = (255, 248, 220)
Bisque = (255, 228, 196)
PaleGreen = (152, 251, 152)
Brown = (165, 42, 42)
DarkTurquoise = (0, 206, 209)
DarkGreen = (0, 100, 0)
MediumOrchid = (186, 85, 211)
Chocolate = (210, 105, 30)
PapayaWhip = (255, 239, 213)
Olive = (128, 128, 0)
DarkSalmon = (233, 150, 122)
PeachPuff = (255, 218, 185)
Plum = (221, 160, 221)
DarkGoldenrod = (184, 134, 11)
MintCream = (245, 255, 250)
CornflowerBlue = (100, 149, 237)
HotPink = (255, 105, 180)
DarkBlue = (0, 0, 139)
LimeGreen = (50, 205, 50)
DeepSkyBlue = (0, 191, 255)
DarkKhaki = (189, 183, 107)
LightGrey = (211, 211, 211)
Yellow = (255, 255, 0)
LightSalmon = (255, 160, 122)
MistyRose = (255, 228, 225)
SandyBrown = (244, 164, 96)
DeepPink = (255, 20, 147)
Magenta = (255, 0, 255)
Amethyst = (153, 102, 204)
DarkCyan = (0, 139, 139)
GreenYellow = (173, 255, 47)
DarkOrchid = (153, 50, 204)
OliveDrab = (107, 142, 35)
Chartreuse = (127, 255, 0)
Peru = (205, 133, 63)
Orange = (255, 165, 0)
Red = (255, 0, 0)
Wheat = (245, 222, 179)
LightCyan = (224, 255, 255)
LightSeaGreen = (32, 178, 170)
BlueViolet = (138, 43, 226)
Cyan = (0, 255, 255)
MediumPurple = (147, 112, 219)
MidnightBlue = (25, 25, 112)
Gainsboro = (220, 220, 220)
PaleTurquoise = (175, 238, 238)
PaleGoldenrod = (238, 232, 170)
Gray = (128, 128, 128)
MediumSeaGreen = (60, 179, 113)
Moccasin = (255, 228, 181)
Ivory = (255, 255, 240)
SlateBlue = (106, 90, 205)
Green = (0, 255, 0)
Green_HTML = (0, 128, 0)
DarkSlateBlue = (72, 61, 139)
Teal = (0, 128, 128)
Azure = (240, 255, 255)
LightSteelBlue = (176, 196, 222)
Tan = (210, 180, 140)
AntiqueWhite = (250, 235, 215)
WhiteSmoke = (245, 245, 245)
GhostWhite = (248, 248, 255)
MediumTurquoise = (72, 209, 204)
FloralWhite = (255, 250, 240)
LavenderBlush = (255, 240, 245)
SeaGreen = (46, 139, 87)
Lavender = (230, 230, 250)
BlanchedAlmond = (255, 235, 205)
DarkOliveGreen = (85, 107, 47)
DarkSeaGreen = (143, 188, 143)
Violet = (238, 130, 238)
Navy = (0, 0, 128)
Beige = (245, 245, 220)
SaddleBrown = (139, 69, 19)
IndianRed = (205, 92, 92)
Snow = (255, 250, 250)
SteelBlue = (70, 130, 180)
MediumSlateBlue = (123, 104, 238)
Black = (0, 0, 0)
LightBlue = (173, 216, 230)
Turquoise = (64, 224, 208)
MediumVioletRed = (199, 21, 133)
DarkViolet = (148, 0, 211)
DarkGray = (169, 169, 169)
Salmon = (250, 128, 114)
DarkMagenta = (139, 0, 139)
Tomato = (255, 99, 71)
SkyBlue = (135, 206, 235)
Goldenrod = (218, 165, 32)
MediumSpringGreen = (0, 250, 154)
DodgerBlue = (30, 144, 255)
Aqua = (0, 255, 255)
ForestGreen = (34, 139, 34)
DarkRed = (139, 0, 0)
SlateGray = (112, 128, 144)
Indigo = (75, 0, 130)
CadetBlue = (95, 158, 160)
LightYellow = (255, 255, 224)
DarkOrange = (255, 140, 0)
PowderBlue = (176, 224, 230)
RoyalBlue = (65, 105, 225)
Sienna = (160, 82, 45)
Thistle = (216, 191, 216)
Lime = (0, 255, 0)
Seashell = (255, 245, 238)
LemonChiffon = (255, 250, 205)
LightSkyBlue = (135, 206, 250)
YellowGreen = (154, 205, 50)
Plaid = (204, 85, 51)
Aquamarine = (127, 255, 212)
LightCoral = (240, 128, 128)
DarkSlateGray = (47, 79, 79)
Coral = (255, 127, 80)
Khaki = (240, 230, 140)
BurlyWood = (222, 184, 135)
LightGoldenrodYellow = (250, 250, 210)
MediumBlue = (0, 0, 205)
LightSlateGray = (119, 136, 153)
RosyBrown = (188, 143, 143)
Silver = (192, 192, 192)
PaleVioletRed = (219, 112, 147)
FireBrick = (178, 34, 34)
SpringGreen = (0, 255, 127)
LightGreen = (144, 238, 144)
Linen = (250, 240, 230)
OrangeRed = (255, 69, 0)
DimGray = (105, 105, 105)
Maroon = (128, 0, 0)
LightPink = (255, 182, 193)
MediumAquamarine = (102, 205, 170)
Gold = (255, 215, 0)
Orchid = (218, 112, 214)
OldLace = (253, 245, 230)
