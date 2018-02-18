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
        self._load_animation()

    def pre_run(self):
        self.offset = 0
        self.restart()

    def step(self, amt=1):
        if not self.animations or self.completed:
            return

        try:
            next(self.frames)
            return
        except StopIteration:
            pass

        self.index += 1
        if self.index < len(self.animations):
            self._load_animation()

        elif self.runner.until_complete:
            self.completed = True

        else:
            self.offset += len(self.animations)
            self.restart()

    def _load_animation(self):
        log.debug('Sequence: %s', self.current_animation.title)
        if self.length:
            step = self.offset + self.index
            length = self.length[step % len(self.length)]
            self.current_animation.runner.seconds = length
        self.frames = self.current_animation.generate_frames(False)
