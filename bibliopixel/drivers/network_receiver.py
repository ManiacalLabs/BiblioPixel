import threading
import os
import SocketServer
from network import CMDTYPE, RETURN_CODES

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import log


class ThreadedDataHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            cmd = ord(self.request.recv(1))
            r = bytes(self.request.recv(2))
            size = (ord(r[1]) << 8) | ord(r[0])

            if cmd == CMDTYPE.PIXEL_DATA:
                data = bytearray()
                emptyCount = 0
                while len(data) < size:
                    buf = self.request.recv(4096)
                    if len(buf) == 0:
                        emptyCount += 1
                    if emptyCount >= 5:
                        log.exception(
                            "Failed to receive expected amount of data! Expected: %s bytes / Received: %s bytes", size, len(data))
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
                if self.server.setBrightness:
                    if self.server.setBrightness(bright):
                        result = RETURN_CODES.SUCCESS

                packet = bytearray()
                packet.append(result)
                self.request.sendall(packet)

        except Exception as e:
            log.exception(e)
            pass  # if there's a comm error, just move on
        return


class ThreadedDataServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    update = None
    setBrightness = None
    hasFrame = None


class NetworkReceiver:

    def __init__(self, led, port=3142, interface='0.0.0.0'):
        self._led = led
        self.address = (interface, port)
        SocketServer.TCPServer.allow_reuse_address = True
        self._server = ThreadedDataServer(self.address, ThreadedDataHandler)
        self._server.update = self._update
        self._server.setBrightness = self._led.setMasterBrightness

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

    def _update(self, data):
        self._led.setBuffer(list(data))
        self._led.update()
