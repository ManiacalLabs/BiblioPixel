from .. import log
import contextlib, functools, threading, time, traceback, queue


class Runnable:
    """
    Base class for all objects that contain threads - including threads
    created and started by bp code, and threads started by external libraries.

    There are three possible thread categories for a Runnable:

    1. Runs on the master thread - M
    2. A new thread created by us - N
    3. A new external thread created by some third-party code - X

    Case X is tricky because we would like our code to be called at the start of
    the new thread, and again at the end of that thread, but we can't.

    Lifecycle - what a Runnable does, and what threads it could be called on

    * construction: M
    * start: M
    * on_start: M
      * called on the master thread after any new thread has started up
    * run: MN
    * callbacks: MNX
    * join: M
    * cleanup: M(N?)

    TODO: right now we run all our cleanups on the new thread, if there is a new
    thread, otherwise on the master thread.  Should we move to doing all the
    cleanups on the master thread?

    The way to use a Runnable is like a context manager:

    with some_runnable() as runnable:
         add_some_callbacks(runnable)
         more_stuff_that_runs_on_start()

         # Depending on the thread category, the `Runnable` isn't guaranteed to
         # actually "go off" until the end of this block.

    We're going to call the code inside the context manager `on_start`

    """

    MASTER, NEW, EXTERNAL = 'M', 'N', 'X'
    category = NEW

    timeout = 0.1
    running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def cleanup(self):
        pass

    def join(self, timeout=None):
        """Join this thread, or timeout in `timeout` seconds"""

    def wait(self, timeout=None):
        """Wait until this runnable has started, or time out."""

    def is_alive(self):
        return self.running

    def run(self):
        try:
            self.target()
        except:
            log.error('Exception at %s: \n%s',
                      str(self), traceback.format_exc())
        finally:
            self.cleanup()

    def target(self):
        """The target code that is actually executed in the run method"""
        pass

    @contextlib.contextmanager
    def joiner(self, stop=True):
        self.start()

        try:
            yield self
        finally:
            stop and self.stop()

        while self.is_alive():
            try:
                self.join(self.timeout)
            except Exception as e:
                log.error('Unable to join thread %s: %s', self, e)
                return


class RunnableThread(threading.Thread, Runnable):
    def __init__(self, daemon=True, **kwds):
        super().__init__(daemon=daemon, **kwds)
        self.event = threading.Event()

    def start(self):
        Runnable.start(self)
        threading.Thread.start(self)

    def wait(self, timeout=None):
        self.event.wait(timeout)

    def run(self):
        self.event.set()
        Runnable.run(self)


class Loop(RunnableThread):
    def __init__(self, loop_once=None, **kwds):
        super().__init__(**kwds)
        self.loop_once = loop_once or self.loop_once

    def target(self):
        while self.running:
            self.loop_once()

    def loop_once(self):
        raise NotImplementedError


class RunnableCollection(Runnable):
    def __init__(self, runnables):
        self.runnables = tuple(runnables)

    def start(self):
        for r in self.runnables:
            r.start()

    def stop(self):
        for r in self.runnables:
            r.stop()

    def join(self, timeout=None):
        for r in self.runnables:
            r.join(timeout)

    def wait(self, timeout=None):
        for r in self.runnables:
            r.wait(timeout)

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

    def loop_once(self):
        try:
            msg = self.queue.get(timeout=self.timeout)
        except queue.Empty:
            pass
        else:
            self.send(msg)

    def send(self, msg):
        pass
