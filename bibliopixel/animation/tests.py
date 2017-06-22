from . strip import BaseStripAnim
from . matrix import BaseMatrixAnim
from .. import colors


class StripChannelTest(BaseStripAnim):

    def __init__(self, layout):
        super().__init__(layout)
        self.internal_delay = 0.500
        self.colors = [colors.Red, colors.Green, colors.Blue, colors.White]

    def step(self, amt=1):

        self.layout.set(0, colors.Red)
        self.layout.set(1, colors.Green)
        self.layout.set(2, colors.Green)
        self.layout.set(3, colors.Blue)
        self.layout.set(4, colors.Blue)
        self.layout.set(5, colors.Blue)

        color = self._step % 4
        self.layout.fill(self.colors[color], 7, 9)

        self._step += 1


class MatrixChannelTest(BaseMatrixAnim):

    def __init__(self, layout):
        super().__init__(layout, 0, 0)
        self.internal_delay = 0.500
        self.colors = [colors.Red, colors.Green, colors.Blue, colors.White]

    def step(self, amt=1):

        self.layout.drawLine(0, 0, 0, self.height - 1, colors.Red)
        self.layout.drawLine(1, 0, 1, self.height - 1, colors.Green)
        self.layout.drawLine(2, 0, 2, self.height - 1, colors.Green)
        self.layout.drawLine(3, 0, 3, self.height - 1, colors.Blue)
        self.layout.drawLine(4, 0, 4, self.height - 1, colors.Blue)
        self.layout.drawLine(5, 0, 5, self.height - 1, colors.Blue)

        color = self._step % 4
        self.layout.fillRect(7, 0, 3, self.height, self.colors[color])

        self._step += 1


class MatrixCalibrationTest(BaseMatrixAnim):

    def __init__(self, layout):
        super().__init__(layout, 0, 0)
        self.internal_delay = 0.500
        self.colors = [colors.Red, colors.Green, colors.Green,
                       colors.Blue, colors.Blue, colors.Blue]

    def step(self, amt=1):
        self.layout.all_off()
        i = self._step % self.width
        for x in range(i + 1):
            c = self.colors[x % len(self.colors)]
            self.layout.drawLine(x, 0, x, i, c)

        self.completed = (i == (self.width - 1))

        self._step += 1
