import threading, time

from . base import BaseAnimation
from .. led import LEDMatrix, LEDStrip, LEDCircle
from .. import colors
from .. util import AttributeDict


class OffAnim(BaseAnimation):

    def __init__(self, led, timeout=10):
        super(OffAnim, self).__init__(led)
        self._internalDelay = timeout * 1000

    def step(self, amt=1):
        self._led.all_off()


class AnimationQueue(BaseAnimation):

    def __init__(self, led, anims=None):
        super(AnimationQueue, self).__init__(led)
        self.anims = anims or []
        self.curAnim = None
        self.animIndex = 0
        self._internalDelay = 0  # never wait
        self.fps = None
        self.untilComplete = False

    # overriding to handle all the animations
    def stopThread(self, wait=False):
        for a, r in self.anims:
            # a bit of a hack. they aren't threaded, but stops them anyway
            a._stopEvent.set()
        super(AnimationQueue, self).stopThread(wait)

    def addAnim(self, anim, amt=1, fps=None, max_steps=0, untilComplete=False, max_cycles=0, seconds=None):
        a = (
            anim,
            {
                "amt": amt,
                "fps": fps,
                "max_steps": max_steps,
                "untilComplete": untilComplete,
                "max_cycles": max_cycles,
                "seconds": seconds
            }
        )
        self.anims.append(a)

    def preRun(self, amt=1):
        if len(self.anims) == 0:
            raise Exception("Must provide at least one animation.")
        self.animIndex = -1

    def run(self, amt=1, fps=None, sleep=None, max_steps=0, untilComplete=False, max_cycles=0, threaded=False, joinThread=False, callback=None, seconds=None):
        self.fps = fps
        self.untilComplete = untilComplete
        super(AnimationQueue, self).run(amt=1, fps=None, sleep=None, max_steps=0, untilComplete=untilComplete,
                                        max_cycles=0, threaded=threaded, joinThread=joinThread, callback=callback, seconds=seconds)

    def step(self, amt=1):
        self.animIndex += 1
        if self.animIndex >= len(self.anims):
            if self.untilComplete:
                self.animComplete = True
            else:
                self.animIndex = 0

        if not self.animComplete:
            self.curAnim = self.anims[self.animIndex]

            anim, run = self.curAnim
            run.update(threaded=False, joinThread=False, callback=None)

            run['fps'] = run.get('fps') or self.fps
            anim.run(**(run))

    RUN_PARAMS = [{
        "id": "fps",
        "label": "Default Framerate",
        "type": "int",
                "default": None,
                "min": 1,
                "help": "Default framerate to run all animations in queue."
    }, {
        "id": "untilComplete",
        "label": "Until Complete",
        "type": "bool",
                "default": False,
                "help": "Run until animation marks itself as complete. If supported."
    }]


class BaseStripAnim(BaseAnimation):

    def __init__(self, led, start=0, end=-1):
        super(BaseStripAnim, self).__init__(led)

        if not isinstance(led, LEDStrip):
            raise RuntimeError("Must use LEDStrip with Strip Animations!")

        self._start = max(start, 0)
        self._end = end
        if self._end < 0 or self._end >= self._led.numLEDs:
            self._end = self._led.numLEDs - 1

        self._size = self._end - self._start + 1


class BaseMatrixAnim(BaseAnimation):

    def __init__(self, led, width=0, height=0, startX=0, startY=0):
        super(BaseMatrixAnim, self).__init__(led)
        if not isinstance(led, LEDMatrix):
            raise RuntimeError("Must use LEDMatrix with Matrix Animations!")

        self.width = width or led.width
        self.height = height or led.height

        self.startX = startX
        self.startY = startY


class BaseGameAnim(BaseMatrixAnim):

    def __init__(self, led, inputDev):
        super(BaseGameAnim, self).__init__(led)
        self._input_dev = inputDev
        self._keys = None
        self._lastKeys = None
        self._speedStep = 0
        self._speeds = {}
        self._keyfuncs = {}

    def _exit(self, type, value, traceback):
        if hasattr(self._input_dev, 'setLightsOff'):
            self._input_dev.setLightsOff(5)
        self._input_dev.close()

    def setSpeed(self, name, speed):
        self._speeds[name] = speed

    def getSpeed(self, name):
        return self._speeds.get(name)

    def _checkSpeed(self, speed):
        return not (self._speedStep % speed)

    def checkSpeed(self, name):
        return name in self._speeds and self._checkSpeed(self._speeds[name])

    def addKeyFunc(self, key, func, speed=1, hold=True):
        if not isinstance(key, list):
            key = [key]
        for k in key:
            self._keyfuncs[k] = AttributeDict({
                "func": func,
                "speed": speed,
                "hold": hold,
                "last": False,
                "inter": False
            })

    def handleKeys(self):
        kf = self._keyfuncs
        for key in self._keys:
            val = self._keys[key]
            if key in kf:
                cfg = kf[key]
                speedPass = self._checkSpeed(cfg.speed)

                if cfg.hold:
                    if speedPass:
                        if (val or cfg.inter):
                            cfg.func()
                        else:
                            cfg.inter = cfg.last = val
                elif speedPass:
                    if (val or cfg.inter) and not cfg.last:
                        cfg.func()
                    cfg.inter = cfg.last = val
                else:
                    cfg.inter |= val
        self._lastKeys = self._keys

    def preStep(self, amt):
        pass

    def postStep(self, amt):
        self._speedStep += 1


class BaseCircleAnim(BaseAnimation):

    def __init__(self, led):
        super(BaseCircleAnim, self).__init__(led)

        if not isinstance(led, LEDCircle):
            raise RuntimeError("Must use LEDCircle with Circle Animations!")

        self.rings = led.rings
        self.ringCount = led.ringCount
        self.lastRing = led.lastRing
        self.ringSteps = led.ringSteps


class StripChannelTest(BaseStripAnim):

    def __init__(self, led):
        super(StripChannelTest, self).__init__(led)
        self._internalDelay = 500
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
        super(MatrixChannelTest, self).__init__(led, 0, 0)
        self._internalDelay = 500
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
        super(MatrixCalibrationTest, self).__init__(led, 0, 0)
        self._internalDelay = 500
        self.colors = [colors.Red, colors.Green, colors.Green,
                       colors.Blue, colors.Blue, colors.Blue]

    def step(self, amt=1):
        self._led.all_off()
        i = self._step % self.width
        for x in range(i + 1):
            c = self.colors[x % len(self.colors)]
            self._led.drawLine(x, 0, x, i, c)

        self.animComplete = (i == (self.width - 1))

        self._step += 1
