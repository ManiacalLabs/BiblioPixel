"""
Simple animations that apply to any class of Layout.
"""

import copy
from . import animation
from .. util import log


class Fill(animation.BaseAnimation):
    def __init__(self, *args, color, **kwds):
        super().__init__(*args, preclear=False, **kwds)
        self.color = color

    def pre_run(self):
        if hasattr(self.color_list, 'dtype'):
            self.color_list[:None] = self.color
        else:
            self.color_list[:] = [tuple(self.color)] * len(self.color_list)

    def step(self, amt=1):
        pass


class LogFade(animation.BaseAnimation):
    def __init__(self, *args, color=None, ratio=0.98, **kwds):
        super().__init__(*args, preclear=False, **kwds)
        self.color = color and tuple(c * (1 - ratio) for c in color)
        self.ratio = ratio
        if hasattr(self.color_list, 'dtype'):
            self.step = self.step_numpy

    def step_numpy(self, amt=1):
        self.color_list *= self.ratio
        if self.color:
            self.color_list[:None] += self.color

    def step(self, amt=1):
        if self.color:
            def apply(c):
                return tuple(self.ratio * i + j for i, j in zip(c, self.color))
        else:
            def apply(c):
                return tuple(self.ratio * i for i in c)
        self.color_list[:] = (apply(c) for c in self.color_list)
