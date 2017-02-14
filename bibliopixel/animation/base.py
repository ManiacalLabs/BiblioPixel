import threading, time
from .. import log


class BaseAnimation(object):

    def __init__(self, led):
        self._led = led
        self.thread_strategy = led.thread_strategy
        self.thread_strategy.set_animation(self)

        self.animComplete = False
        self._step = 0
        self._timeRef = 0
        self._internalDelay = None
        self._free_run = False

    def _msTime(self):
        return time.time() * 1000.0

    def preRun(self, amt=1):
        self._led.all_off()

    def step(self, amt=1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def cleanup(self):
        self.thread_strategy.stop_animation_thread(wait=True)
        self._led.all_off()
        self._led.push_to_driver()
        self.thread_strategy.wait_for_update()

    def is_running(self, cur_step):
        if self.thread_strategy.animation_stop_event.isSet():
            return False

        if self.max_steps:
            return cur_step < self.max_steps

        return not (self.until_complete and self.animComplete)

    def _run(self):
        self.preRun(self.amt)

        initSleep = self.sleep_time

        self._step = 0
        cur_step = 0
        cycle_count = 0
        self.animComplete = False

        while self.is_running(cur_step):
            self._timeRef = self._msTime()

            start = self._msTime()
            self.step(self.amt)
            mid = self._msTime()

            if self._free_run:
                self.sleep_time = None
            elif self._internalDelay:
                self.sleep_time = self._internalDelay
            elif initSleep:
                self.sleep_time = initSleep

            self._led._frameGenTime = int(mid - start)
            self._led._frameTotalTime = self.sleep_time

            self._led.push_to_driver()
            now = self._msTime()

            if self.animComplete and self.max_cycles > 0:
                if cycle_count < self.max_cycles - 1:
                    cycle_count += 1
                    self.animComplete = False

            self.thread_strategy.report_framerate(start, mid, now)

            if self.sleep_time:
                diff = (self._msTime() - self._timeRef)
                t = max(0, (self.sleep_time - diff) / 1000.0)
                if t == 0:
                    log.warning(
                        "Frame-time of %dms set, but took %dms!", self.sleep_time, diff)
                self.thread_strategy.animation_wait(t)
            cur_step += 1

    def set_run(self, amt=1, fps=None, sleep_time=0, max_steps=0,
                until_complete=False, max_cycles=0, threaded=False,
                join_thread=False, seconds=None):
        assert max_steps >= 0
        assert sleep_time >= 0
        assert max_cycles >= 0

        self.amt = amt
        self.sleep_time = sleep_time
        self.max_steps = max_steps
        self.until_complete = until_complete
        self.max_cycles = max_cycles
        self.threaded = threaded
        self.join_thread = join_thread

        # calculate sleep time base on desired Frames per Second
        assert not (sleep_time and fps)
        if fps:
            self.sleep_time = int(1000.0 / fps)

        assert not (seconds and max_steps)
        if seconds is not None:
            self.max_steps = int((seconds * 1000.0) / self.sleep_time)

    def run(self, **kwds):
        self.set_run(**kwds)

        def run():
            try:
                self._run()
            finally:
                self.cleanup()

        self.thread_strategy.run_animation(run, self.threaded, self.join_thread)

    RUN_PARAMS = [{
        "id": "amt",
        "label": "Step Amount",
        "type": "int",
                "min": 1,
                "default": 1,
                "help": ("Amount to step animation by on each frame: "
                         "perhaps ignored by some animation classes.")
    }, {
        "id": "fps",
        "label": "Framerate",
        "type": "int",
                "default": 30,
                "min": 1,
                "help": "Framerate at which to run animation."
    }, {
        "id": "seconds",
        "label": "Run Seconds",
        "type": "int",
                "default": None,
                "min": 0,
                "help": "Number of seconds to run animation."
    }, {
        "id": "max_steps",
        "label": "Max Frames",
        "type": "int",
                "min": 0,
                "default": 0,
                "help": "Total frames to run before stopping."
    }, {
        "id": "until_complete",
        "label": "Until Complete",
        "type": "bool",
                "default": False,
                "help": "Run until animation marks itself as complete."
    }, {
        "id": "max_cycles",
        "label": "Max Cycles",
        "type": "int",
                "min": 1,
                "default": 1,
                "help": ("If Until Complete is set, animation will repeat "
                         "this many times.")
    }, ]
