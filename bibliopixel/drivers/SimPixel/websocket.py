import threading, uuid
from ... util import log
from . SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class Client(WebSocket):

    def __init__(self, *args, driver):
        super().__init__(*args)
        self.driver = driver
        self.connected = False
        self.oid = None
        log.debug('Server started...')

    def handleConnected(self):
        log.debug('Connected:{}'.format(self.address))
        self.connected = True
        self.oid = uuid.uuid1()
        self.driver.add_websock(self.oid, self.send_pixels)
        self.sendMessage(bytearray([0x00, 0x00]) + self.driver.pixel_positions)

    def handleClose(self):
        self.driver.remove_websock(self.oid)
        self.connected = False
        log.debug('Closed:{}'.format(self.address))

    def handleMessage(self):
        pass

    def send_pixels(self, pixels):
        if self.connected:
            self.sendMessage(bytearray([0x00, 0x01]) + pixels)


class Server:

    def __init__(self, port, **kwds):
        self.ws_server = SimpleWebSocketServer('', port, Client, **kwds)
        self.thread = threading.Thread(target=self.target, daemon=True)
        self.thread.start()

    def stop(self):
        self.ws_server.stop()

    def close(self):
        self.ws_server.close()

    def is_alive(self):
        return self.thread.is_alive()

    def target(self):
        log.info('Starting WebSocket server thread...')
        try:
            self.ws_server.serveforever()
        except:
            pass
        log.info('WebSocket server closed')
