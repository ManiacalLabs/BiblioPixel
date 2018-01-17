import functools
from ...drivers.channel_order import ChannelOrder

USAGE = """
A ChannelOrder can be initialized with:

* A list, tuple or string of lengths three: '012', 'bgr', (0, 2, 1)
* An integer from 0 to 5."""

NAMES = {
    'r': 0,
    'g': 1,
    'b': 2,
    'R': 0,
    'G': 1,
    'B': 2,
    '0': 0,
    '1': 1,
    '2': 2,
    0: 0,
    1: 1,
    2: 2,
}


@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(tuple)
@make.register(list)
@make.register(str)
def _(c):
    i = ChannelOrder.ORDERS.index(tuple(NAMES[i] for i in c))
    return ChannelOrder.ORDERS[i]


@make.register(int)
def _(c):
    if c < 0:
        raise IndexError('RGB indices cannot be negative')
    return ChannelOrder.ORDERS[c]
