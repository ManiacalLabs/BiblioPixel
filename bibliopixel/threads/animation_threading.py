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

    def report_framerate(self, start, mid, now):
        stepTime = mid - start
        render_duration = now - mid
        totalTime = stepTime + render_duration
        fps = int(1.0 / max(totalTime, 0.001))
        log.debug("%sms/%sfps / Frame: %sms / Update: %sms",
                  round(1000 * totalTime), fps, round(1000 * stepTime),
                  round(1000 * render_duration))

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
