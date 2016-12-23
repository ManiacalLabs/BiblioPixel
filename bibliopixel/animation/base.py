import threading, time
from .. import log


class BaseAnimation(object):

    def __init__(self, led):
        self._led = led
        self.animComplete = False
        self._step = 0
        self._timeRef = 0
        self._internalDelay = None
        self._thread = None
        self._callback = None
        self._stopEvent = threading.Event()
        self._stopEvent.clear()
        self._led._threadedAnim = False
        self._free_run = False

    def _msTime(self):
        return time.time() * 1000.0

    def preRun(self, amt=1):
        self._led.all_off()

    def step(self, amt=1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def stopThread(self, wait=False):
        if self._thread:
            self._stopEvent.set()

            if wait:
                self._thread.join()

    def __enter__(self):
        # DEPRECATED in favor of self.run_cleanup()
        return self

    def __exit__(self, type, value, traceback):
        # DEPRECATED in favor of self.run_cleanup()
        self.cleanup()

    def cleanup(self):
        self.stopThread(wait=True)
        self._led.all_off()
        self._led.push_to_driver()
        self._led.waitForUpdate()

    def run_cleanup(self, **kwds):
        try:
            self.run(**kwds)
        finally:
            self.cleanup()

    def stopped(self):
        return not (self._thread and self._thread.isAlive())

    def _run(self, amt, fps, sleep, max_steps, until_complete, max_cycles, seconds):
        self.preRun()

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

            stepTime = int(mid - start)
            if self._led._threadedUpdate:
                updateTime = int(self._led.lastThreadedUpdate())
                totalTime = updateTime
            else:
                updateTime = int(now - mid)
                totalTime = stepTime + updateTime

            if self._led._threadedUpdate:
                log.debug(
                    "Frame: %sms / Update Max: %sms", stepTime, updateTime)
            else:
                log.debug("%sms/%sfps / Frame: %sms / Update: %sms",
                          totalTime, int(1000 / max(totalTime, 1)), stepTime,
                          updateTime)

            if sleep:
                diff = (self._msTime() - self._timeRef)
                t = max(0, (sleep - diff) / 1000.0)
                if t == 0:
                    log.warning(
                        "Frame-time of %dms set, but took %dms!", sleep, diff)
                if self._led._threadedAnim:
                    self._stopEvent.wait(t)
                else:
                    time.sleep(t)
            cur_step += 1

        self.cleanup()
        self._callback and self._callback(self)

    def run(self, amt=1, fps=None, sleep=None, max_steps=0, until_complete=False,
            max_cycles=0, threaded=False, joinThread=False, callback=None,
            seconds=None):

        self._callback = callback
        self._led._threadedAnim = threaded
        if self._led._threadedAnim:
            self._stopEvent.clear()
        self._callback = callback

        def do_run():
            self._run(
                amt, fps, sleep, max_steps, until_complete, max_cycles, seconds)

        if self._led._threadedAnim:
            def target():
                # TODO: no testpath exercises this code...
                log.debug('Starting thread...')
                do_run()
                log.debug('Thread Complete')

            self._thread = threading.Thread(target=do_run, daemon=True)
            self._thread.start()
            if joinThread:
                self._thread.join()
        else:
            do_run()

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
