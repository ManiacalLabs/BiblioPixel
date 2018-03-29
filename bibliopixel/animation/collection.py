import os, traceback
from .. project import aliases, construct, load, project
from . import animation
from .. util import json, log


class Collection(animation.Animation):
    """
    A ``Collection`` is a list of ``Animation``s
    """

    @staticmethod
    def pre_recursion(desc):
        animations = []

        for a in desc['animations']:
            loaded = load.load_if_filename(a)
            if loaded:
                animation = loaded.get('animation', {})
                run = loaded.get('run', {})

            elif callable(a) or isinstance(a, str) or 'animation' not in a:
                animation = a
                run = {}

            else:
                animation = a.pop('animation', {})
                run = a.pop('run', {})
                if a:
                    raise ValueError(
                        'Extra fields in animation: ' + ', '.join(a))

            animation = construct.to_type_constructor(
                animation, 'bibliopixel.animation')

            run.update(animation.get('run', {}))
            animation['run'] = run

            # Children without fps or sleep_time get it from their parents.
            if not ('fps' in run or 'sleep_time' in run):
                if 'fps' in desc['run']:
                    run.update(fps=desc['run']['fps'])
                elif 'sleep_time' in desc['run']:
                    run.update(sleep_time=desc['run']['sleep_time'])

            animations.append(animation)

        desc['animations'] = animations
        return desc

    CHILDREN = 'animations',

    def __init__(self, layout, animations=None, **kwds):
        super().__init__(layout, **kwds)
        self.animations = animations or []
        self.internal_delay = 0  # never wait

    # Override to handle all the animations
    def cleanup(self, clean_layout=True):
        self.state = animation.STATE.canceled
        for a in self.animations:
            a.cleanup()
        super().cleanup(clean_layout)

    def add_animation(self, anim, **kwds):
        from .. util import deprecated
        deprecated.deprecated('Collection.add_animation')

        anim._set_runner(kwds)
        self.animations.append(anim)

    def pre_run(self):
        for a in self.animations:
            a.pre_run()
