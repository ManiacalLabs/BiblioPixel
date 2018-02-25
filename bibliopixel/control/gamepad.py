from .. util import AttributeDict


class BaseGamePad(object):
    def __init__(self):
        pass

    def getKeys(self):
        raise Exception("getKeys must be overriden!")

    def close(self):
        pass

    def setLights(self, data):
        pass

    def setLightsOff(self, count):
        pass
