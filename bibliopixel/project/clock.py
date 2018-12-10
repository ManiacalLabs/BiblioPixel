import time


class Clock:
    def __init__(self, is_flat_out=False):
        self.is_flat_out = is_flat_out
        self._time = time.time()

    def time(self):
        return self._time if self.is_flat_out else time.time()

    def sleep(self, delta_time):
        delta_time = max(delta_time, 0)
        # TODO: why is delta_time occasionally tiny and negative?
        if not self.is_flat_out:
            time.sleep(delta_time)
        else:
            self._time += delta_time
