from . geometry import gen_matrix
from .. project import aliases


class MultiMapBuilder:

    def __init__(self, make_object):
        self.map = []
        self.offset = 0
        self.make_object = make_object

    def make_drivers(self, driver, drivers):
        if not drivers:
            return [self.make_object(**aliases.resolve(driver))]

        if driver:
            # driver is a default for each driver.
            drivers = [dict(driver, **d) for d in drivers]

        return [self._make_driver(**d) for d in drivers]

    def _make_driver(self, width, height, matrix=None, **kwds):
        kwds = aliases.resolve(kwds)
        row = gen_matrix(width, height, **(matrix or {}))
        for y, row_entry in enumerate(row):
            self.map.append([i + self.offset for i in row_entry])

        self.offset += len(row) * len(row[0])
        return self.make_object(width=width, height=height, **kwds)

    def addRow(self, *maps):
        # DEPRECATED
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
