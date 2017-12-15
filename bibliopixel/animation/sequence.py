from . import collection
from .. util import log
import random as rand


class Sequence(collection.Collection):
    def __init__(
            self, layout, random=False, slideshow=None, **kwds):
        """
        Arguments

        random -- If True, a random animation is selected each step
        slideshow -- if slideshow is a number, run all the animations in a loop
            for `slideshow` seconds each.  If `slideshow` is a list of numbers,
            use the numbers successively as times.
        """
        super().__init__(layout, **kwds)
        self.random = random
        if isinstance(slideshow, (list, tuple)):
            self.slideshow = slideshow
        else:
            self.slideshow = slideshow and [slideshow]

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
            if self.slideshow:
                seconds = self.slideshow[self.cur_step % len(self.slideshow)]
                self.current_animation.runner.seconds = seconds
            self.current_animation.run_all_frames(clean_layout=False)

        self.index += 1
        if self.index >= len(self.animations):
            if self.runner.until_complete:
                self.completed = True
            else:
                self.restart()
