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
        self._callback = None
        self._stopEvent = threading.Event()
        self._stopEvent.clear()
        self._free_run = False

    def _msTime(self):
        return time.time() * 1000.0

    def preRun(self, amt=1):
        self._led.all_off()

    def step(self, amt=1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def stopThread(self, wait=False):
        if self.thread_strategy.animation_thread:
            self._stopEvent.set()

            if wait:
                self.thread_strategy.animation_thread.join()

    def cleanup(self):
        self.stopThread(wait=True)
        self._led.all_off()
        self._led.push_to_driver()
        self.thread_strategy.wait_for_update()

    def stopped(self):
        return not (self.thread_strategy.animation_thread and self.thread_strategy.animation_thread.isAlive())

    def _run(self, amt, fps, sleep, max_steps, until_complete,
             max_cycles, seconds):
        self.preRun(amt)

        # calculate sleep time base on desired Frames per Second
        if fps:
            sleep = int(1000 / fps)

        if seconds is not None:
            max_steps = int((seconds * 1000) / sleep)

        initSleep = sleep

        self._step = 0
        cur_step = 0
        cycle_count = 0
        self.animComplete = False

        while (not self._stopEvent.isSet() and
               ((max_steps == 0 and not until_complete) or
                (max_steps > 0 and cur_step < max_steps) or
                (max_steps == 0 and until_complete and not self.animComplete))):

            self._timeRef = self._msTime()

            start = self._msTime()
            if hasattr(self, "_input_dev"):
                self._keys = self._input_dev.getKeys()
            self.step(amt)
            mid = self._msTime()

            if self._free_run:
                sleep = None
            elif self._internalDelay:
                sleep = self._internalDelay
            elif initSleep:
                sleep = initSleep

            self._led._frameGenTime = int(mid - start)
            self._led._frameTotalTime = sleep

            self._led.push_to_driver()
            now = self._msTime()

            if self.animComplete and max_cycles > 0:
                if cycle_count < max_cycles - 1:
                    cycle_count += 1
                    self.animComplete = False

            self.thread_strategy.report_framerate(start, mid, now)

            if sleep:
                diff = (self._msTime() - self._timeRef)
                t = max(0, (sleep - diff) / 1000.0)
                if t == 0:
                    log.warning(
                        "Frame-time of %dms set, but took %dms!", sleep, diff)
                if self.thread_strategy.use_animation_thread:
                    self._stopEvent.wait(t)
                else:
                    time.sleep(t)
            cur_step += 1

        self._callback and self._callback(self)

    def run(self, amt=1, fps=None, sleep=None, max_steps=0, until_complete=False,
            max_cycles=0, threaded=False, joinThread=False, callback=None,
            seconds=None):

        self._callback = callback
        self.thread_strategy.use_animation_thread = threaded
        if self.thread_strategy.use_animation_thread:
            self._stopEvent.clear()
        self._callback = callback

        def run():
            try:
                self._run(amt, fps, sleep, max_steps, until_complete,
                          max_cycles, seconds)
            finally:
                self.cleanup()

        if self.thread_strategy.use_animation_thread:
            def target():
                # TODO: no testpath exercises this code...
                log.debug('Starting thread...')
                run()
                log.debug('Thread Complete')

            self.thread_strategy.animation_thread = threading.Thread(target=target, daemon=True)
            self.thread_strategy.animation_thread.start()
            if joinThread:
                self.thread_strategy.animation_thread.join()
        else:
            run()

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
