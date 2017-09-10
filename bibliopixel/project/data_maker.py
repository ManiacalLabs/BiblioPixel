import os
from ctypes import c_float, c_uint8
from multiprocessing.sharedctypes import RawArray
from .. util import log
from .. util.color_list import numpy, numpy_array

NUMPY_DTYPE = os.environ.get('BP_NUMPY_DTYPE')


class Maker:
    def __init__(
            self, floating=None, shared_memory=False, numpy_dtype=NUMPY_DTYPE):
        if numpy_dtype:
            if numpy_array:
                log.info('Using numpy')
            else:
                log.error('numpy module is not available.')
                numpy_dtype = None

        if shared_memory and numpy_dtype:
            log.error('Shared memory for numpy arrays is not yet supported.')
            numpy_dtype = None

        if floating is None:
            floating = not shared_memory

        c_type = c_float if floating else c_uint8

        if shared_memory:
            def color_list(size, pixel_size=3):
                return RawArray(pixel_size * c_type, size)

            self.bytes = lambda size: RawArray(c_uint8, size)
            self.color_list = color_list
            # Note https://stackoverflow.com/questions/37705974/

        elif numpy_dtype:
            def color_list(size, pixel_size=3):
                return numpy.zeros((size, pixel_size), numpy_dtype)
            self.bytes = bytearray
            self.color_list = color_list

        else:
            def color_list(size, pixel_size=3):
                return [tuple(0 for i in range(pixel_size))] * size

            self.bytes = bytearray
            self.color_list = color_list


MAKER = Maker()
ColorList = MAKER.color_list
