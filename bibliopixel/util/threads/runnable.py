from .. import log
import contextlib, functools, threading, traceback, queue


class Runnable:
    """
    Base class for all objects that contain threads - including threads
    created and started by bp code, and threads started by external libraries.

    You can use a Runnable in two ways:  you can call the methods start, stop,
    and join just like for a thread, or you can use it as a context manager:

    with some_runnable() as runnable:
         do_some_things(runnable)

         # At the end of the block, runnable.stop() is called and then
         # the thread is joined

    """

    timeout = 0.1
    running = True

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def join(self):
        """Join this thread, or timeout after self.timeout seconds"""
        pass

    def cleanup(self):
        pass

    def is_alive(self):
        return self.running

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        try:
            self.join()
        except Exception as e:
            log.error('Unable to join thread %s: %s', self, e)


class RunnableTarget(Runnable):
    def run(self):
        try:
            self.target()
        except:
            log.error('Exception at %s: \n%s', str(self), traceback.format_tb())
        finally:
            self.cleanup()

    def target(self):
        """The target code that is actually executed in the run method"""
        pass


class RunnableThread(threading.Thread, RunnableTarget):
    def __init__(self, daemon=True, **kwds):
        super().__init__(daemon=daemon, **kwds)

    def start(self):
        RunnableTarget.start(self)
        threading.Thread.start(self)

    def run(self):
        RunnableTarget.run(self)

    def join(self):
        threading.Thread.join(self, self.timeout)


class Loop(RunnableThread):
    def __init__(self, loop=None, **kwds):
        super().__init__(**kwds)
        self.loop = loop or self.loop

    def target(self):
        while self.running:
            self.loop()

    def loop(self):
        raise NotImplementedError


class Iterable(RunnableThread):
    def __init__(self, iterator=None, **kwds):
        super().__init__(**kwds)
        self.iterator = iterator or self.iterator

    def target(self):
        for i in self.iterator():
            self.receiver(i)
            if not self.running:
                break

    def iterator(self):
        pass


class RunnableCollection(Runnable):
    def __init__(self, runnables):
        self.runnables = tuple(runnables)

    def start(self):
        for r in self.runnables:
            r.start()

    def stop(self):
        for r in self.runnables:
            r.stop()

    def join(self):
        for r in self.runnables:
            r.join()

    def cleanup(self):
        for r in self.runnables:
            r.cleanup()

    def is_alive(self):
        return any(r.is_alive() for r in self.runnables)


class QueueHandler(Loop):
    def __init__(self, timeout=0.1, send=None, **kwds):
        super().__init__(**kwds)
        self.timeout = timeout
        self.queue = queue.Queue()
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
