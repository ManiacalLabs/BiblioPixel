import ctypes
from multiprocessing.sharedctypes import RawArray

# Note https://stackoverflow.com/questions/37705974/

BYTE, FLOAT = ctypes.c_uint8, ctypes.c_float


def shared_list_maker(type):
    return lambda size: RawArray(type, size)


def list_maker(size):
    return [(0, 0, 0)] * size


class Maker(object):
    def __init__(self, integer=False, shared_memory=False):
        if shared_memory:
            self.make_packet = shared_list_maker(BYTE)
            number_type = BYTE if integer else FLOAT
            self.color_list = shared_list_maker(3 * number_type)

        else:
            self.make_packet = bytearray
            self.color_list = list_maker


MAKER = Maker()
ColorList = MAKER.color_list
