from . import collection
from .. util import log
import random as rand


class Sequence(collection.Collection):
    def __init__(self, layout, random=False, length=None, **kwds):
        """
        Arguments

        random -- If True, a random animation is selected each step
        length -- if length is a number, run all the animations in a loop
            for `length` seconds each.  If `length` is a list of numbers,
            use the numbers successively as times.
        """
        super().__init__(layout, **kwds)
        self.random = random
        if isinstance(length, (list, tuple)):
            self.length = length
        else:
            self.length = length and [length]

    def restart(self):
        self.random and rand.shuffle(self.animations)
        self.index = 0

    def pre_run(self):
        self.restart()

    def step(self, amt=1):
        if not self.animations:
            return

        if not self.completed:
            log.debug('Sequence: %s', self.current_animation.title)
            if self.length:
                length = self.length[self.cur_step % len(self.length)]
                self.current_animation.runner.seconds = length
            self.current_animation.run_all_frames(clean_layout=False)

        self.index += 1
        if self.index >= len(self.animations):
            if self.runner.until_complete:
                self.completed = True
            else:
                self.restart()
