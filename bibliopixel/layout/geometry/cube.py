from . rotation import rotate_and_flip
from . matrix import make_matrix_coord_map


def make_cube_coord_map(dx, dy, dz, xy_serpentine=True, offset=0,
                        xy_rotation=0, z_rotation=0,
                        y_flip=False, z_flip=False):
    result = []
    plane_offset = offset
    for z in range(dz):
        plane = make_matrix_coord_map(dx, dy, serpentine=xy_serpentine,
                                      offset=plane_offset, rotation=xy_rotation,
                                      y_flip=y_flip)
        plane_offset += (dx * dy)
        result.append(plane)

    result = rotate_and_flip(result, z_rotation, z_flip)

    return result


def make_cube_coord_map_positions(coord_map):
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
