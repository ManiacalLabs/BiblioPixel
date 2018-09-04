from . driver_base import DriverBase
import time


class Dummy(DriverBase):
    """For Testing: Provides no ouput, just a valid interface"""

    def __init__(self, num=1024, delay=0, **kwds):
        """
        Args
            delay: time to wait in seconds to simulate actual hardware
            interface time
        """
        super().__init__(num)
        self._kwds = kwds
        self._delay = delay

    # Push new data to strand
    def _compute_packet(self):
        if self._delay > 0:
            self.project.sleep(self._delay)
        else:
            pass


from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    DriverDummy = Dummy
