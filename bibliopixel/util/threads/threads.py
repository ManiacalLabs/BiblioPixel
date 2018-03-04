import functools, threading, queue


class Loop(threading.Thread):
    def __init__(self, loop=None, daemon=True, **kwds):
        super().__init__(daemon=daemon, **kwds)
        self.running = True
        self.loop = loop or self.loop

    def run(self):
        while self.running:
            self.loop()

    def stop(self):
        self.running = False

    def loop(self):
        pass


class Loops(object):
    def __init__(self, loops):
        self.loops = list(loops)

    def start(self):
        map(lambda x: x.start(), self.loops)

    def stop(self):
        map(lambda x: x.stop(), self.loops)


class QueueHandler(Loop):
    def __init__(self, timeout=0.1, send=None, **kwds):
        super().__init__(**kwds)
        self.timeout = timeout
        self.queue = queue.Queue
        self.send = send or self.send

    def loop(self):
        try:
            msg = self.queue.get(timeout=self.timeout)
        except queue.Empty:
            pass
        else:
            self.send(msg)

    def send(self, msg):
        pass
