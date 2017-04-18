from . strip import BaseStripAnim
from . matrix import BaseMatrixAnim
from .. import colors


class StripChannelTest(BaseStripAnim):

    def __init__(self, led):
        super().__init__(led)
        self.internal_delay = 0.500
        self.colors = [colors.Red, colors.Green, colors.Blue, colors.White]

    def step(self, amt=1):

        self._led.set(0, colors.Red)
        self._led.set(1, colors.Green)
        self._led.set(2, colors.Green)
        self._led.set(3, colors.Blue)
        self._led.set(4, colors.Blue)
        self._led.set(5, colors.Blue)

        color = self._step % 4
        self._led.fill(self.colors[color], 7, 9)

        self._step += 1


class MatrixChannelTest(BaseMatrixAnim):

    def __init__(self, led):
        super().__init__(led, 0, 0)
        self.internal_delay = 0.500
        self.colors = [colors.Red, colors.Green, colors.Blue, colors.White]

    def step(self, amt=1):

        self._led.drawLine(0, 0, 0, self.height - 1, colors.Red)
        self._led.drawLine(1, 0, 1, self.height - 1, colors.Green)
        self._led.drawLine(2, 0, 2, self.height - 1, colors.Green)
        self._led.drawLine(3, 0, 3, self.height - 1, colors.Blue)
        self._led.drawLine(4, 0, 4, self.height - 1, colors.Blue)
        self._led.drawLine(5, 0, 5, self.height - 1, colors.Blue)

        color = self._step % 4
        self._led.fillRect(7, 0, 3, self.height, self.colors[color])

        self._step += 1


class MatrixCalibrationTest(BaseMatrixAnim):

    def __init__(self, led):
        super().__init__(led, 0, 0)
        self.internal_delay = 0.500
        self.colors = [colors.Red, colors.Green, colors.Green,
                       colors.Blue, colors.Blue, colors.Blue]

    def step(self, amt=1):
        self._led.all_off()
        i = self._step % self.width
        for x in range(i + 1):
            c = self.colors[x % len(self.colors)]
            self._led.drawLine(x, 0, x, i, c)

        self.completed = (i == (self.width - 1))

        self._step += 1
