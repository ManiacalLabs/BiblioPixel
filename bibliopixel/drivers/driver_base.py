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

    def __init__(self, num=0, width=0, height=0, c_order=ChannelOrder.RGB, gamma=None):
        if num == 0:
            num = width * height
            if num == 0:
                raise ValueError(
                    "Either num or width and height must be provided!")

        self.numLEDs = num
        self.gamma = gamma or range(256)

        self.c_order = c_order
        self.perm = ChannelOrder.ORDERS.index(c_order)

        self.width = width
        self.height = height
        self._buf = bytearray(self.bufByteCount())

        self._thread = None
        self.lastUpdate = 0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
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

    def setMasterBrightness(self, brightness):
        return False

    def _write_colors_to_buffer(self, colors, pos):
        gamma, (r, g, b) = self.gamma, self.c_order
        for i in range(self.numLEDs):
            fix = lambda x: gamma[max(0, min(255, int(x)))]
            c = tuple(int(x) for x in colors[i + pos])
            self._buf[i * 3:(i + 1) * 3] = fix(c[r]), fix(c[g]), fix(c[b])
