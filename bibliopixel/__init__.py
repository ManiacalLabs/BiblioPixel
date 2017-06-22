from . layout import Circle, Matrix, POV, Strip, Cube
from . layout.geometry import Rotation
from . layout.geometry.matrix import gen_matrix
from . layout.geometry.circle import gen_circle
from . layout.geometry.cube import gen_cube
from . import animation, colors, font, gamma, layout, log, util

# These are DEPRECATED
from . layout import LEDCircle, LEDMatrix, LEDPOV, LEDStrip, LEDCube


def _get_version():
    from os.path import abspath, dirname, join
    filename = join(dirname(abspath(__file__)), 'VERSION')
    return open(filename).read().strip()


__version__ = _get_version()
VERSION = __version__
