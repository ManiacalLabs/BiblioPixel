from .. project import aliases, project
from . import animation, runner


class Collection(animation.BaseAnimation):
    def __init__(self, layout, animations=None):
        super().__init__(layout)
        self.animations = [self._make_animation(i) for i in animations or []]
        self.index = 0
        self.internal_delay = 0  # never wait

    # Override to handle all the animations
    def cleanup(self, clean_layout=True):
        for a in self.animations:
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
        return self.animations[self.index]

    def _make_animation(self, a):
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
        return project.make_animation(layout=self.layout, **desc)
