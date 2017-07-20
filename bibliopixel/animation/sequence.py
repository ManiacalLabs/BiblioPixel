from . import collection


class Sequence(collection.Collection):
    def step(self, amt=1):
        self.index += 1
        if self.index >= len(self.animations):
            if self.runner.until_complete:
                self.completed = True
            else:
                self.index = 0

        if not self.completed and self.animations:
            self.current_animation.run_all_frames()
