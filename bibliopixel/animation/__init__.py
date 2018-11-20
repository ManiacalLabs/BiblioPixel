from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    from . animation import Animation, BaseAnimation
    from . circle import BaseCircleAnim, Circle
    from . cube import BaseCubeAnim
    from . game import BaseGameAnim
    from . matrix import BaseMatrixAnim
    from . off import Off, OffAnim
    from . receiver import BaseReceiver
    from . sequence import Sequence
    from . strip import BaseStripAnim
    from . tests import (
        StripChannelTest, MatrixChannelTest, MatrixCalibrationTest)

    strip_test = StripChannelTest
    matrix_calibration = MatrixCalibrationTest
    matrix_test = MatrixChannelTest
