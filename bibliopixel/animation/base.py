import threading, time
from .runner import Runner
from .. import log
from .. threads.animation_threading import AnimationThreading


class BaseAnimation(object):
    free_run = False

    def __init__(self, led):
        self._led = led
        self.completed = False
        self._step = 0
        self.start = 0
        self.internal_delay = None

    def _msTime(self):
        return time.time()

    def preRun(self, amt=1):
        self._led.all_off()

    def step(self, amt=1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def cleanup(self):
        self.threading.stop_thread(wait=True)
        self._led.cleanup()

    def _is_running(self):
        if self.threading.stop_event.isSet():
            return False

        if self.runner.max_steps:
            return self.cur_step < self.runner.max_steps

        return not (self.runner.until_complete and self.completed)

    def _run_once(self):
        self.start = self._msTime()
        self.step(self.runner.amt)
        self.mid = self._msTime()

        self._led.frame_render_time = int(self.mid - self.start)
        self._led.animation_sleep_time = self.sleep_time or 0

        self._led.push_to_driver()
        self.now = self._msTime()

        if self.completed and self.runner.max_cycles > 0:
            if self.cycle_count < self.runner.max_cycles - 1:
                self.cycle_count += 1
                self.completed = False

        self.threading.report_framerate(self.start, self.mid, self.now)

        if self.sleep_time:
            diff = (self._msTime() - self.start)
            t = max(0, self.sleep_time - diff)
            if t == 0:
                log.warning('Frame-time of %dms set, but took %dms!',
                            self.sleep_time, diff)
            self.threading.wait(t)
        self.cur_step += 1

    def _run(self):
        try:
            self.preRun(self.runner.amt)
            while self._is_running():
                self._run_once()
        finally:
            self.cleanup()

    def run(self, **kwds):
        self.runner = Runner(**kwds)

        self._step = 0
        self.cur_step = 0
        self.cycle_count = 0
        self.completed = False

        if self.free_run:
            self.sleep_time = None
        elif self.internal_delay:
            self.sleep_time = self.internal_delay
        else:
            self.sleep_time = self.runner.sleep_time

        self.threading = AnimationThreading(self.runner, self._run)
        self.threading.start()
