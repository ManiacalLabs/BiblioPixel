import time
from enum import IntEnum
from .. util import log
from .. project import attributes, load


class STATE(IntEnum):
    ready = 0
    running = 1
    complete = 2
    canceled = 3
    max_steps = 4
    timeout = 5


class Runner(object):

    def __init__(self, *, amt=1, fps=None, sleep_time=0, max_steps=0,
                 until_complete=False, max_cycles=0, seconds=None,
                 threaded=False, main=None, **kwds):
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

        if sleep_time and fps:
            log.error('sleep_time=%s and fps=%s cannot both be set',
                      sleep_time, fps)
            sleep_time = 0
        if seconds and max_steps:
            log.error('seconds=%s and max_steps=%s cannot both be set',
                      seconds, max_steps)
            max_steps = 0

        self.amt = amt
        self.sleep_time = 1 / fps if fps else sleep_time
        self.until_complete = until_complete
        self.seconds = seconds
        self.run_start_time = 0
        self.max_steps = max_steps
        self.max_cycles = max_cycles
        self.seconds = seconds
        self.threaded = threaded
        self.main = load.code(main)

    @property
    def fps(self):
        return 1 / self.sleep_time

    @fps.setter
    def fps(self, fps):
        self.sleep_time = 1 / fps

    def compute_state(self, cur_step, state):
        if self.seconds:
            elapsed = time.time() - self.run_start_time
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
