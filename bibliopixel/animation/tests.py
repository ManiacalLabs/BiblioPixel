from . strip import Strip
from . matrix import Matrix
from . animation import Animation
from .. colors import COLORS

BASE_COLORS = [COLORS.Red, COLORS.Green, COLORS.Green,
               COLORS.Blue, COLORS.Blue, COLORS.Blue]
CYCLE_COLORS = [COLORS.Red, COLORS.Green, COLORS.Blue, COLORS.White]


class StripChannelTest(Strip):

    def __init__(self, layout):
        super().__init__(layout)
        self.internal_delay = 0.500
        self.colors = CYCLE_COLORS

    def step(self, amt=1):
        for i, c in enumerate(BASE_COLORS):
            self.layout.set(i, c)

        color = self.cur_step % 4
        self.layout.fill(self.colors[color], 7, 9)


class MatrixChannelTest(Matrix):

    def __init__(self, layout):
        super().__init__(layout, 0, 0)
        self.internal_delay = 0.500
        self.colors = [COLORS.Red, COLORS.Green, COLORS.Blue, COLORS.White]

    def step(self, amt=1):
        self.layout.drawLine(0, 0, 0, self.height - 1, COLORS.Red)
        self.layout.drawLine(1, 0, 1, self.height - 1, COLORS.Green)
        self.layout.drawLine(2, 0, 2, self.height - 1, COLORS.Green)
        self.layout.drawLine(3, 0, 3, self.height - 1, COLORS.Blue)
        self.layout.drawLine(4, 0, 4, self.height - 1, COLORS.Blue)
        self.layout.drawLine(5, 0, 5, self.height - 1, COLORS.Blue)

        color = self.cur_step % 4
        self.layout.fillRect(7, 0, 3, self.height, self.colors[color])


class MatrixCalibrationTest(Matrix):

    def __init__(self, layout):
        super().__init__(layout, 0, 0)
        self.internal_delay = 0.500
        self.colors = [COLORS.Red, COLORS.Green, COLORS.Green,
                       COLORS.Blue, COLORS.Blue, COLORS.Blue]

    def step(self, amt=1):
        self.layout.all_off()
        i = self.cur_step % self.width
        for x in range(i + 1):
            c = self.colors[x % len(self.colors)]
            self.layout.drawLine(x, 0, x, i, c)

        self.completed = (i == (self.width - 1))


class PixelTester(Animation):
    """"""
    PAUSE = 10

    def __init__(self, *args, brightness=1.0, **kwds):
        self.brightness = brightness
        super().__init__(*args, **kwds)

    def pre_run(self):
        self.stepper = self.steps()

    def step(self, amt=1):
        try:
            next(self.stepper)
        except StopIteration:
            self.completed = True

    def steps(self):
        for color in (COLORS.Red, COLORS.Green, COLORS.Blue, COLORS.Yellow,
                      COLORS.Fuchsia, COLORS.Aqua, COLORS.White):
            color = tuple(c * self.brightness for c in color)
            for i in range(len(self.color_list)):
                self.color_list[i] = color
                yield

            for i in range(self.PAUSE):
                yield

            self.color_list = [COLORS.Black] * len(self.color_list)
            yield
