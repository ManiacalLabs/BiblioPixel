#!/usr/bin/env python
# encoding: utf-8
from .. driver_base import DriverBase, ChannelOrder

import logging
import signal
import sys
import time
import threading
import uuid
from ... import log

from . SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class VisWebSocket(WebSocket):

    def __init__(self, *args, **kwargs):
        super(VisWebSocket, self).__init__(*args, **kwargs)
        self.kinect = None
        self.oid = None
        self.connected = False

    def handleConnected(self):
        log.debug(self.address, 'connected')
        self.connected = True
        # self.kinect = KinectFactory.create_kinect()
        # self.oid = uuid.uuid1()
        # self.kinect.add_observer(self.oid, self.send_depth)

    def handleClose(self):
        # self.kinect.remove_observer(self.oid)
        self.connected = False
        log.debug(self.address, 'closed')

    def handleMessage(self):
        # degs = int(float(self.data))
        # self.kinect.set_tilt(degs)
        pass

    def send_pixels(self, pixels):
        if self.connected:
            self.sendMessage(pixels)


class ws_thread(threading.Thread):
    def __init__(self, server):
        super(ws_thread, self).__init__()
        self.server = server

    def run(self):
        try:
            self.server.serveforever()
        except:
            pass
        log.debug('WebSocket Server closed')


class DriverWebVis(DriverBase):

    def __init__(self, num, port=6666):
        super(DriverWebVis, self).__init__(num)
        self.port = port
        self.server = SimpleWebSocketServer('0.0.0.0', self.port, VisWebSocket)
        self.ws_thread = ws_thread(self.server)
        self.ws_thread.start()

    def cleanup(self):
        self.server.close()

    def _compute_packet(self):
        self._render()

    def _send_packet(self):
        print(self._buf)
        # self.server.send_pixels(self._buf)
