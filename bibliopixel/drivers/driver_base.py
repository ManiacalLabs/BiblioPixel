from .. import gamma as _gamma
from .. import timedata

import time


class ChannelOrder:
    RGB = 0, 1, 2
    RBG = 0, 2, 1
    GRB = 1, 0, 2
    GBR = 1, 2, 0
    BRG = 2, 0, 1
    BGR = 2, 1, 0

    ORDERS = RGB, RBG, GRB, GBR, BRG, BGR


class DriverBase(object):
    """Base driver class to build other drivers from"""

    def __init__(self, num=0, width=0, height=0, c_order=ChannelOrder.RGB,
                 gamma=None):
        if num == 0:
            num = width * height
            if num == 0:
                raise ValueError(
                    "Either num or width and height must be provided!")

        self.numLEDs = num
        gamma = gamma or _gamma.DEFAULT
        self.gamma = gamma

        self.c_order = c_order
        self.perm = ChannelOrder.ORDERS.index(c_order)

        self.width = width
        self.height = height
        self._buf = self._make_buf()

        self._thread = None
        self.lastUpdate = 0

        self._render_td = timedata.Renderer(
            gamma=gamma.gamma,
            offset=gamma.offset,
            permutation=self.perm,
            min=gamma.lower_bound,
            max=255)


    def _make_buf(self):
        return bytearray(self.bufByteCount())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def cleanup(self):
        return self.__exit__(None, None, None)

    def bufByteCount(self):
        return 3 * self.numLEDs

    def sync(self):
        pass

    def _compute_packet(self, colors, pos):
        """Compute the packet from the colors and position.

        Eventually, this will run on the compute thread.
        """
        return colors, pos

    def _send_packet(self, packet):
        """Send the packet to the driver.

        Eventually, this will run on an I/O thread.
        """
        pass

    def receive_colors(self, colors, pos):
        if self._thread:
            start = time.time() * 1000.0

        packet = self._compute_packet(colors, pos)
        self._send_packet(packet)

        if self._thread:
            self.lastUpdate = (time.time() * 1000.0) - start

    def set_brightness(self, brightness):
        if brightness > 255 or brightness < 0:
            raise ValueError('Brightness not between 0 and 255: %s' % brightness)
        self._brightness = brightness
        return True

    def _render_py(self, colors, pos, length=-1, output=None):
        fix, (r, g, b) = self.gamma.get, self.c_order
        for i in range(length):
            c = tuple(int(x) for x in colors[i + pos])
            output[i * 3:(i + 1) * 3] = fix(c[r]), fix(c[g]), fix(c[b])
        return output

    def _render(self, colors, pos):
        r = (hasattr(colors, 'indexer') and self._render_td) or self._render_py
        self._buf = r(colors, pos, self.numLEDs, self._buf)
