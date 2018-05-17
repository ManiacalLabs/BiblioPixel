import collections, copy, queue
from . import control
from .. util import artnet_message, log, offset_range, server_cache, udp

QUEUE_TIMEOUT = 0.1


class ArtNet(control.ExtractedControl):
    def __init__(self, *args, ip_address='', port=artnet_message.UDP_PORT,
                 offset=0, **kwds):
        super().__init__(*args, **kwds)
        self.address = ip_address, port
        self.offset = offset_range.DMXChannel.make(offset)

    def _convert(self, msg):
        msg = artnet_message.bytes_to_message(msg)
        if not msg:
            return

        data = bytes(self.offset.read_from(msg.data))
        msg = collections.OrderedDict((
            ('type', 'dmx'),
            ('net', msg.net),
            ('subUni', msg.subUni),
            ('data', data)))

        return super()._convert(msg)

    def _make_thread(self):
        return udp.Receiver(self.address, receive=self.receive)
