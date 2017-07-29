from . geometry import gen_matrix


class MultiMapBuilder:

    def __init__(self, make_object):
        self.map = []
        self.offset = 0
        self.make_object = make_object

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

    def make_driver(self, width, height, matrix=None, **kwds):
        self.addRow(gen_matrix(width, height, **(matrix or {})))
        return self.make_object(width=width, height=height, **kwds)
