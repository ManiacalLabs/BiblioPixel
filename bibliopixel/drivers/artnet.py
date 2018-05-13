import copy, ctypes, enum
from . server_driver import ServerDriver
from .. util import artnet_message, log, server_cache, udp


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
        self.offset = offset
        self.msg = artnet_message.dmx_message()
        self.last_message = None

    def _send_packet(self):
        self._copy_buffer_into_data()
        msg = bytes(self.msg)
        if not (self.filter_dupes and msg == self.last_message):
            self.server.send(msg)
            self.last_message = msg

    def _copy_buffer_into_data(self):
        buf, offset, data = self._buf, self.offset, self.msg.data
        if offset < 0:
            buf = buf[-offset:]
            offset = 0

        delta = len(data) - len(buf) - offset
        if delta <= 0:
            # data is shorter
            data[:] = buf[offset:offset + len(data)]
        else:
            # data is longer
            data[:len(buf) - offset] = buf[offset:]

    def _on_positions(self):
        pass
