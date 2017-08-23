import errno, threading, uuid
from ... util import log
from . SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

ADDRESS_IN_USE_ERROR = """

Port {0} on your machine is already in use.
Perhaps BiblioPixel is already running on your machine?
"""


class Client(WebSocket):
    POSITION_START = bytearray([0x00, 0x00])
    PIXEL_START = bytearray([0x00, 0x01])

    def __init__(self, *args, server):
        super().__init__(*args)
        self.server = server
        self.connected = False
        log.debug('Server started...')

    def handleConnected(self):
        log.debug('Connected:{}'.format(self.address))
        self.connected = True
        self.server.add_client(self)

    def handleClose(self):
        self.server.remove_client(self)
        self.connected = False
        log.debug('Closed:{}'.format(self.address))

    def handleMessage(self):
        pass

    def update(self, pixels=None, positions=None):
        if self.connected:
            if pixels:
                self.sendFragmentStart(self.PIXEL_START)
                self.sendFragmentEnd(pixels)
            if positions:
                self.sendFragmentStart(self.POSITION_START)
                self.sendFragmentEnd(positions)


class Server:

    def __init__(self, port, selectInterval):
        self.clients = set()
        self.state = {}

        self.ws_server = SimpleWebSocketServer(
            '', port, Client, server=self, selectInterval=selectInterval)
        self.thread = threading.Thread(target=self.target, daemon=True)
        self.thread.start()

    def stop(self):
        self.ws_server.stop()

    def close(self):
        self.ws_server.close()

    def close(self):
        self.server.close()

    def is_alive(self):
        return self.thread.is_alive()

    def target(self):
        log.info('Starting WebSocket server thread...')
        try:
            self.ws_server.serveforever()
        except:
            pass
        log.info('WebSocket server closed')

    def update(self, **state):
        self.state.update(state)
        for client in self.clients:
            client.update(**state)

    def add_client(self, client):
        self.clients.add(client)
        client.update(**self.state)

    def remove_client(self, client):
        try:
            self.clients.remove(client)
        except:
            pass


def make_server(port, *args, **kwds):
    try:
        return Server(port, *args, **kwds)

    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            e.strerror += ADDRESS_IN_USE_ERROR.format(port)
            e.args = (e.errno, e.strerror)
        raise
