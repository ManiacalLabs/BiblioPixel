import errno, struct, threading, uuid
from ... import log
from .. driver_base import DriverBase
from . import websocket

ADDRESS_IN_USE_ERROR = """

Port {0} on your machine is already in use.
Perhaps BiblioPixel is already running on your machine?
"""


class SimPixel(DriverBase):

    def __init__(self, num, port=1337, layout=None, **kwds):
        super().__init__(num, **kwds)
        self.port = port
        self.layout = self.server = self.thread = None
        self.websocks = {}

        if layout:
            self.set_layout(layout)

    def __start_server(self):
        log.debug('Starting server...')
        desc = dict(driver=self, layout=self.layout, selectInterval=0.001)
        try:
            self.server = websocket.Server(
                '', self.port, websocket.Client, **desc)
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                e.strerror += ADDRESS_IN_USE_ERROR.format(self.port)
                e.args = (e.errno, e.strerror)
            raise

        self.thread = threading.Thread(target=self._serve_forever, daemon=True)
        self.thread.start()

    def _serve_forever(self):
        try:
            self.server.serveforever()
        except:
            pass
        log.debug('WebSocket Server closed')

    def set_layout(self, layout):
        if not (self.thread and self.thread.is_alive()):
            # flatten layout
            pl = [c for p in layout for c in p]
            self.layout = bytearray(struct.pack('<%sh' % len(pl), *pl))
            self.__start_server()

    def add_websock(self, oid, send_pixels):
        self.websocks[oid] = send_pixels

    def remove_websock(self, oid):
        try:
            del self.websocks[oid]
        except KeyError:
            pass

    def cleanup(self):
        self.server.close()

    def _compute_packet(self):
        self._render()

    def _send_packet(self):
        for ws in self.websocks.values():
            ws(self._buf)


# This is DEPRECATED.
DriverSimPixel = SimPixel
