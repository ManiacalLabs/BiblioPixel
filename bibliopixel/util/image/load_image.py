from ... util import colors
from ... layout import Matrix


def show_image(setter, width, height,
               image_path='', image_obj=None, offset=(0, 0), bgcolor=colors.Off,
               brightness=255):
    """Display an image on a matrix."""
    bgcolor = colors.color_scale(bgcolor, brightness)

    img = image_obj
    if image_path and not img:
        from PIL import Image

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


def showImage(layout, imagePath="", imageObj=None, offset=(0, 0),
              bgcolor=colors.Off, brightness=255):
    """Display an image on the matrix"""
    if not isinstance(layout, Matrix):
        raise RuntimeError("Must use Matrix with showImage!")

    layout.all_off()

    return show_image(layout.set, layout.width, layout.height, imagePath,
                      imageObj, offset, bgcolor, brightness)


def loadImage(layout, imagePath="", imageObj=None, offset=(0, 0),
              bgcolor=colors.Off, brightness=255):
    """Display an image on the matrix"""

    if not isinstance(layout, Matrix):
        raise RuntimeError("Must use Matrix with loadImage!")

    texture = [[colors.Off for x in range(layout.width)]
               for y in range(layout.height)]

    def setter(x, y, pixel):
        if y >= 0 and x >= 0:
            texture[y][x] = pixel

    show_image(setter, layout.width, layout.height, imagePath, imageObj,
               offset, bgcolor, brightness)

    return texture
