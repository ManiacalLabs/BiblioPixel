from .. project import aliases, project
from . import animation
import copy, traceback
from .. util import log


class Collection(animation.BaseAnimation):
    def __init__(self, layout, animations=None, no_fail=False, **kwds):
        super().__init__(layout, **kwds)
        self.animations = [self._make_animation(i, no_fail) for i in animations or []]
        self.index = 0
        self.internal_delay = 0  # never wait

    # Override to handle all the animations
    def cleanup(self, clean_layout=True):
        self.state = animation.STATE.canceled
        for a in self.animations:
            if a:
                a.cleanup()
        super().cleanup(clean_layout)

    def add_animation(self, anim, **kwds):
        # DEPRECATED.
        anim.set_runner(kwds)
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
            animation = a
            run = None

        elif isinstance(a, dict):
            animation = a.get('animation')
            if animation:
                # Looks like {'animation': ..., 'run': }
                run = a.get('run')
            else:
                # It's an animation itself.
                animation, run = a, None

        else:
            animation, run = a

        assert animation, '%s:%s:%s' % (a, animation, run)
        try:
            return project.make_animation(self.layout, animation, run)
        except:
            log.error(traceback.format_exc())
            return None
