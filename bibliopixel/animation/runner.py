import time
from enum import IntEnum
from .. util import log
from .. project import attributes, load

DEFAULT_FPS = 24


class STATE(IntEnum):
    ready = 0
    running = 1
    complete = 2
    canceled = 3
    max_steps = 4
    timeout = 5


class Runner(object):

    def __init__(self, *, amt=1, fps=0, sleep_time=0, max_steps=0,
                 until_complete=False, max_cycles=0, seconds=None,
                 threaded=False, main=None, flat_out=False,
                 repeats=None, **kwds):
        attributes.check(kwds, 'run')

        if max_steps < 0:
            log.error('max_steps %s < 0', max_steps)
            max_steps = 0
        if sleep_time < 0:
            log.error('sleep_time %s < 0', sleep_time)
            sleep_time = 0
        if max_cycles < 0:
            log.error('max_cycles %s < 0', max_cycles)
            max_cycles = 0
        if fps < 0:
            log.error('fps %s < 0', fps)
            fps = 0
        if repeats and repeats < 0:
            log.error('repeats %s < 0', repeats)
            repeats = None

        if sleep_time and fps:
            log.error('sleep_time=%s and fps=%s cannot both be set',
                      sleep_time, fps)
            sleep_time = 0
        if seconds and max_steps:
            log.error('seconds=%s and max_steps=%s cannot both be set',
                      seconds, max_steps)
            max_steps = 0

        self.amt = amt

        if fps:
            self.sleep_time = 1 / fps
        elif sleep_time:
            self.sleep_time = sleep_time
        else:
            self.sleep_time = 1 / DEFAULT_FPS

        self.until_complete = until_complete
        self.seconds = seconds
        self.run_start_time = 0
        self.max_steps = max_steps
        self.max_cycles = max_cycles
        self.seconds = seconds
        self.threaded = threaded
        self.flat_out = flat_out
        self.main = load.code(main)
        if repeats is not None:
            self.until_complete = True
            self.max_cycles = repeats
        self.repeats = repeats

    def set_project(self, project):
        self.project = project
        if self.flat_out:
            project.flat_out()

    @property
    def fps(self):
        return 1 / self.sleep_time

    @fps.setter
    def fps(self, fps):
        self.sleep_time = 1 / fps

    def compute_state(self, cur_step, state):
        if self.seconds:
            elapsed = self.project.time() - self.run_start_time
            if elapsed >= self.seconds:
                return STATE.timeout

        elif self.max_steps:
            if cur_step >= self.max_steps:
                return STATE.max_steps

        elif not self.until_complete:
            if state == STATE.complete:
                # Ignore STATE.complete if until_complete is False
                return STATE.running

        return state
