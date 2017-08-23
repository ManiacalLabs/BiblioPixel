import struct
from . import websocket
from .. driver_base import DriverBase
from ... util import log


class SimPixel(DriverBase):

    def __init__(self, num=1024, port=1337, pixel_positions=None, **kwds):
        """
        Args:
            num:  number of LEDs being visualizer.
            port:  the port on which the SimPixel server is running.
            pixel_positions:  the positions of the LEDs in 3-d space.
            **kwds:  keywords passed to DriverBase.
        """
        super().__init__(num, **kwds)
        self.port = port
        self.pixel_positions = self.server = self.thread = None

        if pixel_positions:
            self.set_pixel_positions(pixel_positions)

    def start(self):
        self.server = websocket.make_server(self.port, selectInterval=0.001)
        if self.pixel_positions:
            self.server.update(positions=self.pixel_positions)

    def set_pixel_positions(self, pixel_positions):
        # Flatten list of led positions.
        pl = [c for p in pixel_positions for c in p]
        self.pixel_positions = bytearray(struct.pack('<%sh' % len(pl), *pl))
        if self.server:
            self.server.update(positions=self.pixel_positions)

    def cleanup(self):
        self.server.close()

    def _compute_packet(self):
        self._render()

    def _send_packet(self):
        self.server.update(pixels=self._buf)


# This is DEPRECATED.
DriverSimPixel = SimPixel
