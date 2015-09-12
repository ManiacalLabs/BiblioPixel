import win32api
import win32con

from util import d
from gamepad import BaseGamePad

class GamePadEmu(BaseGamePad):
    foundDevices = []
    def __init__(self, btn_map = [[win32con.VK_UP, "UP"], [win32con.VK_DOWN, "DOWN"], [win32con.VK_LEFT, "LEFT"], [win32con.VK_RIGHT, "RIGHT"], [win32con.VK_SPACE, "FIRE"], ["A","A"],["S","B"],["Z","X"],["X","Y"]]):
        super(GamePadEmu, self).__init__()
        self._map = btn_map

    def getKeys(self):
        result = {}
        for m in self._map:
            key = m
            val = m
            if isinstance(m, list):
                val = m[0]
                key = m[1]
            if isinstance(val, str):
                val = ord(val[0])

            result[key] = abs(win32api.GetAsyncKeyState(val)) > 1
        return d(result)
