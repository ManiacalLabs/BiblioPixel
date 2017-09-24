from . import index_ops
from . rotation import rotate_and_flip
import copy


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


def make_matrix_coord_map(
        dx, dy, serpentine=True, offset=0, rotation=0, y_flip=False):
    """Helper method to generate X,Y coordinate maps for strips"""
    result = []
    for y in range(dy):
        if not serpentine or y % 2 == 0:
            result.append([(dx * y) + x + offset for x in range(dx)])
        else:
            result.append([dx * (y + 1) - 1 - x + offset for x in range(dx)])

    result = rotate_and_flip(result, rotation, y_flip)

    return result


DEFAULT_CONFIG = {
    'serpentine': True,
    'rotation': 0,
    'y_flip': False
}


def make_matrix_coord_map_multi(config, rotation=0, y_flip=False):
    matrix_offset = 0
    matrix_result = []

    def populate_config(cfg):
        return dict(DEFAULT_CONFIG, **cfg)

    def add_row(offset, matrix, row):
        for y in row:
            matrix.append([x + offset for x in y])

        return offset + sum([len(y) for y in row])

    def combine_cols(cols):
        row_offset = 0
        row = []
        for col in cols:
            count = 0
            for i, y in enumerate(col):
                offset_col = [x + row_offset for x in y]
                if i >= len(row):
                    row.append(offset_col)
                else:
                    row[i] += offset_col
                count += len(col)
            row_offset += count
        return row

    if isinstance(config, dict):
        matrix_result = make_matrix_coord_map(**config)

    else:
        for row in config:
            if isinstance(row, dict):  # is configs
                row = populate_config(row)
                matrix_offset = add_row(
                    matrix_offset, matrix_result, make_matrix_coord_map(**row))

            elif isinstance(row, list):  # is row
                cols = []
                for config in row:
                    config = populate_config(config)
                    cols.append(make_matrix_coord_map(**config))

                matrix_offset = add_row(
                    matrix_offset, matrix_result, combine_cols(cols))

    return rotate_and_flip(matrix_result, rotation, y_flip)


def make_matrix_coord_map_positions(coord_map):
    num = len(coord_map) * max(len(x) for x in coord_map)
    result = [None] * num

    for y in range(len(coord_map)):
        for x in range(len(coord_map[y])):
            result[coord_map[y][x]] = [x, y, 0]

    return result
