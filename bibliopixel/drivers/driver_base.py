import time
import sys


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
                 gamma=None, gamma_value=1.0, min_value=0, max_value=255):
        if num == 0:
            num = width * height
            if num == 0:
                raise ValueError(
                    "Either num or width and height must be provided!")

        self.numLEDs = num
        self.gamma = gamma or range(256)
        self.gamma_value = gamma_value

        self.c_order = c_order
        self.perm = ChannelOrder.ORDERS.index(c_order)

        self.width = width
        self.height = height
        self._buf = bytearray(self.bufByteCount())

        self._thread = None
        self.lastUpdate = 0

        self._frame = None

        try:
            import timedata
            self._renderer = timedata.Renderer(
                gamma=gamma_value,
                permutation=self.perm,
                min=min_value,
                max=max_value).render
        except:
            pass

    def cleanup(self):
        return self.__exit__(None, None, None)

    def bufByteCount(self):
        return 3 * self.numLEDs

    # Push new data to strand
    def _receive_colors(self, colors, pos):
        # TODO: use abc here.
        raise RuntimeError("Base class receive_colors() called.")

    def receive_colors(self, colors, pos):
        start = time.time() * 1000.0
        self._receive_colors(colors, pos)
        if self._thread:
            self.lastUpdate = (time.time() * 1000.0) - start

    def set_brightness(self, brightness):
        if brightness > 255 or brightness < 0:
            raise ValueError('Brightness must be between 0 and 255')
        self._brightness = brightness
        return True

    def _renderer(self, colors, offset=0, length=-1, output=None):
        gamma, (r, g, b) = self.gamma, self.c_order
        for i in range(length):
            fix = lambda x: gamma[int(max(0, min(255, int(x))))]  # flake8: noqa
            ci = colors[i + offset]
            colors[i + pos] = (fix(ci[r]), fix(ci[g]), fix(ci[b]))
        return bytearray(i for c in colors for i in c)

    def _render(self, colors, offset):
        self._frame = self._renderer(
            colors, offset=offset, length=self.numLEDs, output=self._frame)
        return self._frame
