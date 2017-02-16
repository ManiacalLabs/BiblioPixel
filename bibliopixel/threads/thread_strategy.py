import threading, time

from .. import log
from . import update_thread


class ThreadStrategy(object):
    """
    ThreadStrategy handles threading - and eventually multiprocessing - for
    BaseAnimation and LEDBase.
    """

    def __init__(self, use_update_thread, led):
        self.use_update_thread = use_update_thread
        self.use_animation_thread = False
        self.led = led
        self.animation_thread = None
        self.animation_stop_event = threading.Event()

        if use_update_thread:
            self.update_thread = update_thread.UpdateThread(led.drivers)
            self.update_thread.start()

    def update_colors(self):
        if self.use_update_thread:
            self.update_thread.update_colors()
        else:
            for d in self.led.drivers:
                d.update_colors()
            for d in self.led.drivers:
                d.sync()

    def wait_for_update(self):
        if self.use_update_thread:
            while all([d._thread.sending() for d in self.led.drivers]):
                time.sleep(0.000001)

    def push_to_driver(self):
        """Push the current pixel state to the driver"""
        self.wait_for_update()
        self.update_colors()

    def set_animation(self, animation):
        self.animation = animation

    def report_framerate(self, start, mid, now):
        stepTime = int(mid - start)
        render_duration = int(now - mid)
        totalTime = stepTime + render_duration
        fps = int(1000.0 / max(totalTime, 1))
        log.debug("%sms/%sfps / Frame: %sms / Update: %sms",
                  totalTime, fps, stepTime, render_duration)

    def stop_animation_thread(self, wait=False):
        if self.animation_thread:
            self.animation_stop_event.set()

            if wait:
                self.animation_thread.join()

    def animation_stopped(self):
        return not (self.animation_thread and self.animation_thread.isAlive())

    def animation_wait(self, t):
        if self.use_animation_thread:
            self.animation_stop_event.wait(t)
        else:
            time.sleep(t)

    def run_animation(self, run, threaded, join_thread):
        self.use_animation_thread = threaded
        if self.use_animation_thread:
            self.animation_stop_event.clear()

            def target():
                # TODO: no testpath exercises this code...
                log.debug('Starting thread...')
                run()
                log.debug('Thread Complete')

            self.animation_thread = threading.Thread(target=target, daemon=True)
            self.animation_thread.start()
            if join_thread:
                self.animation_thread.join()
        else:
            run()
