import time


class ChannelOrder:
    RGB = [0, 1, 2]
    RBG = [0, 2, 1]
    GRB = [1, 0, 2]
    GBR = [1, 2, 0]
    BRG = [2, 0, 1]
    BGR = [2, 1, 0]


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

        self.width = width
        self.height = height
        self._buf = [0] * self.bufByteCount()

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
    def _receive_colors(self, data):
        # TODO: use abc here.
        raise RuntimeError("Base class receive_colors() called.")

    def receive_colors(self, data):
        start = time.time() * 1000.0
        self._receive_colors(data)
        if self._thread:
            self.lastUpdate = (time.time() * 1000.0) - start

    def setMasterBrightness(self, brightness):
        return False

    def _fixData(self, data):
        gamma = self.gamma
        for a, b in enumerate(self.c_order):
            self._buf[a:self.numLEDs * 3:3] = [gamma[v] for v in data[b::3]]
