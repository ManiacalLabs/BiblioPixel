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
        self.frame_overrun = False

    def stop_thread(self, wait=False):
        # run regardless of threaded, used to stop sequences
        self.stop_event.set()
        if self.thread and wait:
            self.thread.join()

    def stopped(self):
        return not (self.thread and self.thread.isAlive())

    def target(self):
        # TODO: no testpath exercises this code...
        log.debug('Starting thread...')
        self.run()
        log.debug('Thread Complete')

    def wait(self, wait_time, timestamps):
        if not wait_time:
            return

        elapsed_time = timestamps[-1] - timestamps[0]
        if elapsed_time > wait_time:
            logger = log.debug if self.frame_overrun else log.warning
            logger('Frame-time of %dms set, but took %dms!',
                   1000 * wait_time, 1000 * elapsed_time)
            self.frame_overrun = True

        elif self.runner.threaded:
            self.stop_event.wait(wait_time - elapsed_time)

        else:
            time.sleep(wait_time - elapsed_time)

    def start(self):
        self.stop_event.clear()

        if not self.runner.threaded:
            self.run()
            return

        self.thread = threading.Thread(target=self.target, daemon=True)
        self.thread.start()

        if self.runner.join_thread:
            # TODO: why would you do this rather than disable threading?
            self.thread.join()
