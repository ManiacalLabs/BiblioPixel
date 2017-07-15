from .. project import aliases, project
from . import animation, runner


class Sequence(animation.BaseAnimation):
    def __init__(self, layout, animations=None):
        def make_animation(a):
            if isinstance(a, str):
                desc = {'animation': a[0]}
            elif isinstance(a, dict):
                desc = a
            else:
                desc = {'animation': a[0], 'run': a[1]}
            desc = aliases.resolve(desc)
            return project.make_animation(layout=layout, **desc)

        super().__init__(layout)

        self.animations = [make_animation(i) for i in animations or []]
        self.index = 0
        self.internal_delay = 0  # never wait

    # overriding to handle all the animations
    def cleanup(self, clean_layout=True):
        for a in self.animations:
            a.cleanup()
        super().cleanup(clean_layout)

    def add_animation(self, anim, **kwds):
        # DEPRECATED.
        anim.set_runner(runner.Runner(**kwds))
        self.animations.append(anim)

    def preRun(self, amt=1):
        self.index = -1

    @property
    def current_animation(self):
        return self.animations[self.index]

    def step(self, amt=1):
        self.index += 1
        if self.index >= len(self.animations):
            if self.runner.until_complete:
                self.completed = True
            else:
                self.index = 0

        if not self.completed and self.animations:
            self.current_animation.run_all_frames()
