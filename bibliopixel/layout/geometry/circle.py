from ... util import pointOnCircle
import math


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


def make_circle_coord_map(rings=None, pixels_per=None, offset=0, invert=False):
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
                raise ValueError(
                    '"rings" values must only be first and last index.')
            if r[0] < r[1]:
                indices = list(range(r[0], r[1]))
            else:
                indices = list(range(r[1], r[0]))[::-1]
            out_rings.append(indices)
            num += len(indices)

        if invert:
            out_rings = out_rings[::-1]

        return (out_rings, calc_ring_steps(out_rings))


def make_circle_coord_map_positions(
        rings, origin=(0, 0, 0), z_diff=0, radii=None):
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
            if radii:
                radius = radii[i]
            else:
                radius = (len(r) - 1) * math.pi
            x, y = pointOnCircle(0, 0, radius, angle)
            if use_z:
                points[p] = (x + ox, y + oy, z + oz)
            else:
                points[p] = (x + ox, y + oy)

            angle += step

        z += z_diff

    return points
