class MatrixRotation:
    ROTATE_0 = 0  # no rotation
    ROTATE_90 = 3  # rotate 90 degrees
    ROTATE_180 = 2  # rotate 180 degrees
    ROTATE_270 = 1  # rotate 270 degrees


def mapGen(width, height, serpentine=True, offset=0,
           rotation=MatrixRotation.ROTATE_0, vert_flip=False):
    """Helper method to generate X,Y coordinate maps for strips"""

    result = []
    for y in range(height):
        if not serpentine or y % 2 == 0:
            result.append([(width * y) + x + offset for x in range(width)])
        else:
            result.append([((width * (y + 1)) - 1) - x +
                           offset for x in range(width)])

    for i in range(rotation):
        result = list(zip(*result[::-1]))

    if vert_flip:
        result = result[::-1]

    return result


class MultiMapBuilder(object):

    def __init__(self):
        self.map = []
        self.offset = 0

    def addRow(self, *maps):
        yOff = len(self.map)
        lengths = [len(m) for m in maps]
        h = max(lengths)
        if(min(lengths) != h):
            raise ValueError("All maps in row must be the same height!")

        offsets = [0 + self.offset]
        count = 0
        for m in maps:
            offsets.append(h * len(m[0]) + offsets[count])
            count += 1

        for y in range(h):
            self.map.append([])
            for x in range(len(maps)):
                self.map[y + yOff] += [i + offsets[x] for i in maps[x][y]]

        self.offset = offsets[len(offsets) - 1]
