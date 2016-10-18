import contextlib, threading

"""
Typical usage would look like this.

In the "write thread":

    while write_thread_is_running():
        with double_buffer.produce() as input:
           # mutate input buffer

In a separate "read thread"

    while read_thread_is_running():
        with double_buffer.consume() as output:
           # read output buffer

"""


class DoubleBuffer(object):
    def __init__(self, front, back):
        self._front = front
        self._back = back

        self._ready = threading.Event()
        self._consumed = threading.Event()
        self._consumed.set()

    @contextlib.contextmanager
    def produce(self):
        """Swap a full buffer in front for an empty one in back."""
        self._consumed.wait()
        self._consumed.clear()

        yield self._front
        self._front, self._back = self._back, self._front

        self._ready.set()

    @contextlib.contextmanager
    def consume(self):
        self._ready.wait()
        self._ready.clear()

        yield self._back
        self._consumed.set()
