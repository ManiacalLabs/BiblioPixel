import sys
import os
from . import log

try:
    from PIL import Image, ImageSequence
except ImportError as e:
    error = "Please install Python Imaging Library: pip install pillow"
    log.error(error)
    raise ImportError(error)

import glob
from led import LEDMatrix
import colors


def showImage(led, imagePath="", imageObj=None, offset=(0, 0), bgcolor=colors.Off, brightness=255):
    """Display an image on the matrix"""

    if not isinstance(led, LEDMatrix):
        raise RuntimeError("Must use LEDMatrix with showImage!")

    bgcolor = colors.color_scale(bgcolor, brightness)

    img = imageObj
    if not img and not (imagePath == ""):
        img = Image.open(imagePath)
    elif not img:
        raise ValueError("Must provide either imagePath or imageObj")

    w = led.width - offset[0]
    if img.size[0] < w:
        w = img.size[0]

    h = led.height - offset[1]
    if img.size[1] < h:
        h = img.size[1]

    ox = offset[0]
    oy = offset[1]

    led.all_off()

    for x in range(ox, w + ox):
        for y in range(oy, h + oy):
            r, g, b, a = (0, 0, 0, 255)
            rgba = img.getpixel((x - ox, y - oy))

            if isinstance(rgba, int):
                raise ValueError("Image must be in RGB or RGBA format!")
            if len(rgba) == 3:
                r, g, b = rgba
            elif len(rgba) == 4:
                r, g, b, a = rgba
            else:
                raise ValueError("Image must be in RGB or RGBA format!")

            if a == 0:
                r, g, b = bgcolor
            else:
                r, g, b = colors.color_scale((r, g, b), a)

            if brightness != 255:
                r, g, b = colors.color_scale((r, g, b), brightness)

            led.set(x, y, (r, g, b))


def loadImage(led, imagePath="", imageObj=None, offset=(0, 0), bgcolor=colors.Off, brightness=255):
    """Display an image on the matrix"""

    if not isinstance(led, LEDMatrix):
        raise RuntimeError("Must use LEDMatrix with loadImage!")

    bgcolor = colors.color_scale(bgcolor, brightness)

    img = imageObj
    if not img and not (imagePath == ""):
        img = Image.open(imagePath)
    elif not img:
        raise ValueError("Must provide either imagePath or imageObj")

    w = led.width - offset[0]
    if img.size[0] < w:
        w = img.size[0]

    h = led.height - offset[1]
    if img.size[1] < h:
        h = img.size[1]

    ox = offset[0]
    oy = offset[1]

    texture = [[colors.Off for x in range(led.width)]
               for y in range(led.height)]
    for x in range(ox, w + ox):
        for y in range(oy, h + oy):
            r, g, b, a = (0, 0, 0, 255)
            rgba = img.getpixel((x - ox, y - oy))
            if isinstance(rgba, int):
                raise ValueError("Image must be in RGB or RGBA format!")
            if len(rgba) == 3:
                r, g, b = rgba
            elif len(rgba) == 4:
                r, g, b, a = rgba
            else:
                raise ValueError("Image must be in RGB or RGBA format!")

            if a == 0:
                r, g, b = bgcolor
            else:
                r, g, b = colors.color_scale((r, g, b), a)

            if brightness != 255:
                r, g, b = colors.color_scale((r, g, b), brightness)

            if y >= 0 and x >= 0:
                texture[y][x] = (r, g, b)

    return texture
