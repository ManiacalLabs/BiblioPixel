from enum import IntEnum


class Rotation(IntEnum):
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
