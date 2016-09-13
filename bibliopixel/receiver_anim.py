from bibliopixel.animation import BaseAnimation
from bibliopixel import log
import threading


class HOST_TYPE:
    STRIP = 1
    MATRIX = 2
    CIRCLE = 3


HOST_MAP = {
    'LEDStrip': HOST_TYPE.STRIP,
    'LEDMatrix': HOST_TYPE.MATRIX,
    'LEDCircle': HOST_TYPE.CIRCLE
}


class BaseReceiver(BaseAnimation):
    def __init__(self, led):
        super(BaseReceiver, self).__init__(led)
        name = type(self._led).__name__
        if name in HOST_MAP:
            self.host_type = HOST_MAP[name]
        else:
            raise ValueError('led must be of type {}'.format(', '.join(HOST_MAP.keys())))

        self._free_run = True
        self._hold_for_data = threading.Event()
        self._stop_event = threading.Event()
        self._stop_event.clear()
        self._recv_thread_obj = None

    def preRun(self, amt=1):
        self._led.all_off()
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
        Instead, receive the data on the recieve thread and set it on the buffer.
        Then call self._hold_for_data.set()
        """
        if not self._stop_event.isSet():
            self._hold_for_data.wait()
            self._hold_for_data.clear()
