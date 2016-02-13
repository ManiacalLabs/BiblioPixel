from util import d


class BaseGamePad(object):
    def __init__(self):
        pass

    def getKeys(self):
        raise Exception("getKeys must be overriden!")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def close(self):
        pass

    def setLights(self, data):
        pass

    def setLightsOff(self, count):
        pass
