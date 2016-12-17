import threading

from . import compose_events, task_thread


class UpdateDriverThread(task_thread.LoopThread):

    def __init__(self, driver):
        super().__init__()
        self.setDaemon(True)
        self._wait = threading.Event()
        self._reading = threading.Event()
        self._reading.set()
        self._updating = threading.Event()
        self._driver = driver

    def update_colors(self):
        self._reading.wait()
        self._reading.clear()
        self._wait.set()

    def sync(self):
        self._updating.wait()
        self._driver.sync()

    def sending(self):
        return self._wait.isSet()

    def _loop(self):
        self._wait.wait()
        self._updating.clear()
        self._driver.update_colors()
        self._wait.clear()
        self._reading.set()
        self._updating.set()


class UpdateThread(task_thread.LoopThread):

    def __init__(self, drivers):
        super().__init__()
        self.setDaemon(True)
        self._wait = threading.Event()
        self._reading = threading.Event()
        self._reading.set()
        self._drivers = drivers
        for d in self._drivers:
            t = UpdateDriverThread(d)
            t.start()
            d._thread = t

        events = (d._thread._updating for d in self._drivers)
        self._updated = compose_events.compose_events(events)

    def update_colors(self):
        self._reading.wait()
        for d in self._drivers:
            d._thread.update_colors()
        self._reading.clear()
        self._wait.set()

    def _loop(self):
        self._wait.wait()
        self._updated.wait()

        for d in self._drivers:
            d._thread.sync()

        self._updated.clear()
        self._wait.clear()
        self._reading.set()
