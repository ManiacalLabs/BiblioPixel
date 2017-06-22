from . import index_ops
from . import Rotation, rotate_and_flip


class Matrix(object):
    """Map a matrix onto a strip of lights."""

    def __init__(self, strip, columns=None, rows=None,
                 reflect_x=False, reflect_y=False,
                 serpentine_x=False, serpentine_y=False,
                 transpose=False):
        self.strip = strip

        if columns:
            if not rows:
                rows = len(strip) // columns
            elif rows * columns > len(strip):
                raise IndexError('Index out of range.')
        elif rows:
            columns = len(strip) // rows
        else:
            raise ValueError('Must supply either rows or columns')
        self.columns, self.rows = columns, rows

        ops = (reflect_x and index_ops.reflect_x,
               reflect_y and index_ops.reflect_y,
               serpentine_x and index_ops.serpentine_x,
               serpentine_y and index_ops.serpentine_y,
               transpose and index_ops.transpose)
        self.operations = list(filter(None, ops))

    def _index(self, x, y):
        for o in self.operations:
            x, y = o(x, y, self)

        if 0 <= x < self.columns and 0 <= y < self.rows:
            return x + y * self.columns

        raise IndexError('Index out of range.')

    def get(self, x, y):
        return self.strip[self._index(x, y)]

    def set(self, x, y, value):
        self.strip[self._index(x, y)] = value


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


def pixel_positions_from_matrix(coord_map):
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
