import copy
from . import collection
from .. util import color_list


class Mixer(collection.Parallel):
    def __init__(self, *args, levels=None, master=1, **kwds):
        self.master = master

        super()(*args, **kwds)
        self.mixer = color_list.Mixer(
            self.color_list,
            [a.color_list for a in self.animations],
            levels)

    def step(self, amt=1):
        super().step(amt)
        self.mixer.clear()
        self.mixer.mix(self.master)
