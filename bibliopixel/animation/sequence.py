from . import collection
import random as rand


class Sequence(collection.Collection):
    def __init__(self, layout, random=False, **kwds):
        super().__init__(layout, **kwds)
        self.random = random
        self.indices = list(range(0, len(self.animations)))
        self.sub_index = 0

    def pre_run(self):
        if self.random:
            rand.shuffle(self.indices)
        self.sub_index = 0

    def step(self, amt=1):
        self.sub_index += 1

        if self.sub_index >= len(self.animations):
            if self.runner.until_complete:
                self.completed = True
            else:
                rand.shuffle(self.indices)
                self.sub_index = 0

        self.index = self.indices[self.sub_index]

        if not self.completed and self.animations:
            self.current_animation.run_all_frames()
