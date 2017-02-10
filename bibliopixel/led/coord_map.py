from .. util import pointOnCircle


class Rotation:
    ROTATE_0 = 0  # no rotation
    ROTATE_90 = 3  # rotate 90 degrees
    ROTATE_180 = 2  # rotate 180 degrees
    ROTATE_270 = 1  # rotate 270 degrees


def rotate_and_flip(coord_map, rotation, flip):
    for i in range(rotation):
        coord_map = list(zip(*coord_map[::-1]))

    if flip:
        coord_map = coord_map[::-1]

    return coord_map


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


def layout_from_cube(coord_map):
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


def calc_ring_pixel_count(rings):
    num = 0
    for r in rings:
        num += len(r)
    return num


def calc_ring_steps(rings):
    steps = []
    for r in rings:
        steps.append(360.0 / len(r))
    return steps


def gen_circle(rings=None, pixels_per=None, offset=0, invert=False):
    if pixels_per:
        rings = []
        for c in pixels_per:
            rings.append([offset, offset + c])
            offset = offset + c

    if not rings:
        raise ValueError('Must specify rings or pixels_per')

    if rings:
        num = 0
        out_rings = []
        for r in rings:
            if len(r) != 2:
                raise ValueError('"rings" values must only be first and last index.')
            if r[0] < r[1]:
                indices = list(range(r[0], r[1]))
            else:
                indices = list(range(r[1], r[0]))[::-1]
            out_rings.append(indices)
            num += len(indices)

        if invert:
            out_rings = out_rings[::-1]

        return (out_rings, calc_ring_steps(out_rings))


def layout_from_rings(rings, origin=(0, 0, 0), z_diff=0):
    if len(origin) not in [2, 3]:
        raise ValueError('origin must be (x,y) or (x,y,z)')

    use_z = len(origin) == 3
    if use_z:
        ox, oy, oz = origin
    else:
        ox, oz = origin

    num = calc_ring_pixel_count(rings)
    steps = calc_ring_steps(rings)

    points = [None] * num
    z = 0
    for i in range(len(rings)):
        r = rings[i]
        step = steps[i]
        angle = 0.0
        for p in r:
            radius = (len(r) * 0.5)
            x, y = pointOnCircle(0, 0, radius, angle)
            if use_z:
                points[p] = (x + ox, y + oy, z + oz)
            else:
                points[p] = (x + ox, y + oy)
            angle += step

        z += z_diff

    return points
