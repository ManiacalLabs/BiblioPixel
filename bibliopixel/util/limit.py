class Limit:
    def __init__(self, ratio=1, knee=0, gain=1, enable=True):
        """
        :param float ratio: the compression ratio (1 means no compression).
            ratio should usually between 0 and 1.

        :param float knee: the ratio where the compression starts to kick in.
            knee should usually be 0 <= knee <= ratio

        :param float gain: post limiter output gain. gain should usually be >= 0
        """
        # ratio and knee are properties, because we need to recompute _scale
        self.ratio = ratio
        self.knee = knee
        self.gain = gain
        self.enable = enable

    def __bool__(self):
        return self.enable and (self.gain != 1 or self.ratio < 1)

    def limit(self, value):
        if not (self.enable or self):
            return value

        overshoot = value - self.knee
        if overshoot >= 0:
            scale = (self.ratio - self.knee) / (1 - self.knee or 1)
            value = self.knee + overshoot * scale

        value = min(value, self.ratio)
        return value * self.gain

    def limit_colors(self, colors, math):
        if self:
            total = math.sum(colors)
            max_total = 3 * 255 * len(colors)
            average = total / max_total
            limit = self.limit(average) / average
            math.scale(colors, limit)
