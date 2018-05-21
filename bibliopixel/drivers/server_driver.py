from . driver_base import DriverBase
from .. util.server_cache import StaticCache
from .. project import construct


class ServerDriver(DriverBase, StaticCache):
    def __init__(self, *args, address, pixel_positions=None, **kwds):
        """
        Args:
            port:  the port on which the SimPixel server is running.
            pixel_positions:  the positions of the LEDs in 3-d space.
            **kwds:  keywords passed to DriverBase.
        """
        super().__init__(*args, **kwds)
        self.address = address
        self.server = self.thread = None
        self.pixel_positions = pixel_positions
        if pixel_positions:
            self.set_pixel_positions(pixel_positions)

    def start(self):
        self.server = self.cache().get_server(self.address)
        self._on_positions()

    def set_pixel_positions(self, pixel_positions):
        # This is the "automatic" update from the layout - don't overwrite
        # any pixel_position set in the constructor.
        if self.pixel_positions is None:
            self.pixel_positions = pixel_positions
            self._on_positions()

    def _send_packet(self):
        pass

    def _on_positions(self):
        pass

    def cleanup(self):
        self.server and self.server.close()

    def _compute_packet(self):
        self._render()
