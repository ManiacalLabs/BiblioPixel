from . import collection
import random as rand


class Sequence(collection.Collection):
    def __init__(self, layout, random=False, **kwds):
        super().__init__(layout, **kwds)
        self.random = random

    def restart(self):
        self.random and rand.shuffle(self.animations)
        self.index = 0

    def pre_run(self):
        self.restart()

    def step(self, amt=1):
        if not self.animations:
            return

        if not self.completed:
            self.current_animation.run_all_frames(clean_layout=False)

        self.index += 1
        if self.index >= len(self.animations):
            if self.runner.until_complete:
                self.completed = True
            else:
                self.restart()
