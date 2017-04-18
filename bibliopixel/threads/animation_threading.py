import threading, time
from .. import log


class AnimationThreading(object):
    """
    AnimationThreading handles threading - and eventually multiprocessing - for
    BaseAnimation.
    """

    def __init__(self, runner):
        self.runner = runner
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

    def wait(self, t):
        if self.runner.threaded:
            self.stop_event.wait(t)
        else:
            time.sleep(t)

    def run_animation(self, run):
        if not self.runner.threaded:
            run()
            return

        def target():
            # TODO: no testpath exercises this code...
            log.debug('Starting thread...')
            run()
            log.debug('Thread Complete')

        self.stop_event.clear()

        self.thread = threading.Thread(target=target, daemon=True)
        self.thread.start()

        if self.runner.join_thread:
            # TODO: why would you do this rather than disable threading?
            self.thread.join()
