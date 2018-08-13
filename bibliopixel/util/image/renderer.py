from ... util import colors, log
from ... layout import Matrix, Strip


def renderer(layout, color, pixel_width, pixel_height,
             ellipse, vertical, frame, padding):
    if not isinstance(layout, (Matrix, Strip)):
        raise ValueError('Cannot render a layout of type %s' % type(layout))

    from PIL import Image, ImageDraw

    shape = layout.shape
    if len(shape) == 1:
        if vertical:
            shape, getter = (1, shape[0]), lambda x, y: layout.get(y)
        else:
            shape, getter = (shape[0], 1), lambda x, y: layout.get(x)
    else:
        getter = layout.get

    # LED width and height
    width, height = shape

    # width and height for individual pixels
    pw, ph = pixel_width, pixel_width
    ph = pw if ph is None else ph

    # Cell width and height
    cw, ch = pw + 2 * padding, ph + 2 * padding
    image_size = 2 * frame + width * cw, 2 * frame + height * ch

    def render():
        image = Image.new('RGB', image_size, color)
        draw = ImageDraw.Draw(image)
        draw_pixel = draw.ellipse if ellipse else draw.rectangle
        offset = frame + padding

        for x in range(width):
            px = offset + x * cw
            for y in range(height):
                py = offset + y * ch
                pcolor = tuple(int(i) for i in getter(x, y))
                draw_pixel((px, py, px + pw, py + ph), pcolor, pcolor)

        return image

    return render
