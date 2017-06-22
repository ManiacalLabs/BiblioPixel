"""These are operations that transform an x, y matrix index."""


def reflect_x(x, y, matrix):
    """Reflect the index vertically."""
    return matrix.columns - 1 - x, y


def reflect_y(x, y, matrix):
    """Reflect the index horizontally."""
    return x, matrix.rows - 1 - y


def serpentine_x(x, y, matrix):
    """Every other row is indexed in reverse."""
    if y % 2:
        return matrix.columns - 1 - x, y
    return x, y


def serpentine_y(x, y, matrix):
    """Every other column is indexed in reverse."""
    if x % 2:
        return x, matrix.rows - 1 - y
    return x, y


def transpose(x, y, _):
    """Transpose rows and columns."""
    return y, x
