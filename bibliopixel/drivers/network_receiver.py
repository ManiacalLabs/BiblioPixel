import os, threading

import socketserver as SocketServer
from .. drivers.return_codes import RETURN_CODES
from . network import CMDTYPE
from .. util import log


class ThreadedDataHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            cmd = ord(self.request.recv(1))
            r = bytes(self.request.recv(2))
            size = (ord(r[1]) << 8) | ord(r[0])

            if cmd == CMDTYPE.PIXEL_DATA:
                data = bytearray()
                empty_count = 0
                while len(data) < size:
                    buf = self.request.recv(4096)
                    if len(buf) == 0:
                        empty_count += 1
                    if empty_count >= 5:
                        log.exception(
                            "Failed to receive expected amount of data! "
                            "Expected: %s bytes / Received: %s bytes",
                            size, len(data))
                        self.request.sendall(RETURN_CODES.ERROR_SIZE)
                        return

                    data.extend(buf)

                if len(data) != size:
                    log.exception(
                        "Received data size incorrect! "
                        "Expected: %s bytes / Received: {%s bytes",
                        size, len(data))
                    return

                self.server.update(data)

                if self.server.hasFrame:
                    while self.server.hasFrame():
                        pass

                packet = bytearray()
                packet.append(RETURN_CODES.SUCCESS)
                self.request.sendall(packet)

            elif cmd == CMDTYPE.BRIGHTNESS:
                res = self.request.recv(1)
                bright = ord(res)
                result = RETURN_CODES.ERROR_UNSUPPORTED
                if self.server.set_brightness:
                    if self.server.set_brightness(bright):
                        result = RETURN_CODES.SUCCESS
                    else:
                        # Try again.
                        self.server.set_brightness(bright)

                packet = bytearray()
                packet.append(result)
                self.request.sendall(packet)

        except Exception as e:
            log.exception(e)
            pass  # if there's a comm error, just move on
        return


class ThreadedDataServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    update = None
    set_brightness = None
    hasFrame = None


class NetworkReceiver:

    def __init__(self, layout, port=3142, interface='0.0.0.0'):
        self.layout = layout
        self.address = (interface, port)
        SocketServer.TCPServer.allow_reuse_address = True
        self._server = ThreadedDataServer(self.address, ThreadedDataHandler)
        self._server.update = self.update
        self._server.set_brightness = self.layout.set_brightness

    def start(self, join=False):
        self._t = threading.Thread(target=self._server.serve_forever)
        self._t.setDaemon(True)  # don't hang on exit
        self._t.start()
        log.info("Listening on %s", self.address)
        if join:
            self._t.join()

    def stop(self):
        log.info("Closing server...")
        self._server.shutdown()
        self._server.server_close()
        # self._t.join()

    def update(self, data):
        self.layout.setBuffer(list(data))
        self.layout.push_to_driver()
