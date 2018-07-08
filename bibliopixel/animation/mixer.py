import copy
from . import parallel
from .. util import color_list


class Mixer(parallel.Parallel):
    def __init__(self, *args, levels=None, master=1, **kwds):
        self.master = master

        super().__init__(*args, **kwds)
        self.mixer = color_list.Mixer(
            self.color_list,
            [a.color_list for a in self.animations],
            levels)

    @property
    def levels(self):
        return self.mixer.levels

    @levels.setter
    def levels(self, levels):
        self.mixer.levels[:] = levels

    def step(self, amt=1):
        super().step(amt)
        self.mixer.clear()
        self.mixer.mix(self.master)
