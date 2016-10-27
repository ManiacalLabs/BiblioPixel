import collections, threading


class LoopThread(threading.Thread):
    def __init__(self, loop=None, **kwds):
        super().__init__(**kwds)
        self.running = True
        self._loop = loop or self._loop

    def run(self):
        while self.running:
            self._loop()

    def stop(self):
        self.running = False


class Task(object):
    def __init__(self, task=None, event=None):
        self.task = task or (lambda: None)
        self.event = event or threading.Event()

    def run(self, next_task):
        """Wait for the event, run the task, trigger the next task."""
        self.event.wait()
        self.task()
        self.event.clear()

        next_task.event.set()


class TaskThread(LoopThread):
    def __init__(self, producer_task, consumer_task, daemon=True, **kwds):
        super().__init__(daemon=daemon, **kwds)
        self.producer_task = producer_task
        self.consumer_task = consumer_task

    def produce(self):
        self.producer_task.run(self.consumer_task)

    def _loop(self):
        self.consumer_task.run(self.producer_task)
