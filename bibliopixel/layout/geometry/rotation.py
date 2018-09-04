from enum import IntEnum


def rotate_and_flip(coord_map, rotation, flip):
    rotation = (-rotation % 360) // 90
    for i in range(rotation):
        coord_map = list(zip(*coord_map[::-1]))

    if flip:
        coord_map = coord_map[::-1]

    return coord_map


from ... util import deprecated
if deprecated.allowed():  # pragma: no cover
    class Rotation(IntEnum):
        ROTATE_0 = 0  # no rotation
        ROTATE_90 = 90  # rotate 90 degrees
        ROTATE_180 = 180  # rotate 180 degrees
        ROTATE_270 = 270  # rotate 270 degrees
