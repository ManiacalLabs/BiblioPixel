import statistics


class Segments(list):
    """
    A list of [level, time] pairs.
    """
    def __init__(self, segments=(), length=None):
        super().__init__()
        self.base_value = 0
        for segment in segments:
            try:
                level, time = segment
            except TypeError:
                level, time = segment, None
            self.append([level, time])

        times = [t for s, t in self if t is not None]
        if times:
            mean = sum(times) / len(times)
        else:
            mean = (length or 1) / max(1, len(self))

        for segment in self:
            if segment[1] is None:
                segment[1] = mean

        self.total_time = sum(t for l, t in self)

    def __call__(self, time, base_value=0):
        elapsed_time = 0
        level = base_value
        for l, t in self:
            segment_end_time = elapsed_time + t
            if time < segment_end_time:
                delta_t = time - elapsed_time
                return level + (l - level) * delta_t / t

            elapsed_time = segment_end_time
            level = l

        return level
