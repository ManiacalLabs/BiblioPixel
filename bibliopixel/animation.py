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

    # def stopped(self):
    #     return self._anim._stopThread

    def run(self):
        log.logger.debug("Starting thread...")
        self._anim._run(**self._args)
        log.logger.debug("Thread Complete")

class BaseAnimation(object):
    def __init__(self, led):
        self._led = led
        self.animComplete = False
        self._step = 0
        self._timeRef = 0
        self._internalDelay = None
        self._threaded = False
        self._stopThread = False
        self._thread = None
        self._callback = None

    def _msTime(self):
        return time.time() * 1000.0

    def preRun(self, amt=1):
        pass

    def preStep(self, amt=1):
        pass

    def postStep(self, amt=1):
        pass

    def step(self, amt = 1):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def stopThread(self, wait = False):
        print "Stopping thread..."
        if self._thread:
            self._stopThread = True
            if wait:
                self._thread.join()

    def __enter__(self):
        return self

    def __exit(self, type, value, traceback):
        pass

    def __exit__(self, type, value, traceback):
        self.__exit(type, value, traceback)
        self._led.all_off()
        self._led.update()
        self.stopThread(wait = True)

    def cleanup(self):
        return self.__exit__(None, None, None)

    def stopped(self):
        if self._thread:
            return not self._thread.isAlive()
        else:
            return True

    def _run(self, amt, fps, sleep, max_steps, untilComplete, max_cycles):
        self.preRun()

        #calculate sleep time base on desired Frames per Second
        if fps != None:
            sleep = int(1000 / fps)

        initSleep = sleep

        self._step = 0
        cur_step = 0
        cycle_count = 0
        self.animComplete = False

        while not self._stopThread and ((not untilComplete and (max_steps == 0 or cur_step < max_steps)) or (untilComplete and not self.animComplete)):
            self._timeRef = self._msTime()

            start = self._msTime()
            if hasattr(self, "_input_dev"):
                self._keys = self._input_dev.getKeys()
            self.preStep(amt)
            self.step(amt)
            self.postStep(amt)
            mid = self._msTime()

            if initSleep:
                sleep = initSleep
            elif self._internalDelay:
                sleep = self._internalDelay

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
                log.logger.debug("Frame: {}ms / Update Max: {}ms".format(stepTime, updateTime))
            else:
                log.logger.debug("{}ms/{}fps / Frame: {}ms / Update: {}ms".format(totalTime, int(1000 / max(totalTime,1)), stepTime, updateTime))

            if sleep:
                diff = (self._msTime() - self._timeRef)
                t = max(0, (sleep - diff) / 1000.0)
                if t == 0:
                    log.logger.warning("Frame-time of %dms set, but took %dms!" % (sleep, diff))
                time.sleep(t)
            cur_step += 1

        if self._callback:
            self._callback(self)

    def run(self, amt = 1, fps=None, sleep=None, max_steps = 0, untilComplete = False, max_cycles = 0, threaded = False, joinThread = False, callback=None):

        self._threaded = threaded
        self._stopThread = False
        self._callback = callback

        if self._threaded:
            args = {}
            l = locals()
            run_params = ["amt", "fps", "sleep", "max_steps", "untilComplete", "max_cycles"]
            for p in run_params:
                if p in l:
                    args[p] = l[p]

            self._thread = animThread(self, args)
            self._thread.start()
            if joinThread:
                self._thread.join()
        else:
            self._run(amt, fps, sleep, max_steps, untilComplete, max_cycles)

    RUN_PARAMS = [{
                "id": "amt",
                "label": "Step Amount",
                "type": "int",
                "min": 1,
                "default": 1,
                "help":"Amount to step animation by on each frame. May not be used on some animations."
            },{
                "id": "fps",
                "label": "Framerate",
                "type": "int",
                "default": None,
                "min": 1,
                "help":"Framerate at which to run animation."
            },{
                "id": "max_steps",
                "label": "Max Frames",
                "type": "int",
                "min": 0,
                "default": 0,
                "help":"Total frames to run before stopping."
            },{
                "id": "untilComplete",
                "label": "Until Complete",
                "type": "bool",
                "default": False,
                "help":"Run until animation marks itself as compelte. If supported."
            },{
                "id": "max_cycles",
                "label": "Max Cycles",
                "type": "int",
                "min": 1,
                "default": 1,
                "help":"If Until Complete is set, animation will repeat this many times."
            },]

class AnimationQueue(BaseAnimation):
    def __init__(self, led, anims=[]):
        super(AnimationQueue, self).__init__(led)
        self.anims = anims
        self.curAnim = None
        self.animIndex = 0;
        self._internalDelay = 0 #never wait
        self.fps = None
        self.untilComplete = False

    #overriding to handle all the animations
    def stopThread(self, wait = False):
        print "Stopping queue..."
        for a,r in self.anims:
            #a bit of a hack. they aren't threaded, but stops them anyway
            a._stopThread = True
        super(AnimationQueue, self).stopThread(wait)

    def addAnim(self, anim, amt = 1, fps=None, max_steps = 0, untilComplete = False, max_cycles = 0):
        a = (
            anim,
            {
                "amt": amt,
                "fps": fps,
                "max_steps": max_steps,
                "untilComplete": untilComplete,
                "max_cycles": max_cycles
            }
        )
        self.anims.append(a)

    RUN_PARAMS = [{
                "id": "fps",
                "label": "Default Framerate",
                "type": "int",
                "default": None,
                "min": 1,
                "help":"Default framerate to run all animations in queue."
            },{
                "id": "untilComplete",
                "label": "Until Complete",
                "type": "bool",
                "default": False,
                "help":"Run until animation marks itself as compelte. If supported."
            }]

    def preRun(self, amt=1):
        if len(self.anims) == 0:
            raise Exception("Must provide at least one animation.")
        self.animIndex = -1

    def run(self, amt = 1, fps=None, sleep=None, max_steps = 0, untilComplete = False, max_cycles = 0, threaded = False, joinThread = False, callback=None):
        self.fps = fps
        self.untilComplete = untilComplete
        super(AnimationQueue, self).run(amt = 1, fps=None, sleep=None, max_steps = 0, untilComplete = untilComplete, max_cycles = 0, threaded = threaded, joinThread = joinThread, callback=callback)

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
            run['threaded'] = False
            run['joinThread'] = False
            run['callback'] = None

            if run['fps'] == None and self.fps != None:
                run['fps'] = self.fps
            anim.run(**(run))

class BaseStripAnim(BaseAnimation):
    def __init__(self, led, start = 0, end = -1):
        super(BaseStripAnim, self).__init__(led)

        if not isinstance(led, LEDStrip):
            raise RuntimeError("Must use LEDStrip with Strip Animations!")

        self._start = start
        self._end = end
        if self._start < 0:
            self._start = 0
        if self._end < 0 or self._end > self._led.lastIndex:
            self._end = self._led.lastIndex

        self._size = self._end - self._start + 1

class BaseMatrixAnim(BaseAnimation):
    def __init__(self, led, width=0, height=0, startX=0, startY=0):
        super(BaseMatrixAnim, self).__init__(led)
        if not isinstance(led, LEDMatrix):
            raise RuntimeError("Must use LEDMatrix with Matrix Animations!")

        if width == 0:
            self.width = led.width
        else:
            self.width = width

        if height == 0:
            self.height = led.height
        else:
            self.height = height

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

    def setSpeed(self, name, speed):
        self._speeds[name] = speed

    def getSpeed(self, name):
        if name in self._speeds:
            return self._speeds[name]
        else:
            return None

    def _checkSpeed(self, speed):
        return self._speedStep % speed == 0

    def checkSpeed(self, name):
        return (name in self._speeds) and (self._checkSpeed(self._speeds[name]))

    def addKeyFunc(self, key, func, speed = 1, hold = True):
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
                else:
                    if speedPass:
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
        self.colors =  [colors.Red, colors.Green, colors.Blue, colors.White]

    def step(self, amt = 1):

        self._led.set(0, colors.Red)
        self._led.set(1, colors.Green)
        self._led.set(2, colors.Green)
        self._led.set(3, colors.Blue)
        self._led.set(4, colors.Blue)
        self._led.set(5, colors.Blue)

        color =  self._step % 4
        self._led.fill(self.colors[color], 7, 9)

        self._step += 1

class MatrixChannelTest(BaseMatrixAnim):
    def __init__(self, led):
        super(MatrixChannelTest, self).__init__(led, 0, 0)
        self._internalDelay = 500
        self.colors =  [colors.Red, colors.Green, colors.Blue, colors.White]

    def step(self, amt = 1):

        self._led.drawLine(0, 0, 0, self.height - 1, colors.Red)
        self._led.drawLine(1, 0, 1, self.height - 1, colors.Green)
        self._led.drawLine(2, 0, 2, self.height - 1, colors.Green)
        self._led.drawLine(3, 0, 3, self.height - 1, colors.Blue)
        self._led.drawLine(4, 0, 4, self.height - 1, colors.Blue)
        self._led.drawLine(5, 0, 5, self.height - 1, colors.Blue)

        color =  self._step % 4
        self._led.fillRect(7, 0, 3, self.height, self.colors[color])

        self._step += 1

class MatrixCalibrationTest(BaseMatrixAnim):
    def __init__(self, led):
        super(MatrixCalibrationTest, self).__init__(led, 0, 0)
        self._internalDelay = 500
        self.colors = [colors.Red, colors.Green, colors.Green, colors.Blue, colors.Blue, colors.Blue]

    def step(self, amt = 1):
        self._led.all_off()
        i = self._step % self.width
        for x in range(i + 1):
            c = self.colors[x % len(self.colors)]
            self._led.drawLine(x, 0, x, i, c)

        self.animComplete = (i == (self.width-1))

        self._step += 1
