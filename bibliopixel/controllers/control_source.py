import threading
from . import extractor


class ControlSource():
    """
    A ControlSource sends messages to a callback.

    Usage:

        source = MyControlSource(callback)
        source.start()

        # callback gets periodically called in another thread with messages.

        source.stop()
    """

    def __init__(self, callback):
        self._callback = callback

    def start(self):
        self.thread = self._make_thread()
        self.thread.start()

    def stop(self):
        self.thread.stop()

    def callback(self, msg):
        self._callback(msg)

    def _make_thread(self):
        return threading.Thread(target=self.loop, daemon=True)

    def loop(self):
        for msg in self:
            self.callback(msg)

    def __iter__(self):
        raise NotImplementedError


class ExtractedSource(ControlSource):
    """
    ExtractedSource is a ControlSource whose messages are passed through an
    Extractor.
    """

    KEYS_BY_TYPE = {}
    NORMALIZERS = {}

    def __init__(self, callback, **kwds):
        """
        Arguments
        kwds -- keyword options passed to the  constructor of Extractor.
        """
        super().__init__(callback)
        self.extractor = extractor.Extractor(
            normalizers=self.NORMALIZERS,
            keys_by_type=self.KEYS_BY_TYPE,
            **kwds)

    def callback(self, msg):
        for m in self.extractor.extract(msg):
            self._callback(m)
