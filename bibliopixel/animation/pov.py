from . wrapper import Wrapper
from .. layout import matrix

# Takes a matrix animation and displays it as individual columns or rows over
# time on a Strip


class POV(Wrapper):
    def __init__(self, *args, is_vertical=True, serpentine=False, **kwds):
        super().__init__(*args, **kwds)
        w, h = self.animation.width, self.animation.height
        color_list = self.layout.maker.color_list(w * h)
        self.animation.layout = matrix.Matrix(
            self.layout.drivers, w, h,
            serpentine=serpentine, color_list=color_list)
        self.get = self.animation.layout.get

        # Is the display strip oriented vertically?
        self.is_vertical = is_vertical

        # self.actual is the number of actual pixels in the strip
        # self.subframes is the number of virtual subframes
        actual, self.subframes = (w, h) if is_vertical else (h, w)

        if actual != self.layout.numLEDs:
            dim = ('vertical', 'horizontal')[is_vertical]
            raise ValueError('%s dimension is %d but should match shape=%d' %
                             (dim, actual, self.layout.numLEDs))

    def step(self, amt=1):
        substep = self.cur_step % self.subframes
        if not substep:
            super().step()

        for i in range(self.layout.numLEDs):
            x, y = (substep, i) if self.is_vertical else (i, substep)
            self.layout.set(i, self.get(x, y))
