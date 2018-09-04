import math, threading, time
from . matrix import Matrix


# Takes a matrix and displays it as individual columns over time
class POV(Matrix):

    def __init__(self, drivers, povHeight, width, rotation=0,
                 vert_flip=False, threadedUpdate=False,
                 brightness=255, **kwargs):
        self.numLEDs = povHeight * width

        super().__init__(drivers, width, povHeight, None,
                         rotation, vert_flip, threadedUpdate, brightness,
                         **kwargs)

    # This is the magic. Overriding the normal push_to_driver() method
    # It will automatically break up the frame into columns spread over
    # frameTime (ms)
    def push_to_driver(self, frameTime=None):
        if frameTime:
            self.animation_sleep_time = frameTime

        sleep = None
        if self.animation_sleep_time:
            sleep = (self.animation_sleep_time -
                     self.frame_render_time) / self.width

        width = self.width
        for h in range(width):
            start = time.time()

            def color(i):
                return self._colors[(h + width * i) * 3]
            # TODO: Figure out what line below needs to do
            # buf = [color(i) for i in range(self.height)]
            self.drivers[0].update_colors()
            sendTime = time.time() - start
            if sleep:
                time.sleep(max(0, sleep - sendTime))


from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    LEDPOV = POV
