from .. project import aliases, project
from . import animation, runner
import traceback
from .. import log


class Collection(animation.BaseAnimation):
    def __init__(self, layout, animations=None, no_fail=False):
        super().__init__(layout)
        self.animations = [self._make_animation(i, no_fail) for i in animations or []]
        self.index = 0
        self.internal_delay = 0  # never wait

    # Override to handle all the animations
    def cleanup(self, clean_layout=True):
        for a in self.animations:
            if a:
                a.cleanup()
        super().cleanup(clean_layout)

    def add_animation(self, anim, **kwds):
        # DEPRECATED.
        anim.set_runner(runner.Runner(**kwds))
        self.animations.append(anim)

    def pre_run(self):
        self.index = -1

    @property
    def current_animation(self):
        if (0 <= self.index < len(self.animations)):
            return self.animations[self.index]
        else:
            return None

    def _make_animation(self, a, no_fail=False):
        if isinstance(a, str):
            desc = {'animation': a}
        elif isinstance(a, dict):
            if 'animation' in a:
                # TODO: this hackiness occurs because this indirectly gets
                # called from different places.  Figure out a better way.
                desc = a
            else:
                desc = {'animation': a}
        else:
            desc = {'animation': a[0], 'run': a[1]}
        desc = aliases.resolve(desc)
        try:
            return project.make_animation(layout=self.layout, **desc)
        except:
            log.error(traceback.format_exc())
            return None
