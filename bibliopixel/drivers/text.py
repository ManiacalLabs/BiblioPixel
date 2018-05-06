from . driver_base import DriverBase
from .. util.colors import names
from .. util import log
import time


class Text(DriverBase):
    """For testing:  prints colors to terminal"""

    def __init__(self, num=1024, columns=8, max_colors=16, **kwds):
        """
        Args
            delay: time to wait in seconds to simulate actual hardware
            interface time
        """
        super().__init__(num)
        self.columns = columns
        self.max_colors = max_colors

    # Push new data to strand
    def _compute_packet(self):
        count = self.numLEDs
        if self.max_colors:
            count = min(count, self.max_colors)

        for i in range(count):
            if not i % self.columns:
                log.printer()
            hex_color = names.color_to_name(self._colors[i + self._pos], True)
            log.printer(hex_color, ' ', end='')

        if self.max_colors and self.numLEDs > self.max_colors:
            log.printer('...')
        else:
            log.printer('')
        log.printer('--')
