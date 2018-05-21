import math


def generate_header(cmd, size):
    packet = bytearray()
    packet.append(cmd)
    packet.append(size & 0xFF)
    packet.append(size >> 8)
    return packet


def tuple_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def tuple_sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def tuple_mult(a, b):
    return tuple(x * y for x, y in zip(a, b))


def tuple_div(a, b):
    return tuple(x / y for x, y in zip(a, b))


def even_dist(start, stop, steps):
    steps -= 1
    start = float(start)
    stop = float(stop)
    div = (stop - start) / steps
    return [int(round(start + x * div)) for x in range(steps)] + [int(stop)]


def pointOnCircle(cx, cy, radius, angle):
    """
    Calculates the coordinates of a point on a circle given the center point,
    radius, and angle.
    """
    angle = math.radians(angle) - (math.pi / 2)
    x = cx + radius * math.cos(angle)
    if x < cx:
        x = math.ceil(x)
    else:
        x = math.floor(x)

    y = cy + radius * math.sin(angle)

    if y < cy:
        y = math.ceil(y)
    else:
        y = math.floor(y)

    return (int(x), int(y))


def genVector(width, height, x_mult=1, y_mult=1):
    """
    Generates a map of vector lengths from the center point to each coordinate.

    width - width of matrix to generate
    height - height of matrix to generate
    x_mult - value to scale x-axis by
    y_mult - value to scale y-axis by
    """
    center_x = (width - 1) / 2
    center_y = (height - 1) / 2

    def length(x, y):
        dx = math.pow(x - center_x, 2 * x_mult)
        dy = math.pow(y - center_y, 2 * y_mult)
        return int(math.sqrt(dx + dy))

    return [[length(x, y) for x in range(width)] for y in range(height)]
