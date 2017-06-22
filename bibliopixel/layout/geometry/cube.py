from . import Rotation, rotate_and_flip
from . matrix import gen_matrix


def gen_cube(dx, dy, dz, xy_serpentine=True, offset=0,
             xy_rotation=Rotation.ROTATE_0, z_rotation=Rotation.ROTATE_0,
             y_flip=False, z_flip=False):
    result = []
    plane_offset = offset
    for z in range(dz):
        plane = gen_matrix(dx, dy, serpentine=xy_serpentine,
                           offset=plane_offset, rotation=xy_rotation,
                           y_flip=y_flip)
        plane_offset += (dx * dy)
        result.append(plane)

    result = rotate_and_flip(result, z_rotation, z_flip)

    return result


def pixel_positions_from_cube(coord_map):
    num = 0
    dx, dy, dz = (0, 0, len(coord_map))

    for xy in coord_map:
        if len(xy) > dx:
            dy = len(xy)
        for x in xy:
            if len(x) > dx:
                dx = len(x)
            num += len(x)

    result = [None] * num
    for z in range(dz):
        for y in range(dy):
            for x in range(dx):
                result[coord_map[z][y][x]] = [x, y, z]
    return result
