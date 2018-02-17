import struct
from . import websocket
from .. driver_base import DriverBase
from ... util import log, server_cache


class SimPixel(DriverBase):
    """Output a simulation of your displat to the web-based
    simulator at http://simpixel.io

    Provides the same parameters of
    :py:class:`bibliopixel.drivers.driver_base.DriverBase` as
    well as those below:

    :param int port: Port to serve websocket server on.
    :param pixel_positions: Override the automatic generation of pyhsical
        pixel layout. This value can be generated via the methods in
        :py:mod:`bibliopixel.layout.geometry`
    """

    CACHE = server_cache.ServerCache(websocket.Server, selectInterval=0.001)

    def __init__(self, num=1024, port=1337, pixel_positions=None, **kwds):

        super().__init__(num, **kwds)
        self.port = port
        self.pixel_positions = self.server = self.thread = None

        if pixel_positions:
            self.set_pixel_positions(pixel_positions)

    def start(self):
        """SHOULD BE PRIVATE"""
        self.server = self.CACHE.get_server(self.port)
        if self.pixel_positions:
            self.server.update(positions=self.pixel_positions)

    def set_pixel_positions(self, pixel_positions):
        """SHOULD BE PRIVATE"""
        # Flatten list of led positions.
        pl = [c for p in pixel_positions for c in p]
        self.pixel_positions = bytearray(struct.pack('<%sh' % len(pl), *pl))
        if self.server:
            self.server.update(positions=self.pixel_positions)

    def cleanup(self):
        """SHOULD BE PRIVATE"""
        self.server.close()

    def _compute_packet(self):
        self._render()

    def _send_packet(self):
        self.server.update(pixels=self._buf)


# This is DEPRECATED.
DriverSimPixel = SimPixel
