import loady
from .. util import log
from .. project import project


class Runner(object):

    def __init__(self, amt=1, fps=None, sleep_time=0, max_steps=0,
                 until_complete=False, max_cycles=0, seconds=None,
                 threaded=False, main=None, **kwds):
        project.raise_if_unknown(kwds, 'attribute', 'run')

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
        self.fps = fps
        self.sleep_time = 1 / fps if fps else sleep_time
        self.until_complete = until_complete
        self.seconds = seconds
        self.run_start_time = 0
        self.max_steps = max_steps
        self.max_cycles = max_cycles
        self.seconds = seconds
        self.threaded = threaded
        self.main = main and loady.code.load(main)
