import numpy
from ctypes import c_float, c_uint8
from multiprocessing.sharedctypes import RawArray
from .. util import log
from . import importer


# These are just the ones we are sure to work with.  numpy defines a
# lot more, and we pass the names right through, if you want to experiment
# with 'float128' or whatever.
NUMPY_TYPES = (
    'int', 'int8', 'int16', 'int32', 'int64',
    'uint', 'uint8', 'uint16', 'uint32', 'uint64',
    'float', 'float32', 'float64')

NUMPY_DEFAULTS = (True, 'true', 'True', 'float')


class Maker:
    def __init__(self, floating=None, shared_memory=False, numpy_dtype=None):
        if numpy_dtype:
            log.debug('Using numpy')
            if numpy_dtype in NUMPY_DEFAULTS:
                numpy_dtype = 'float32'
            if numpy_dtype not in numpy.sctypeDict:
                raise ValueError(BAD_NUMPY_TYPE_ERROR % numpy_dtype)

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
NUMPY_MAKER = Maker(numpy_dtype='float')

ColorList = MAKER.color_list
NumpyColorList = NUMPY_MAKER.color_list

BAD_NUMPY_TYPE_ERROR = """
Bad numpy_type "%s"

Possible numpy_type values include:
    """ + ' '.join(NUMPY_TYPES)
