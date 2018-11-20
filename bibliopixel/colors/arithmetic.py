def color_blend(a, b):
    """
    Performs a Screen blend on RGB color tuples, a and b
    """
    return (255 - (((255 - a[0]) * (255 - b[0])) >> 8),
            255 - (((255 - a[1]) * (255 - b[1])) >> 8),
            255 - (((255 - a[2]) * (255 - b[2])) >> 8))


def color_scale(color, level):
    """
    Scale RGB tuple by level, 0 - 256
    """
    return tuple([int(i * level) >> 8 for i in list(color)])
