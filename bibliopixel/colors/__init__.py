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
from . hue import hsv2rgb_spectrum, hsv2rgb_rainbow, hsv2rgb_360
from . hue import hsv2rgb, hue2rgb, hex2rgb, hue_gradient, hue2rgb_360
from . hue import hue_helper, hue_helper360
from . wheel import wheel_color, wheel_helper


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

# COLORS is a dictionary of lowercase color names to color values.
COLORS = {k.lower(): v for k, v in locals().items() if k.istitle()}
