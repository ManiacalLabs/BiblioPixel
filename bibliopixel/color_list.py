import ctypes, enum
from multiprocessing.sharedctypes import RawArray
from . import timedata


def color_list_maker(integer=True, shared_memory=False, use_timedata=False):
    if use_timedata:
        assert timedata.enabled() and not shared_memory
        return timedata.make_color_list

    if shared_memory:
        number_type = ctypes.c_uint8 if integer else ctypes.c_float
        return lambda size: RawArray(3 * number_type, size)

    return lambda size: [(0, 0, 0)] * size


ColorList = color_list_maker()
Renderer = timedata.Renderer
