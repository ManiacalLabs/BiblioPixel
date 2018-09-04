from . animation import Animation
from .. util import log
import threading
from enum import IntEnum


class HOST_TYPE(IntEnum):
    STRIP = 1
    MATRIX = 2
    CIRCLE = 3
    CUBE = 4


HOST_MAP = {
    'Strip': HOST_TYPE.STRIP,
    'Matrix': HOST_TYPE.MATRIX,
    'Circle': HOST_TYPE.CIRCLE,
    'Cube': HOST_TYPE.CUBE,
}


class Receiver(Animation):
    free_run = True

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)
        name = type(self.layout).__name__

        if name not in HOST_MAP:
            raise ValueError('layout must be of type' + ', '.join(HOST_MAP))

        self.host_type = HOST_MAP[name]
        self._hold_for_data = threading.Event()
        self._stop_event = threading.Event()
        self._stop_event.clear()
        self._recv_thread_obj = None

    def pre_run(self):
        self.start()

    def start(self):
        self._t = threading.Thread(target=self._recv_thread_obj)
        self._t.setDaemon(True)  # don't hang on exit
        self._t.start()
        log.info("Receiver Listening on %s", self.address)

    def thread_cleanup(self):
        # To be overriden, if need be
        pass

    def stop(self):
        self._stop_event.set()
        log.info("Stopping Receiver...")
        self.thread_cleanup()

    def _exit(self, type, value, traceback):
        self.stop()

    def step(self, amt=1):
        """
        This may seem silly, but on a Receiver step() need not do anything.
        Instead, receive the data on the receive thread and set it on the buffer
        then call self._hold_for_data.set()
        """
        if not self._stop_event.isSet():
            self._hold_for_data.wait()
            self._hold_for_data.clear()


from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    BaseReceiver = Receiver
