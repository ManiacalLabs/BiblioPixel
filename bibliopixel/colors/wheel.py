def _gen_wheel():
    result = []
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
        result.append((r, g, b))

    return result


_WHEEL = _gen_wheel()


def wheel_color(position):
    """Get color from wheel value (0 - 384).
    Provided for those used to using it from Adafruit libraries
    """
    return _WHEEL[round(position) % len(_WHEEL)]


def wheel_helper(pos, length, cycle_step):
    """Helper for wheel_color that distributes colors over length and
    allows shifting position."""
    return wheel_color((pos * len(_WHEEL) / length) + cycle_step)
