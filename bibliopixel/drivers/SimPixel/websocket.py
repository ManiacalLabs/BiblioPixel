import uuid
from ... import log
from . SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

Server = SimpleWebSocketServer


class Client(WebSocket):

    def __init__(self, *args, driver, layout):
        super().__init__(*args)
        self.driver = driver
        self.connected = False
        self.layout = layout
        self.oid = None
        log.debug('Server started...')

    def handleConnected(self):
        log.debug('Connected:{}'.format(self.address))
        self.connected = True
        self.oid = uuid.uuid1()
        self.driver.add_websock(self.oid, self.send_pixels)
        self.sendMessage(bytearray([0x00, 0x00]) + self.layout)

    def handleClose(self):
        self.driver.remove_websock(self.oid)
        self.connected = False
        log.debug('Closed:{}'.format(self.address))

    def handleMessage(self):
        pass

    def send_pixels(self, pixels):
        if self.connected:
            self.sendMessage(bytearray([0x00, 0x01]) + pixels)
