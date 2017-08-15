import functools
from ...layout.geometry.rotation import Rotation

USAGE = """A Rotation is represented by a string or an integer

Possible Rotations are 0, 1, 2, 3, or 0, 90, 180, 350, or
""" + ', '.join(Rotation.__members__)


ROTATION_NAMES = {
    0: Rotation.ROTATE_0,
    1: Rotation.ROTATE_270,
    2: Rotation.ROTATE_180,
    3: Rotation.ROTATE_90,

    90: Rotation.ROTATE_90,
    180: Rotation.ROTATE_180,
    270: Rotation.ROTATE_270,
}


@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(str)
def _(c):
    try:
        c = int(c)
    except:
        return Rotation[c]
    else:
        return ROTATION_NAMES[c]


@make.register(int)
def _(c):
    return ROTATION_NAMES[c]
