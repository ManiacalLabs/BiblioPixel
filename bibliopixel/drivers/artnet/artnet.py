import copy, ctypes, enum
from .. server_driver import ServerDriver
from ... util import log, server_cache, udp
from . import dmx_message

UDP_PORT = 0x1936  # 6454


class ArtNet(ServerDriver):
    SERVER_CLASS = udp.Sender

    def __init__(self, *args, ip_address, **kwds):
        """
        :param dict channel_map: maps DMX channels to positions in
            the color_list
        """
        self.msg = dmx_message.dmx_message()

        address = ip_address, UDP_PORT
        super().__init__(*args, address=address, **kwds)

    def _make_buffer(self):
        return self.msg.data

    def _send_packet(self):
        # Regrettably, we need a copy here, because we can't be sure that the
        # next _render won't come before this message has been sent.
        # This is avoidable but not easily...
        self.server.send(copy.copy(self.msg))

    def _on_positions(self):
        pass
