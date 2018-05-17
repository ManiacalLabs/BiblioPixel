import copy, ctypes, enum
from . server_driver import ServerDriver
from .. util import artnet_message, log, offset_range, server_cache, udp


class ArtNet(ServerDriver):
    SERVER_CLASS = udp.Sender

    def __init__(self, *args, ip_address='', port=artnet_message.UDP_PORT,
                 filter_dupes=True, offset=0, **kwds):
        """
        :param dict channel_map: maps DMX channels to positions in
            the color_list
        :param int offset: a DMX channel offset, positive, negative or zero
        """
        super().__init__(*args, address=(ip_address, port), **kwds)
        self.filter_dupes = filter_dupes
        self.offset = offset_range.DMXChannel(offset)
        self.msg = artnet_message.dmx_message()
        self.last_message = None

    def _send_packet(self):
        self._copy_buffer_into_data()
        msg = bytes(self.msg)
        if not (self.filter_dupes and msg == self.last_message):
            self.server.send(msg)
            self.last_message = msg

    def _copy_buffer_into_data(self):
        self.offset.copy_to(self._buf, self.msg.data)

    def _on_positions(self):
        pass
