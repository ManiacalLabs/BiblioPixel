import threading

from . import compose_events


class UpdateDriverThread(threading.Thread):

    def __init__(self, driver):
        super(UpdateDriverThread, self).__init__()
        self.setDaemon(True)
        self._stop = threading.Event()
        self._wait = threading.Event()
        self._updating = threading.Event()
        self._reading = threading.Event()
        self._reading.set()
        self._data = []
        self._driver = driver

    def update_colors(self):
        self._reading.wait()
        self._reading.clear()
        self._wait.set()

    def sync(self):
        self._updating.wait()
        self._driver.sync()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def sending(self):
        return self._wait.isSet()

    def run(self):
        while not self.stopped():
            self._wait.wait()
            self._updating.clear()
            self._driver.update_colors()
            self._data = []
            self._wait.clear()
            self._reading.set()
            self._updating.set()


class UpdateThread(threading.Thread):

    def __init__(self, drivers):
        super(UpdateThread, self).__init__()
        self.setDaemon(True)
        self._stop = threading.Event()
        self._wait = threading.Event()
        self._reading = threading.Event()
        self._reading.set()
        self._data = []
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

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            self._wait.wait()

            # while all([d._thread.sending() for d in self._drivers]):
            #     time.sleep(0.00000000001)

            self._updated.wait()
            # for d in self._drivers:
            #     d._thread._updating.wait()

            for d in self._drivers:
                d._thread.sync()

            self._updated.clear()

            self._data = []
            self._wait.clear()
            self._reading.set()
