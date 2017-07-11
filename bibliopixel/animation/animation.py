import contextlib, threading, time
from . runner import Runner
from .. import log
from .. threads.animation_threading import AnimationThreading
from enum import IntEnum


class COMPLETE_REASON(IntEnum):
    NONE = 0
    CANCELED = 1
    MAX_STEPS = 2
    SELF_COMPLETE = 3


class BaseAnimation(object):
    free_run = False

    def __init__(self, layout):
        self.layout = layout
        self.internal_delay = None
        self.__complete_callback = None
        self.complete_reason = COMPLETE_REASON.NONE

    @property
    def _led(self):
        """Many BiblioPixelAnimations use the "protected" variable _led."""
        return self.layout

    @_led.setter
    def _led(self, layout):
        self.layout = layout

    def preRun(self, amt=1):
        self.layout.all_off()

    @property
    def complete_callback(self):
        return self.__complete_callback

    @complete_callback.setter
    def complete_callback(self, callback):
        if not callable(callback):
            raise ValueError('complete_callback must be a function!')

        self.__complete_callback = callback

    def step(self, amt=1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def cleanup(self, clean_layout=True):
        # if current thread is animation thread this was called
        # by the context manager and thread is therefore already stopped
        if self.threading.thread != threading.current_thread():
            self.threading.stop_thread(wait=True)
        # Some cases we may not want to clear the screen
        # Like with the remote, it would flash between anims
        if clean_layout:
            self.layout.cleanup()

    def is_running(self):
        if self.threading.stop_event.isSet():
            self.complete_reason = COMPLETE_REASON.CANCELED
            return False

        if self.runner.max_steps and not (self.cur_step < self.runner.max_steps):
            self.complete_reason = COMPLETE_REASON.MAX_STEPS
            return False

        if (self.runner.until_complete and self.completed):
            self.complete_reason = COMPLETE_REASON.SELF_COMPLETE
            return False

        return True

    def run_one_frame(self):
        timestamps = []

        def stamp():
            timestamps.append(time.time())

        stamp()

        self.step(self.runner.amt)

        stamp()

        self.layout.frame_render_time = timestamps[1] - timestamps[0]
        self.layout.push_to_driver()

        stamp()

        _report_framerate(timestamps)

        self.cur_step += 1
        if self.completed and self.runner.max_cycles > 0:
            if self.cycle_count < self.runner.max_cycles - 1:
                self.cycle_count += 1
                self.completed = False

        stamp()

        self.threading.wait(self.sleep_time, timestamps)

    @contextlib.contextmanager
    def run_context(self):
        self.completed = False
        self.complete_reason = COMPLETE_REASON.NONE
        self._step = 0
        self.cur_step = 0
        self.cycle_count = 0

        if self.free_run:
            self.sleep_time = None
        elif self.internal_delay:
            self.sleep_time = self.internal_delay
        else:
            self.sleep_time = self.runner.sleep_time
        self.layout.animation_sleep_time = self.sleep_time or 0

        self.preRun(self.runner.amt)
        try:
            yield
        finally:
            self.cleanup()

        if self.__complete_callback:
            self.__complete_callback(self.complete_reason)

    def run_all_frames(self):
        with self.run_context():
            while self.is_running():
                self.run_one_frame()

    def set_runner(self, runner):
        self.runner = runner
        self.threading = AnimationThreading(self.runner, self.run_all_frames)

    def start(self):
        self.threading.start()

    def run(self, **kwds):
        # DEPRECATED
        self.set_runner(Runner(**kwds))
        self.start()


def _report_framerate(timestamps):
    total_time = timestamps[-1] - timestamps[0]
    fps = int(1.0 / max(total_time, 0.001))
    log.debug("%dms/%dfps / Frame: %dms / Update: %dms",
              1000 * total_time,
              fps,
              1000 * (timestamps[1] - timestamps[0]),
              1000 * (timestamps[2] - timestamps[1]))
