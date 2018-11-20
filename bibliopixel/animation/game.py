from . matrix import Matrix


class Game(Matrix):

    def __init__(self, layout, inputDev):
        super().__init__(layout)
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
            self._keyfuncs[k] = {
                "func": func,
                "speed": speed,
                "hold": hold,
                "last": False,
                "inter": False
            }

    def handleKeys(self):
        for key in self._keys:
            val = self._keys[key]
            if key in self._keyfuncs:
                cfg = self._keyfuncs[key]
                speed_pass = self._checkSpeed(cfg.speed)

                if cfg.hold:
                    if speed_pass:
                        if (val or cfg.inter):
                            cfg.func()
                        else:
                            cfg.inter = cfg.last = val
                elif speed_pass:
                    if (val or cfg.inter) and not cfg.last:
                        cfg.func()
                    cfg.inter = cfg.last = val
                else:
                    cfg.inter |= val
        self._lastKeys = self._keys

    def step(self, amt):
        self._keys = self._input_dev.getKeys()
        self._speedStep += 1


from .. util import deprecated
if deprecated.allowed():
    BaseGameAnim = Game
