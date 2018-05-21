import math
from .. util import colors, log
from . import font

##########################################################################
# Drawing Functions
# Lovingly borrowed from Adafruit
# https://github.com/adafruit/Adafruit-GFX-Library/blob/master/Adafruit_GFX.cpp
##########################################################################


def draw_circle(setter, x0, y0, r, color=None):
    """
    Draws a circle at point x0, y0 with radius r of the specified RGB color
    """
    f = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x = 0
    y = r

    setter(x0, y0 + r, color)
    setter(x0, y0 - r, color)
    setter(x0 + r, y0, color)
    setter(x0 - r, y0, color)

    while x < y:
        if f >= 0:
            y -= 1
            ddF_y += 2
            f += ddF_y
        x += 1
        ddF_x += 2
        f += ddF_x

        setter(x0 + x, y0 + y, color)
        setter(x0 - x, y0 + y, color)
        setter(x0 + x, y0 - y, color)
        setter(x0 - x, y0 - y, color)
        setter(x0 + y, y0 + x, color)
        setter(x0 - y, y0 + x, color)
        setter(x0 + y, y0 - x, color)
        setter(x0 - y, y0 - x, color)


def _draw_circle_helper(setter, x0, y0, r, cornername, color=None):
    f = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x = 0
    y = r

    while x < y:
        if (f >= 0):
            y -= 1
            ddF_y += 2
            f += ddF_y
        x += 1
        ddF_x += 2
        f += ddF_x
        if (cornername & 0x4):
            setter(x0 + x, y0 + y, color)
            setter(x0 + y, y0 + x, color)

        if (cornername & 0x2):
            setter(x0 + x, y0 - y, color)
            setter(x0 + y, y0 - x, color)

        if (cornername & 0x8):
            setter(x0 - y, y0 + x, color)
            setter(x0 - x, y0 + y, color)

        if (cornername & 0x1):
            setter(x0 - y, y0 - x, color)
            setter(x0 - x, y0 - y, color)


def _fill_circle_helper(setter, x0, y0, r, cornername, delta, color=None):
    f = 1 - r
    ddF_x = 1
    ddF_y = -2 * r
    x = 0
    y = r

    while (x < y):
        if (f >= 0):
            y -= 1
            ddF_y += 2
            f += ddF_y
        x += 1
        ddF_x += 2
        f += ddF_x

        if (cornername & 0x1):
            _draw_fast_vline(setter, x0 + x, y0 - y, 2 * y + 1 + delta, color)
            _draw_fast_vline(setter, x0 + y, y0 - x, 2 * x + 1 + delta, color)

        if (cornername & 0x2):
            _draw_fast_vline(setter, x0 - x, y0 - y, 2 * y + 1 + delta, color)
            _draw_fast_vline(setter, x0 - y, y0 - x, 2 * x + 1 + delta, color)


def fill_circle(setter, x0, y0, r, color=None):
    """Draws a filled circle at point x0,y0 with radius r and specified color"""
    _draw_fast_vline(setter, x0, y0 - r, 2 * r + 1, color)
    _fill_circle_helper(setter, x0, y0, r, 3, 0, color)


def draw_line(setter, x0, y0, x1, y1, color=None, colorFunc=None, aa=False):
    if aa:
        wu_line(setter, x0, y0, x1, y1, color, colorFunc)
    else:
        bresenham_line(setter, x0, y0, x1, y1, color, colorFunc)


# Bresenham's algorithm
def bresenham_line(setter, x0, y0, x1, y1, color=None, colorFunc=None):
    """Draw line from point x0,y0 to x,1,y1. Will draw beyond matrix bounds."""
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)

    err = dx / 2

    if y0 < y1:
        ystep = 1
    else:
        ystep = -1

    count = 0
    for x in range(x0, x1 + 1):
        if colorFunc:
            color = colorFunc(count)
            count += 1

        if steep:
            setter(y0, x, color)
        else:
            setter(x, y0, color)

        err -= dy
        if err < 0:
            y0 += ystep
            err += dx
# END Bresenham's algorithm


# Xiaolin Wu's _line Algorithm
def wu_line(setter, x0, y0, x1, y1, color=None, colorFunc=None):
    funcCount = [0]  # python2 hack since nonlocal not available

    def plot(x, y, level):
        c = color
        if colorFunc:
            c = colorFunc(funcCount[0])
            funcCount[0] += 1

        c = colors.color_scale(color, int(255 * level))
        setter(int(x), int(y), c)

    def ipart(x):
        return int(x)

    def fpart(x):
        return x - math.floor(x)

    def rfpart(x):
        return 1.0 - fpart(x)

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx

    # handle first endpoint
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend  # this will be used in the main loop
    ypxl1 = ipart(yend)

    if steep:
        plot(ypxl1, xpxl1, rfpart(yend) * xgap)
        plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap)
    else:
        plot(xpxl1, ypxl1, rfpart(yend) * xgap)
        plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap)

    # first y-intersection for the main loop
    intery = yend + gradient

    # handle second endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend  # this will be used in the main loop
    ypxl2 = ipart(yend)

    if steep:
        plot(ypxl2, xpxl2, rfpart(yend) * xgap)
        plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap)
    else:
        plot(xpxl2, ypxl2, rfpart(yend) * xgap)
        plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap)

    # main loop
    for x in range(int(xpxl1 + 1), int(xpxl2)):
        if steep:
            plot(ipart(intery), x, rfpart(intery))
            plot(ipart(intery) + 1, x, fpart(intery))
        else:
            plot(x, ipart(intery), rfpart(intery))
            plot(x, ipart(intery) + 1, fpart(intery))
        intery = intery + gradient

# END Xiaolin Wu's _line Algorithm


def _draw_fast_vline(setter, x, y, h, color=None, aa=False):
    draw_line(setter, x, y, x, y + h - 1, color, aa)


def _draw_fast_hline(setter, x, y, w, color=None, aa=False):
    draw_line(setter, x, y, x + w - 1, y, color, aa)


def draw_rect(setter, x, y, w, h, color=None, aa=False):
    """Draw rectangle with top-left corner at x,y, width w and height h"""
    _draw_fast_hline(setter, x, y, w, color, aa)
    _draw_fast_hline(setter, x, y + h - 1, w, color, aa)
    _draw_fast_vline(setter, x, y, h, color, aa)
    _draw_fast_vline(setter, x + w - 1, y, h, color, aa)


def fill_rect(setter, x, y, w, h, color=None, aa=False):
    """Draw solid rectangle with top-left corner at x,y, width w and height h"""
    for i in range(x, x + w):
        _draw_fast_vline(setter, i, y, h, color, aa)


def draw_round_rect(setter, x, y, w, h, r, color=None, aa=False):
    """Draw rectangle with top-left corner at x,y, width w, height h,
    and corner radius r.
    """
    _draw_fast_hline(setter, x + r, y, w - 2 * r, color, aa)  # Top
    _draw_fast_hline(setter, x + r, y + h - 1, w - 2 * r, color, aa)  # Bottom
    _draw_fast_vline(setter, x, y + r, h - 2 * r, color, aa)  # Left
    _draw_fast_vline(setter, x + w - 1, y + r, h - 2 * r, color, aa)  # Right
    # draw four corners
    _draw_circle_helper(setter, x + r, y + r, r, 1, color, aa)
    _draw_circle_helper(setter, x + w - r - 1, y + r, r, 2, color, aa)
    _draw_circle_helper(setter, x + w - r - 1, y + h - r - 1, r, 4, color, aa)
    _draw_circle_helper(setter, x + r, y + h - r - 1, r, 8, color, aa)


def fill_round_rect(setter, x, y, w, h, r, color=None, aa=False):
    """Draw solid rectangle with top-left corner at x,y, width w, height h,
    and corner radius r"""
    fill_rect(setter, x + r, y, w - 2 * r, h, color, aa)
    _fill_circle_helper(setter, x + w - r - 1, y + r, r,
                        1, h - 2 * r - 1, color, aa)
    _fill_circle_helper(setter, x + r, y + r, r, 2, h - 2 * r - 1, color, aa)


def draw_triangle(setter, x0, y0, x1, y1, x2, y2, color=None, aa=False):
    """Draw triangle with points x0,y0 - x1,y1 - x2,y2"""
    draw_line(setter, x0, y0, x1, y1, color, aa)
    draw_line(setter, x1, y1, x2, y2, color, aa)
    draw_line(setter, x2, y2, x0, y0, color, aa)


def fill_triangle(setter, x0, y0, x1, y1, x2, y2, color=None, aa=False):
    """Draw solid triangle with points x0,y0 - x1,y1 - x2,y2"""
    a = b = y = last = 0

    if y0 > y1:
        y0, y1 = y1, y0
        x0, x1 = x1, x0
    if y1 > y2:
        y2, y1 = y1, y2
        x2, x1 = x1, x2
    if y0 > y1:
        y0, y1 = y1, y0
        x0, x1 = x1, x0

    if y0 == y2:  # Handle awkward all-on-same-line case as its own thing
        a = b = x0
        if x1 < a:
            a = x1
        elif x1 > b:
            b = x1
        if x2 < a:
            a = x2
        elif x2 > b:
            b = x2
            _draw_fast_hline(setter, a, y0, b - a + 1, color, aa)

    dx01 = x1 - x0
    dy01 = y1 - y0
    dx02 = x2 - x0
    dy02 = y2 - y0
    dx12 = x2 - x1
    dy12 = y2 - y1
    sa = 0
    sb = 0

    # For upper part of triangle, find scanline crossings for segments
    # 0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1
    # is included here (and second loop will be skipped, avoiding a /0
    # error there), otherwise scanline y1 is skipped here and handled
    # in the second loop...which also avoids a /0 error here if y0=y1
    # (flat-topped triangle).

    if y1 == y2:
        last = y1  # include y1 scanline
    else:
        last = y1 - 1  # skip it

    for y in range(y, last + 1):
        a = x0 + sa / dy01
        b = x0 + sb / dy02
        sa += dx01
        sb += dx02

        if a > b:
            a, b = b, a
            _draw_fast_hline(setter, a, y, b - a + 1, color, aa)

    # For lower part of triangle, find scanline crossings for segments
    # 0-2 and 1-2.  This loop is skipped if y1=y2.
    sa = dx12 * (y - y1)
    sb = dx02 * (y - y0)

    for y in range(y, y2 + 1):
        a = x1 + sa / dy12
        b = x0 + sb / dy02
        sa += dx12
        sb += dx02

        if a > b:
            a, b = b, a
            _draw_fast_hline(setter, a, y, b - a + 1, color, aa)


def draw_char(fonts, setter, width, height, x, y, c, color, bg,
              aa=False, font=font.default_font, font_scale=1):
    if font_scale < 1:
        log.error('font_scale %s must be >= 1', font_scale)
        font_scale = 1
    f = fonts[font]
    fh = f['height']
    FONT = f['data']

    c = ord(c)  # make it the int value
    if c < f['bounds'][0] or c > f['bounds'][1]:
        c_data = f['undef']
    else:
        c_data = FONT[c - f['bounds'][0]]

    fw = len(c_data)
    for i in range(fw + f['sep']):
        x_pos = x + (i * font_scale)
        if max(0, 1 - font_scale * fw) <= x_pos < width:
            if i >= fw:
                line = 0
            else:
                line = FONT[c][i]
            for j in range(fh):
                y_pos = y + (j * font_scale)
                if ((y_pos < height) and
                        (y_pos + fh * font_scale - 1) >= 0):
                    if line & 0x1:
                        if font_scale == 1:
                            setter(x_pos, y_pos, color)
                        else:
                            fill_rect(setter, x_pos, y_pos, font_scale,
                                      font_scale, color, aa)
                    elif bg != color and bg is not None:
                        if font_scale == 1:
                            setter(x_pos, y_pos, bg)
                        else:
                            fill_rect(setter, x_pos, y_pos, font_scale,
                                      font_scale, bg, aa)
                line >>= 1
    return fw + f['sep']


def draw_text(fonts, setter, text, width, height, x=0, y=0,
              color=None, bg=colors.Off, aa=False,
              font=font.default_font, font_scale=1):
    fh = fonts[font]['height']
    for c in text:
        if c == '\n':
            y += font_scale * fh
            x = 0
        elif c == '\r':
            pass  # skip it
        else:
            fw = draw_char(fonts, setter, width, height,
                           x, y, c, color, bg, aa, font, font_scale)
            x += font_scale * fw
            if x >= width:
                break
