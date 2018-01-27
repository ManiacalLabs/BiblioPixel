import os, traceback
from .. project import aliases, construct, project
from . import animation
from .. util import json, log


class Collection(animation.BaseAnimation):
    FAIL_ON_EXCEPTION = False

    @staticmethod
    def pre_recursion(desc):
        def cleanup_animation(a):
            if isinstance(a, str) and (
                    a.endswith('.yml') or a.endswith('.json')):
                if not os.path.isabs(a):
                    a = os.path.join(os.path.dirname(project.ROOT_FILE), a)
                a = json.load(a)
                if 'animation' in a:
                    # Dump other cruft.  This is useful if you want to load just
                    # the animation from a complete project.
                    a = {'animation': a['animation'], 'run': a.get('run', {})}

            if callable(a) or isinstance(a, str) or 'animation' not in a:
                animation = a
                a = {}
            else:
                animation = a.pop('animation')
            animation = construct.to_type_constructor(
                animation, 'bibliopixel.animation')
            arun = a.pop('run', {})
            arun = animation['run'] = dict(arun, **animation.get('run', {}))
            drun = desc['run']

            # Children without fps or sleep_time get it from their parents.
            if not ('fps' in arun or 'sleep_time' in arun):
                if 'fps' in drun:
                    arun.update(fps=drun['fps'])
                elif 'sleep_time' in drun:
                    arun.update(sleep_time=drun['sleep_time'])

            if a:
                raise ValueError('Extra fields in animation: ' + ', '.join(a))
            return animation

        desc['animations'] = [cleanup_animation(a) for a in desc['animations']]
        return desc

    CHILDREN = 'animations',

    def __init__(self, layout, animations=None, **kwds):
        super().__init__(layout, **kwds)
        self.animations = animations or []
        self.index = 0
        self.internal_delay = 0  # never wait

    # Override to handle all the animations
    def cleanup(self, clean_layout=True):
        self.state = animation.STATE.canceled
        for a in self.animations:
            a and a.cleanup()
        super().cleanup(clean_layout)

    def add_animation(self, anim, **kwds):
        # DEPRECATED.
        anim.set_runner(kwds)
        self.animations.append(anim)

    def pre_run(self):
        self.index = -1
        for a in self.animations:
            a and a.pre_run()

    @property
    def current_animation(self):
        if 0 <= self.index < len(self.animations):
            return self.animations[self.index]


class Parallel(Collection):
    def __init__(self, *args, levels, **kwds):
        super()(*args, **kwds)

        # Give each animation a unique, mutable layout so they can
        # run independently.
        for a in self.animations:
            a.layout = a.layout.mutable_copy()

    def step(self, amt=1):
        for a in self.animations:
            a and a.step(amt)


class Wrapper(Collection):
    def __init__(self, *args, animation, **kwds):
        super()(*args, animations=[animation], **kwds)
        self.animation = self.animations[0]

    def step(self, amt=1):
        self.animation and self.animation.step(amt)
