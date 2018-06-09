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

    def __init__(self):
        self.run_event = threading.Event()
        self.stop_event = threading.Event()

    @property
    def running(self):
        """
        Is this Runnable expected to make any progress from here?

        The Runnable might still execute a little code after it has stopped
        running.
        """
        return self.run_event.is_set() and not self.stop_event.is_set()

    def is_alive(self):
        """
        Is this Runnable still executing code?

        In some cases, such as threads, self.is_alive() might be true for some
        time after self.running has turned False.
        """
        return self.running

    def start(self):
        self.run_event.set()

    def stop(self):
        self.stop_event.set()

    def wait(self):
        self.stop_event.wait()

    def cleanup(self):
        """
        Cleans up resources after the Runnable.

        self.cleanup() may not throw an exception.
        """

    def run(self):
        try:
            while self.running:
                self.run_once()
        except:
            log.error('Exception at %s: \n%s',
                      str(self), traceback.format_exc())
        finally:
            self.stop()
            self.cleanup()

    def run_once(self):
        """The target code that is repeatedly executed in the run method"""
        pass

    @contextlib.contextmanager
    def run_until_stop(self):
        """
        A context manager that starts this Runnable, yields,
        and then waits for it to finish."""
        self.start()
        try:
            yield self
        finally:
            self.stop()
        self.wait()


class LoopThread(Runnable):
    def __init__(self, daemon=True, **kwds):
        super().__init__()
        self.thread = threading.Thread(daemon=daemon, target=self.run, **kwds)

    def start(self):
        self.thread.start()

    def run(self):
        super().start()
        super().run()

    def is_alive(self):
        return self.thread.is_alive()


class QueueHandler(LoopThread):
    def __init__(self, timeout=0.1, send=None, **kwds):
        super().__init__(**kwds)
        self.timeout = timeout
        self.queue = queue.Queue()
        self.send = send or self.send

    def run_once(self):
        try:
            msg = self.queue.get(timeout=self.timeout)
        except queue.Empty:
            pass
        else:
            self.send(msg)

    def send(self, msg):
        pass
