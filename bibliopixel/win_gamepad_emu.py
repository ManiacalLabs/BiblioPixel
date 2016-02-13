import win32api
import win32con

from util import d
from gamepad import BaseGamePad

DEFAULT_MAP = {
    "UP": win32con.VK_UP,
    "DOWN": win32con.VK_DOWN,
    "LEFT": win32con.VK_LEFT,
    "RIGHT": win32con.VK_RIGHT,
    "SELECT": win32con.VK_SPACE,
    "START": win32con.VK_RETURN,
    "A": "A",
    "B": "S",
    "X": "Z",
    "Y": "X"
}


class WinGamePadEmu(BaseGamePad):

    def __init__(self, btn_map=DEFAULT_MAP):
        super(WinGamePadEmu, self).__init__()
        self._map = btn_map

    def getKeys(self):
        result = {}
        for k in self._map:
            v = self._map[k]
            if isinstance(v, str):
                v = ord(v)
            result[k] = abs(win32api.GetAsyncKeyState(v)) > 1
        return d(result)
