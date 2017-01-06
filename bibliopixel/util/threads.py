import functools, threading


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


class Loops(object):
    def __init__(self, loops):
        self.loops = list(loops)

    def start(self):
        map(lambda x: x.start(), self.loops)

    def stop(self):
        map(lambda x: x.stop(), self.loops)
