
from . layout import Circle, Matrix, POV, Strip, Cube, font
from . layout.geometry.matrix import make_matrix_coord_map
from . layout.geometry.circle import make_circle_coord_map
from . layout.geometry.cube import make_cube_coord_map
from . import animation, layout, util
from . util import colors, image, log

from . util.colors import gamma
from . drivers import return_codes
from . project import data_maker

from . util import deprecated
if deprecated.allowed():
    from . layout import LEDCircle, LEDMatrix, LEDPOV, LEDStrip, LEDCube
    from . layout import matrix_drawing as matrix
    from . layout.geometry.rotation import Rotation

__version__ = '3.4.18'
__status__ = 'Development'

__description__ = """
BiblioPixel is a pure Python 3 library for all your LED animations needs. Through its fully output agnostic design you can write your code once and use it on a huge variety of outputs, from LED strips to cubes and even a high performance LED simulator!

BiblioPixel allows many different display geometries. Many of the existing hardware models are LED strips, matrixes or circles, but there are no real limits on what the output device can be, due to the output drivers model.
"""
__author__ = 'Adam Haile, Tom Swirly'
__author_email__ = 'adam@maniacallabs.com'
__copyright__ = 'Copyright 2018, Maniacal Labs'
__license__ = 'MIT License'
__url__ = 'https://github.com/maniacallabs/bibliopixel'
__credits__ = '''
Adam Haile, for all his work building BiblioPixel, AllPixel, and Maniacal Labs.
Tom Swirly, for revamping BiblioPixel and keeping Adam sane
Cosmo Borsky, for helping with documentation and some Python
'''

VERSION = __version__
