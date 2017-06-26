import functools
from ...drivers.serial import codes

USAGE = """An LEDTYPE is represented by a string.

Possible LEDTYPEs are """ + ', '.join(codes.LEDTYPE.__members__)


@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(str)
def _(c):
    return codes.LEDTYPE[c]
