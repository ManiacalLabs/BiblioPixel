import struct
from . import websocket
from .. server_driver import ServerDriver


class SimPixel(ServerDriver):
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

    SERVER_CLASS = websocket.Server
    SERVER_KWDS = {'selectInterval': 0.001}

    def __init__(self, num=1024, port=1337, **kwds):
        """
        Args:
            num:  number of LEDs being visualizer.
            port:  the port on which the SimPixel server is running.
            pixel_positions:  the positions of the LEDs in 3-d space.
            **kwds:  keywords passed to DriverBase.
        """
        super().__init__(num, address=port, **kwds)

    def _on_positions(self):
        # Flatten list of led positions.
        if self.server:
            pl = [c for p in self.pixel_positions for c in p]
            positions = bytearray(struct.pack('<%sh' % len(pl), *pl))
            self.server.update(positions=positions)

    def _send_packet(self):
        self.server.update(pixels=self._buf)


from ... util import deprecated
if deprecated.allowed():
    DriverSimPixel = SimPixel
