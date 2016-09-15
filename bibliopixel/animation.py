import time
import log

from led import LEDMatrix
from led import LEDStrip
from led import LEDCircle
import colors

from util import d

import threading


class animThread(threading.Thread):

    def __init__(self, anim, args):
        super(animThread, self).__init__()
        self.setDaemon(True)
        self._anim = anim
        self._args = args

    def run(self):
        log.debug("Starting thread...")
        self._anim._run(**self._args)
        log.debug("Thread Complete")


class BaseAnimation(object):

    def __init__(self, led):
        self._led = led
        self.animComplete = False
        self._step = 0
        self._timeRef = 0
        self._internalDelay = None
        self._sleep = None
        self._threaded = False
        self._thread = None
        self._callback = None
        self._stopEvent = threading.Event()
        self._stopEvent.clear()
        self._led._threadedAnim = False
        self._free_run = False

    def _msTime(self):
        return time.time() * 1000.0

    def preRun(self, amt=1):
        self._led.all_off()

    def preStep(self, amt=1):
        pass

    def postStep(self, amt=1):
        pass

    def step(self, amt=1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def stopThread(self, wait=False):
        if self._thread:
            self._stopEvent.set()

            if wait:
                self._thread.join()

    def __enter__(self):
        return self

    def _exit(self, type, value, traceback):
        pass

    def __exit__(self, type, value, traceback):
        self._exit(type, value, traceback)
        self.stopThread(wait=True)
        self._led.all_off()
        self._led.update()
        self._led.waitForUpdate()

    def cleanup(self):
        return self.__exit__(None, None, None)

    def stopped(self):
        return not (self._thread and self._thread.isAlive())

    def _run(self, amt, fps, sleep, max_steps, untilComplete, max_cycles, seconds):
        self.preRun()

        # calculate sleep time base on desired Frames per Second
        if fps:
            sleep = int(1000 / fps)

        if seconds is not None:
            max_steps = int((seconds * 1000) / sleep)

        initSleep = sleep

        self._step = 0
        cur_step = 0
        cycle_count = 0
        self.animComplete = False

        while (not self._stopEvent.isSet() and
               ((max_steps == 0 and not untilComplete) or
                (max_steps > 0 and cur_step < max_steps) or
                (max_steps == 0 and untilComplete and not self.animComplete))):

            self._timeRef = self._msTime()

            start = self._msTime()
            if hasattr(self, "_input_dev"):
                self._keys = self._input_dev.getKeys()
            self.preStep(amt)
            self.step(amt)
            self.postStep(amt)
            mid = self._msTime()

            if self._free_run:
                sleep = None
            elif self._internalDelay:
                sleep = self._internalDelay
            elif initSleep:
                sleep = initSleep

            self._sleep = sleep

            self._led._frameGenTime = int(mid - start)
            self._led._frameTotalTime = sleep

            self._led.update()
            now = self._msTime()

            if self.animComplete and max_cycles > 0:
                if cycle_count < max_cycles - 1:
                    cycle_count += 1
                    self.animComplete = False

            stepTime = int(mid - start)
            if self._led._threadedUpdate:
                updateTime = int(self._led.lastThreadedUpdate())
                totalTime = updateTime
            else:
                updateTime = int(now - mid)
                totalTime = stepTime + updateTime

            if self._led._threadedUpdate:
                log.debug(
                    "Frame: %sms / Update Max: %sms", stepTime, updateTime)
            else:
                log.debug("%sms/%sfps / Frame: %sms / Update: %sms",
                          totalTime, int(1000 / max(totalTime, 1)), stepTime, updateTime)

            if sleep:
                diff = (self._msTime() - self._timeRef)
                t = max(0, (sleep - diff) / 1000.0)
                if t == 0:
                    log.warning(
                        "Frame-time of %dms set, but took %dms!", sleep, diff)
                if self._threaded:
                    self._stopEvent.wait(t)
                else:
                    time.sleep(t)
            cur_step += 1

        self._exit(None, None, None)

        if self._callback:
            self._callback(self)

    def run(self, amt=1, fps=None, sleep=None, max_steps=0, untilComplete=False, max_cycles=0, threaded=False, joinThread=False, callback=None, seconds=None):

        self._led._threadedAnim = self._threaded = threaded
        if self._threaded:
            self._stopEvent.clear()
        self._callback = callback

        if self._threaded:
            args = {}
            l = locals()
            run_params = ["amt", "fps", "sleep",
                          "max_steps", "untilComplete", "max_cycles", "seconds"]
            for p in run_params:
                if p in l:
                    args[p] = l[p]

            self._thread = animThread(self, args)
            self._thread.start()
            if joinThread:
                self._thread.join()
        else:
            self._run(amt, fps, sleep, max_steps, untilComplete, max_cycles, seconds)

    RUN_PARAMS = [{
        "id": "amt",
        "label": "Step Amount",
        "type": "int",
                "min": 1,
                "default": 1,
                "help": "Amount to step animation by on each frame. May not be used on some animations."
    }, {
        "id": "fps",
        "label": "Framerate",
        "type": "int",
                "default": 15,
                "min": 1,
                "help": "Framerate at which to run animation."
    }, {
        "id": "seconds",
        "label": "Run Seconds",
        "type": "int",
                "default": None,
                "min": 0,
                "help": "Number of seconds to run animation for, based on framerate."
    }, {
        "id": "max_steps",
        "label": "Max Frames",
        "type": "int",
                "min": 0,
                "default": 0,
                "help": "Total frames to run before stopping."
    }, {
        "id": "untilComplete",
        "label": "Until Complete",
        "type": "bool",
                "default": False,
                "help": "Run until animation marks itself as complete. If supported."
    }, {
        "id": "max_cycles",
        "label": "Max Cycles",
        "type": "int",
                "min": 1,
                "default": 1,
                "help": "If Until Complete is set, animation will repeat this many times."
    }, ]


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
        if self._end < 0 or self._end > self._led.lastIndex:
            self._end = self._led.lastIndex

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
            self._keyfuncs[k] = d({
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
