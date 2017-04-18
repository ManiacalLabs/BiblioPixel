import threading, time
from .runner import Runner
from .. import log
from .. threads.animation_threading import AnimationThreading


class BaseAnimation(object):
    free_run = False

    def __init__(self, led):
        self._led = led
        self.animComplete = False
        self._step = 0
        self._timeRef = 0
        self._internalDelay = None

    def _msTime(self):
        return time.time()

    def preRun(self, amt=1):
        self._led.all_off()

    def step(self, amt=1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def cleanup(self):
        self.threading.stop_thread(wait=True)
        self._led.cleanup()

    def _is_running(self, cur_step, runner):
        if self.threading.stop_event.isSet():
            return False

        if runner.max_steps:
            return cur_step < runner.max_steps

        return not (runner.until_complete and self.animComplete)

    def _run(self, runner):
        if self.free_run:
            sleep_time = None
        elif self._internalDelay:
            sleep_time = self._internalDelay
        else:
            sleep_time = runner.sleep_time

        self.preRun(runner.amt)

        self._step = 0
        cur_step = 0
        cycle_count = 0
        self.animComplete = False

        while self._is_running(cur_step, runner):
            self._timeRef = self._msTime()

            start = self._msTime()
            self.step(runner.amt)
            mid = self._msTime()

            self._led.frame_render_time = int(mid - start)
            self._led.animation_sleep_time = sleep_time or 0

            self._led.push_to_driver()
            now = self._msTime()

            if self.animComplete and runner.max_cycles > 0:
                if cycle_count < runner.max_cycles - 1:
                    cycle_count += 1
                    self.animComplete = False

            self.threading.report_framerate(start, mid, now)

            if sleep_time:
                diff = (self._msTime() - self._timeRef)
                t = max(0, sleep_time - diff)
                if t == 0:
                    log.warning('Frame-time of %dms set, but took %dms!',
                                sleep_time, diff)
                self.threading.wait(t)
            cur_step += 1

    def run(self, **kwds):
        self.runner = Runner(**kwds)

        def run():
            try:
                self._run(self.runner)
            finally:
                self.cleanup()

        self.threading = AnimationThreading(self.runner)
        self.threading.run_animation(run)
