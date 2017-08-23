import contextlib, threading, time
from . runner import Runner
from .. util import log
from .. threads.animation_threading import AnimationThreading
from .. project import project
from enum import IntEnum


class STATE(IntEnum):
    ready = 0
    running = 1
    complete = 2
    canceled = 3
    max_steps = 4
    timeout = 5


class BaseAnimation(object):
    free_run = False
    name = None
    data = None

    def __init__(self, layout, **kwds):
        project.raise_if_unknown_attributes(kwds, 'animation', self)
        self.layout = layout
        self.internal_delay = None
        self.on_completion = None
        self.state = STATE.ready

    @property
    def _led(self):
        """Many BiblioPixelAnimations use the "protected" variable _led."""
        return self.layout

    @_led.setter
    def _led(self, layout):
        self.layout = layout

    @property
    def completed(self):
        """Many BiblioPixelAnimations use the old `completed` variable."""
        return self.state == STATE.complete

    @completed.setter
    def completed(self, state):
        if state:
            self.state = STATE.complete
        else:
            self.state = STATE.running

    def pre_run(self):
        pass

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

    def compute_state(self):
        if self.threading.stop_event.isSet():
            self.state = STATE.canceled
        elif self.runner.seconds and (time.time() - self.runner.run_start_time) > self.runner.seconds:
            self.state = STATE.timeout
        elif self.runner.max_steps and not (self.cur_step < self.runner.max_steps):
            self.state = STATE.max_steps
        elif (not self.runner.until_complete and self.state == STATE.complete):
            # Ignore STATE.complete if until_complete is False
            self.state = STATE.running

    def check_delay(self):
        if self.free_run:
            self.sleep_time = None
        elif self.internal_delay:
            self.sleep_time = self.internal_delay
        else:
            self.sleep_time = self.runner.sleep_time
        self.layout.animation_sleep_time = self.sleep_time or 0

    def run_one_frame(self):
        timestamps = []

        def stamp():
            timestamps.append(time.time())

        self.check_delay()

        stamp()

        self.step(self.runner.amt)

        stamp()

        self.layout.frame_render_time = timestamps[1] - timestamps[0]
        self.layout.push_to_driver()

        stamp()

        _report_framerate(timestamps)

        self.cur_step += 1
        if self.state == STATE.complete and self.runner.max_cycles > 0:
            if self.cycle_count < self.runner.max_cycles - 1:
                self.cycle_count += 1
                self.state = STATE.running

        stamp()

        self.threading.wait(self.sleep_time, timestamps)

        self.compute_state()

    @contextlib.contextmanager
    def run_context(self):
        self.state = STATE.running
        self.runner.run_start_time = time.time()
        self.threading.stop_event.clear()
        self._step = 0
        self.cur_step = 0
        self.cycle_count = 0

        self.check_delay()

        self.pre_run()
        try:
            yield
        finally:
            self.cleanup()

        self.on_completion and self.on_completion(self.state)

        self.state = STATE.ready

    def run_all_frames(self):
        with self.run_context():
            while self.state == STATE.running:
                self.run_one_frame()

    def set_runner(self, runner):
        self.runner = Runner(**(runner or {}))
        self.threading = AnimationThreading(self.runner, self.run_all_frames)

    def start(self):
        self.threading.start()

    def run(self, **kwds):
        # DEPRECATED
        self.set_runner(kwds)
        self.start()


def _report_framerate(timestamps):
    total_time = timestamps[-1] - timestamps[0]
    fps = int(1.0 / max(total_time, 0.001))
    log.debug("%dms/%dfps / Frame: %dms / Update: %dms",
              1000 * total_time,
              fps,
              1000 * (timestamps[1] - timestamps[0]),
              1000 * (timestamps[2] - timestamps[1]))
