import glob, numbers, os, sys
from .. import colors, log
from .. layout import Matrix

try:
    from PIL import Image, ImageSequence
except:
    Image, ImageSequence = None, None


def show_image(setter, width, height,
               image_path='', image_obj=None, offset=(0, 0), bgcolor=colors.Off,
               brightness=255):
    """Display an image on a matrix."""
    bgcolor = colors.color_scale(bgcolor, brightness)

    img = image_obj
    if image_path and not img:
        if not Image:
            error = "Please install Python Imaging Library: pip install pillow"
            log.error(error)
            raise ImportError(error)
        img = Image.open(image_path)
    elif not img:
        raise ValueError('Must provide either image_path or image_obj')

    w = min(width - offset[0], img.size[0])
    h = min(height - offset[1], img.size[1])
    ox = offset[0]
    oy = offset[1]

    for x in range(ox, w + ox):
        for y in range(oy, h + oy):
            r, g, b, a = (0, 0, 0, 255)
            rgba = img.getpixel((x - ox, y - oy))

            if isinstance(rgba, int):
                raise ValueError('Image must be in RGB or RGBA format!')
            if len(rgba) == 3:
                r, g, b = rgba
            elif len(rgba) == 4:
                r, g, b, a = rgba
            else:
                raise ValueError('Image must be in RGB or RGBA format!')

            if a == 0:
                r, g, b = bgcolor
            else:
                r, g, b = colors.color_scale((r, g, b), a)

            if brightness != 255:
                r, g, b = colors.color_scale((r, g, b), brightness)

            setter(x, y, (r, g, b))


def showImage(layout, imagePath="", imageObj=None, offset=(0, 0), bgcolor=colors.Off, brightness=255):
    """Display an image on the matrix"""
    if not isinstance(layout, Matrix):
        raise RuntimeError("Must use Matrix with showImage!")

    layout.all_off()

    return show_image(layout.set, layout.width, layout.height, imagePath, imageObj,
                      offset, bgcolor, brightness)


def loadImage(layout, imagePath="", imageObj=None, offset=(0, 0), bgcolor=colors.Off, brightness=255):
    """Display an image on the matrix"""

    if not isinstance(layout, Matrix):
        raise RuntimeError("Must use Matrix with loadImage!")

    texture = [[colors.Off for x in range(layout.width)] for y in range(layout.height)]

    def setter(x, y, pixel):
        if y >= 0 and x >= 0:
            texture[y][x] = pixel

    show_image(setter, layout.width, layout.height, imagePath, imageObj,
               offset, bgcolor, brightness)

    return texture


def convert_mode(image, mode='RGB'):
    """Return an image in the given mode."""
    return image if (image.mode == mode) else image.convert(mode=mode)


def image_to_colorlist(image, container=list):
    """Given a PIL.Image, returns a ColorList of its pixels."""
    return container(convert_mode(image).getdata())


def animated_gif_to_colorlists(image, container=list):
    """Given an animated GIF, return a list with a colorlist for each frame."""
    it = ImageSequence.Iterator(image)
    return [image_to_colorlist(i, container) for i in it]


def crop(image, top_offset=0, left_offset=0, bottom_offset=0, right_offset=0):
    """Return an image cropped on top, bottom, left or right."""
    if bottom_offset or top_offset or left_offset or right_offset:
        width, height = image.size
        box = (left_offset, top_offset,
               width - right_offset, height - bottom_offset)
        image = image.crop(box=box)

    return image


def resize(image, x, y, stretch=False, top=None, left=None, mode='RGB',
           resample=None):
    """Return an image resized."""
    if x <= 0:
        raise ValueError('x must be greater than zero')
    if y <= 0:
        raise ValueError('y must be greater than zero')

    resample = Image.ANTIALIAS if resample is None else resample
    if not isinstance(resample, numbers.Number):
        try:
            resample = getattr(Image, resample.upper())
        except:
            raise ValueError("(1) Didn't understand resample=%s" % resample)
        if not isinstance(resample, numbers.Number):
            raise ValueError("(2) Didn't understand resample=%s" % resample)

    size = x, y
    if stretch:
        return image.resize(size, resample=resample)
    result = Image.new(mode, size)

    ratios = [d1 / d2 for d1, d2 in zip(size, image.size)]
    if ratios[0] < ratios[1]:
        new_size = (size[0], int(image.size[1] * ratios[0]))
    else:
        new_size = (int(image.size[0] * ratios[1]), size[1])

    image = image.resize(new_size, resample=resample)
    if left is None:
        box_x = int((x - new_size[0]) / 2)
    elif left:
        box_x = 0
    else:
        box_x = x - new_size[0]

    if top is None:
        box_y = int((y - new_size[1]) / 2)
    elif top:
        box_y = 0
    else:
        box_y = y - new_size[1]

    result.paste(image, box=(box_x, box_y))
    return result
