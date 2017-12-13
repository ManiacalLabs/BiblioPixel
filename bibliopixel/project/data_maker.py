import os
from ctypes import c_float, c_uint8
from multiprocessing.sharedctypes import RawArray
from .. util import log
from .. util.color_list import numpy, numpy_array
from . import importer

NUMPY_DTYPE = os.environ.get('BP_NUMPY_DTYPE')


class Maker:
    def __init__(
            self, floating=None, shared_memory=False, numpy_dtype=NUMPY_DTYPE):
        if numpy_dtype:
            if numpy_array:
                log.info('Using numpy')
            else:
                log.error('The numpy module is not available.')
                print(importer.MISSING_MESSAGE % ('numpy', 'numpy'))

        if shared_memory and numpy_dtype:
            log.error('Shared memory for numpy arrays is not yet supported.')
            numpy_dtype = None

        if floating is None:
            floating = not shared_memory

        c_type = c_float if floating else c_uint8

        if shared_memory:
            self.bytes = lambda size: RawArray(c_uint8, size)
            self.color_list = lambda size: RawArray(3 * c_type, size)
            # Note https://stackoverflow.com/questions/37705974/

        elif numpy_dtype:
            self.bytes = bytearray
            self.color_list = lambda size: numpy.zeros((size, 3), numpy_dtype)

        else:
            self.bytes = bytearray
            self.color_list = lambda size: [(0, 0, 0)] * size


MAKER = Maker()
ColorList = MAKER.color_list
