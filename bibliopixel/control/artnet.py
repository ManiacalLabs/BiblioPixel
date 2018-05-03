import collections, copy, queue
from . import control
from .. util import artnet_message, log, server_cache, udp

QUEUE_TIMEOUT = 0.1


class ArtNet(control.ExtractedControl):
    def __init__(self, *args, ip_address, port=artnet_message.UDP_PORT, **kwds):
        super().__init__(*args, **kwds)
        self.address = ip_address, port

    def _convert(self, msg):
        msg = artnet_message.bytes_to_message(msg)
        assert any(i for i in msg.data)
        msg = collections.OrderedDict((
            ('type', 'dmx'),
            ('net', msg.net),
            ('subUni', msg.subUni),
            ('data', msg.data)))

        return super()._convert(msg)

    def _make_thread(self):
        return udp.Receiver(self.address, receive=self.receive)
