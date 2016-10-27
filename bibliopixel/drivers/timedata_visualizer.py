import ctypes, timedata_visualizer

from . driver_base import DriverBase
from .. import log, timedata

class TimedataVisualizer(DriverBase):
    """Driver for timedata_visualizer UI"""

    def __init__(self, num=0, width=0, height=0, desc=None):
        super().__init__(num, width, height)

        if self.width == 0 and self.height == 0:
            self.width = self.numLEDs
            self.height = 1

        if self.numLEDs != self.width * self.height:
            raise ValueError(
                "Provide either num OR width and height, but not all three.")

        size = self.width * self.height * 3
        self.app = timedata_visualizer.JuceApplication(size)
        self.memory = self.app.memory
        self.address = ctypes.addressof(self.memory)

        self.window = self.app.LightWindow(self.width, self.height)
        ipad = 1
        wpad = 4
        size = 16

        window_desc = dict(
            instrumentPadding=ipad,
            windowPadding=wpad,
            x=2 * size,
            y=2 * size,
            width=self.width * (size + 2 * ipad) + 2 * wpad,
            height=self.height * (size + 2 * ipad) + 2 * wpad,
            name='timedata visualizer for BiblioPixel')
        window_desc.update(desc or {})
        self.window.set_desc(**window_desc)

    def _make_buf(self):
        pass

    def _compute_packet(self, colors, pos):
        self._buf = self.address if timedata.enabled() else self.memory
        self._render(colors, pos)

    def _send_packet(self, packet):
        self.window.repaint()
