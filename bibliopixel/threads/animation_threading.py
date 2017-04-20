import threading, time
from .. import log


class AnimationThreading(object):
    """
    AnimationThreading handles threading - and eventually multiprocessing - for
    BaseAnimation.
    """

    def __init__(self, runner, run):
        self.runner = runner
        self.run = run
        self.stop_event = threading.Event()
        self.thread = None

    def report_framerate(self, timestamps):
        total_time = timestamps[-1] - timestamps[0]
        fps = int(1.0 / max(total_time, 0.001))
        log.debug("%dms/%dfps / Frame: %dms / Update: %dms",
                  1000 * total_time,
                  fps,
                  1000 * (timestamps[1] - timestamps[0]),
                  1000 * (timestamps[2] - timestamps[1]))

    def stop_thread(self, wait=False):
        if self.thread:
            self.stop_event.set()
            if wait:
                self.thread.join()

    def stopped(self):
        return not (self.thread and self.thread.isAlive())

    def target(self):
        # TODO: no testpath exercises this code...
        log.debug('Starting thread...')
        self.run()
        log.debug('Thread Complete')

    def wait(self, t):
        if self.runner.threaded:
            self.stop_event.wait(t)
        else:
            time.sleep(t)

    def start(self):
        if not self.runner.threaded:
            self.run()
            return

        self.stop_event.clear()

        self.thread = threading.Thread(target=self.target, daemon=True)
        self.thread.start()

        if self.runner.join_thread:
            # TODO: why would you do this rather than disable threading?
            self.thread.join()
