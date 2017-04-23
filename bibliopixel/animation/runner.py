class Runner(object):

    def __init__(self, amt=1, fps=None, sleep_time=0, max_steps=0,
                 until_complete=False, max_cycles=0, seconds=None,
                 threaded=False, join_thread=False):
        assert max_steps >= 0
        assert sleep_time >= 0
        assert max_cycles >= 0
        assert not (sleep_time and fps)
        assert not (seconds and max_steps)

        self.amt = amt
        self.fps = fps
        self.sleep_time = 1 / fps if fps else sleep_time
        self.until_complete = until_complete
        if seconds is None:
            self.max_steps = max_steps
        else:
            self.max_steps = int(seconds / self.sleep_time)
        self.max_cycles = max_cycles
        self.seconds = seconds
        self.threaded = threaded
        self.join_thread = join_thread
