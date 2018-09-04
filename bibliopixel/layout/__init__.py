from . circle import Circle
from . matrix import Matrix
from . cube import Cube
from . pov import POV
from . strip import Strip
from . geometry.matrix import make_matrix_coord_map
from . geometry.circle import make_circle_coord_map
from . geometry.cube import make_cube_coord_map

from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    from . circle import LEDCircle
    from . cube import LEDCube
    from . matrix import LEDMatrix
    from . pov import LEDPOV
    from . strip import LEDStrip
    from . geometry.rotation import Rotation
