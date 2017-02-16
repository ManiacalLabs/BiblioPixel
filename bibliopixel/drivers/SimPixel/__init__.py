#!/usr/bin/env python
# encoding: utf-8
from .. driver_base import DriverBase, ChannelOrder

import logging
import signal
import sys
import time
import threading
import uuid
import struct
from ... import log

from . SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class SimPixelWebSocket(WebSocket):

    def __init__(self, *args, driver, layout):
        super(SimPixelWebSocket, self).__init__(*args)
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


class DriverSimPixel(DriverBase):

    def __init__(self, num, port=1337, layout=None):
        super(DriverSimPixel, self).__init__(num)
        self.port = port
        self.layout = None
        self.server = self.thread = None
        self.websocks = {}

        if layout:
            self.set_layout(layout)

    def __start_server(self):
        log.debug('Starting server...')
        self.server = SimpleWebSocketServer(
            '', self.port, SimPixelWebSocket,
            driver=self, layout=self.layout, selectInterval=0.001)

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
        if oid in self.websocks:
            del self.websocks[oid]

    def cleanup(self):
        self.server.close()

    def _compute_packet(self):
        self._render()

    def _send_packet(self):
        for ws in self.websocks.values():
            ws(self._buf)
