from . import Rotation, rotate_and_flip


def gen_matrix(dx, dy, serpentine=True, offset=0,
               rotation=Rotation.ROTATE_0, y_flip=False):
    """Helper method to generate X,Y coordinate maps for strips"""

    result = []
    for y in range(dy):
        if not serpentine or y % 2 == 0:
            result.append([(dx * y) + x + offset for x in range(dx)])
        else:
            result.append([((dx * (y + 1)) - 1) - x + offset for x in range(dx)])

    result = rotate_and_flip(result, rotation, y_flip)

    return result


def layout_from_matrix(coord_map):
    max_width = 0
    for x in coord_map:
        if len(x) > max_width:
            max_width = len(x)

    num = len(coord_map) * max_width
    result = [None] * num

    for y in range(len(coord_map)):
        for x in range(len(coord_map[y])):
            result[coord_map[y][x]] = [x, y, 0]

    return result
