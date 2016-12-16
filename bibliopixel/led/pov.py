import math, threading, time

# from .. import colors, font, matrix, timedata, update_thread

from . matrix import LEDMatrix, MatrixRotation


# Takes a matrix and displays it as individual columns over time
class LEDPOV(LEDMatrix):

    def __init__(self, drivers, povHeight, width, rotation=MatrixRotation.ROTATE_0, vert_flip=False, threadedUpdate=False, masterBrightness=255):
        self.numLEDs = povHeight * width

        super().__init__(drivers, width, povHeight, None,
                         rotation, vert_flip, threadedUpdate, masterBrightness)

    # This is the magic. Overriding the normal push_to_driver() method
    # It will automatically break up the frame into columns spread over
    # frameTime (ms)
    def push_to_driver(self, frameTime=None):
        if frameTime:
            self._frameTotalTime = frameTime

        sleep = None
        if self._frameTotalTime:
            sleep = (self._frameTotalTime - self._frameGenTime) / self.width

        width = self.width
        for h in range(width):
            start = time.time() * 1000.0

            def color(i):
                return self._colors[(h + width * i) * 3]
            # TODO: Figure out what line below needs to do
            # buf = [color(i) for i in range(self.height)]
            self.drivers[0].update_colors()
            sendTime = (time.time() * 1000.0) - start
            if sleep:
                time.sleep(max(0, (sleep - sendTime) / 1000.0))
