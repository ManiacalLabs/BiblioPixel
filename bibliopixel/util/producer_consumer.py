import contextlib, queue

"""
Typical usage would look like this.

In the "write thread":

    while write_thread_is_running():
        with double_queue.produce() as input:
           # mutate input queue

In a separate "read thread"

    while read_thread_is_running():
        with double_queue.consume() as output:
           # read output queue

"""


class Queues(object):
    def __init__(self, item, *items):
        self.empty = queue.Queue()
        self.full = queue.Queue()
        self.empty.put(item)
        for i in items:
            self.empty.put(i)

    @contextlib.contextmanager
    def produce(self):
        i = self.empty.get()
        yield i
        self.full.put(i)

    @contextlib.contextmanager
    def consume(self):
        i = self.full.get()
        yield i
        self.empty.put(i)
