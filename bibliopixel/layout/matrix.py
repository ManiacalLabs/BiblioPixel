from . import index_ops


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
