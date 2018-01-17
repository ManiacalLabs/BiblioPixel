import functools
from ...drivers.ledtype import LEDTYPE

USAGE = """
An LEDTYPE is represented by a string.

Possible LEDTYPEs are """ + ', '.join(LEDTYPE.__members__)


@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(LEDTYPE)
def _(c):
    return c


@make.register(str)
def _(c):
    return LEDTYPE[c]
