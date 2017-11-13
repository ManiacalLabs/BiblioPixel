from .. import log, util
import colorsys


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
    """Generates RGB values from HSV values in line with a typical light
    spectrum."""
    h, s, v = hsv
    return hsv2rgb_raw(((h * 192) >> 8, s, v))


def hsv2rgb_rainbow(hsv):
    """Generates RGB values from HSV that have an even visual
    distribution.  Be careful as this method is only have as fast as
    hsv2rgb_spectrum."""

    def nscale8x3_video(r, g, b, scale):
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

    def scale8_video_LEAVING_R1_DIRTY(i, scale):
        nonzeroscale = 0
        if scale != 0:
            nonzeroscale = 1
        if i != 0:
            i = ((i * scale) >> 8) + nonzeroscale
        return i

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
        r, g, b = nscale8x3_video(r, g, b, s)
        desat = 255 - s
        desat = (desat * desat) >> 8
        brightness_floor = desat
        r = r + brightness_floor
        g = g + brightness_floor
        b = b + brightness_floor

    if v != 255:
        v = scale8_video_LEAVING_R1_DIRTY(v, v)
        r, g, b = nscale8x3_video(r, g, b, v)

    return (r, g, b)


def hsv2rgb_360(hsv):
    """Python default hsv to rgb conversion for when hue values in the
    range 0-359 are preferred.  Due to requiring float math, this method
    is slower than hsv2rgb_rainbow and hsv2rgb_spectrum."""

    h, s, v = hsv

    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return (int(r * 255.0), int(g * 255.0), int(b * 255.0))


# pre-generated spectra for the sake of speed
HUE_RAW = [hsv2rgb_raw((hue, 255, 255)) for hue in range(256)]
HUE_RAINBOW = [hsv2rgb_rainbow((hue, 255, 255)) for hue in range(256)]
HUE_SPECTRUM = [hsv2rgb_spectrum((hue, 255, 255)) for hue in range(256)]
HUE_360 = [hsv2rgb_360((hue, 1.0, 1.0)) for hue in range(360)]


def hue2rgb_raw(hue):
    if hue >= 0 or hue < 256:
        return HUE_RAW[int(hue)]
    else:
        raise ValueError("hue must be between 0 and 255")


def hue2rgb_rainbow(hue):
    if hue >= 0 or hue < 256:
        return HUE_RAINBOW[int(hue)]
    else:
        raise ValueError("hue must be between 0 and 255")


def hue2rgb_spectrum(hue):
    if hue >= 0 or hue < 256:
        return HUE_SPECTRUM[int(hue)]
    else:
        raise ValueError("hue must be between 0 and 255")


def hue2rgb_360(hue):
    if hue >= 0 or hue < 360:
        return HUE_360[int(hue)]
    else:
        raise ValueError("hue must be between 0 and 359")


hsv2rgb = hsv2rgb_rainbow
hue2rgb = hue2rgb_rainbow


def hue_gradient(start, stop, steps):
    if not (0 <= start <= 255 and 0 <= stop <= 255):
        log.error(
            'hue must be between 0 and 255; start=%s, stop=%s', start, stop)
        start = min(255, max(0, start))
        stop = min(255, max(0, stop))
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


def rgb_to_hsv(pixel):
    return colorsys.rgb_to_hsv(*(p / 255 for p in pixel))


def color_cmp(a, b):
    """Order colors by hue, saturation and value, in that order.

    Returns -1 if a < b, 0 if a == b and 1 if a < b.
    """
    if a == b:
        return 0

    a, b = rgb_to_hsv(a), rgb_to_hsv(b)
    return -1 if a < b else 1
