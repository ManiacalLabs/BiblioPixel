import copy, ctypes, enum
from . server_driver import ServerDriver
from .. util import artnet_message, log, server_cache, udp


class ArtNet(ServerDriver):
    SERVER_CLASS = udp.Sender

    def __init__(self, *args, ip_address, port=artnet_message.UDP_PORT,
                 filter_dupes=True, **kwds):
        """
        :param dict channel_map: maps DMX channels to positions in
            the color_list
        """
        self.msg = artnet_message.dmx_message()
        self.last_message = None

        address = ip_address, port
        super().__init__(*args, address=address, **kwds)
        self.filter_dupes = filter_dupes

    def _make_buffer(self):
        return self.msg.data

    def _send_packet(self):
        msg = bytes(self.msg)
        if not (self.filter_dupes and msg == self.last_message):
            self.server.send(msg)
            self.last_message = msg

    def _on_positions(self):
        pass
