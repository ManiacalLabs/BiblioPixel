from driver_base import DriverBase
import time


class DriverDummy(DriverBase):
    """For Testing: Provides no ouput, just a valid interface"""

    def __init__(self, num, delay=0):
        """delay: time to wait in milliseconds to simulate actual hardware interface time"""
        super(DriverDummy, self).__init__(num)
        self._delay = delay

    # Push new data to strand
    def update(self, data):
        if self._delay > 0:
            time.sleep(self._delay / 1000.0)
        else:
            pass
