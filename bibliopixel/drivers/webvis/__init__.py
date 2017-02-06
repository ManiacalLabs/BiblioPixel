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


class VisWebSocket(WebSocket):

    def __init__(self, *args, driver, point_list):
        super(VisWebSocket, self).__init__(*args)
        self.driver = driver
        self.connected = False
        self.point_list = point_list
        self.oid = None
        log.debug('Server started...')

    def handleConnected(self):
        log.debug('Connected:{}'.format(self.address))
        self.connected = True
        # self.kinect = KinectFactory.create_kinect()
        self.oid = uuid.uuid1()
        self.driver.add_websock(self.oid, self.send_pixels)
        self.sendMessage(bytearray([0x00, 0x00]) + self.point_list)

    def handleClose(self):
        self.driver.remove_websock(self.oid)
        self.connected = False
        log.debug('Closed:{}'.format(self.address))

    def handleMessage(self):
        # degs = int(float(self.data))
        # self.kinect.set_tilt(degs)
        pass

    def send_pixels(self, pixels):
        if self.connected:
            self.sendMessage(bytearray([0x00, 0x01]) + pixels)
            # print(time.time())


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

    def __init__(self, num, port=1337, point_list=None):
        super(DriverWebVis, self).__init__(num)
        self.port = port
        self.point_list = None
        self.server = self.ws_thread = None
        self.websocks = {}

        if point_list:
            print(point_list)
            self.set_point_list(point_list)

    def __start_server(self):
        log.debug('Starting server...')
        print(self.port)
        self.server = SimpleWebSocketServer('', self.port, VisWebSocket,
                                            driver=self, point_list=self.point_list,
                                            selectInterval=0.001)
        self.ws_thread = ws_thread(self.server)
        self.ws_thread.start()

    def set_point_list(self, point_list):
        if self.ws_thread is None or (not self.ws_thread.is_alive()):
            # flatten point_list
            pl = [c for p in point_list for c in p]
            # print(pl)
            self.point_list = bytearray(struct.pack('<%sh' % len(pl), *pl))
            # print(self.point_list)
            # print(type(self.point_list))
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
        # print(self._buf)
        for ws in self.websocks.values():
            ws(self._buf)
