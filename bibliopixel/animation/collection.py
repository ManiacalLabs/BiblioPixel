import os
from .. project import aliases, construct, load, project
from . import animation, failed
from .. util import log


class Collection(animation.Animation):
    """
    A ``Collection`` is a list of ``Animation``s
    """

    @staticmethod
    def pre_recursion(desc):
        animations = []
        name_count = {}

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

            datatype = animation.setdefault('datatype', failed.Failed)
            name = animation.setdefault('name', datatype.__name__)
            name_count[name] = 1 + name_count.get(name, 0)

            # Children without fps or sleep_time get it from their parents.
            if not ('fps' in run or 'sleep_time' in run):
                if 'fps' in desc['run']:
                    run.update(fps=desc['run']['fps'])
                elif 'sleep_time' in desc['run']:
                    run.update(sleep_time=desc['run']['sleep_time'])

            animations.append(animation)

        dupes = {k: 1 for k, v in name_count.items() if v > 1}
        for a in animations:
            name = a['name']
            count = dupes.get(name)
            if count:
                dupes[name] += 1
                a['name'] += '_' + str(count - 1)

        desc['animations'] = animations
        return desc

    CHILDREN = 'animations',

    def __init__(self, layout, animations=None, **kwds):
        super().__init__(layout, **kwds)
        self.animations = _AnimationList(animations or [])
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

    def set_project(self, project):
        super().set_project(project)
        for a in self.animations:
            a.set_project(project)

    def detach(self, overlay):
        """
        Give each animation a unique, mutable layout so they can run
        independently.
        """
        # See #868
        #
        for i, a in enumerate(self.animations):
            a.layout = a.layout.clone()
            if overlay and i:
                a.preclear = False


class _AnimationList:
    def __init__(self, animations):
        self._animations = list(animations)
        self._names = {a.name: i for i, a in enumerate(self._animations)}

    def _index(self, i):
        if isinstance(i, int):
            return i % len(self._animations)
        return self._names[i]

    def append(self, animation):
        # We're forced to do the "fill in a name and make sure it's
        # unique" in two different ways, because of this method.
        #
        # TODO: We should disallow APIs from doing surgery on
        # self.animations after construction.  Right now only
        # Remote does this, or legacy code that calls add_animation.
        # That code should go on `cls.pre_recursion( )`.
        self._animations.append(animation)
        try:
            base_name = animation.name
        except AttributeError:
            base_name = animation.__class__.__name__

        count = 0
        name = base_name

        while name in self._names:
            name = '%s_%d' % (base_name, count)
            count += 1

        animation.name = name

    def __getitem__(self, i):
        return self._animations[self._index(i)]

    def __getattr__(self, i):
        return self[i]

    def __iter__(self):
        return iter(self._animations)

    def __len__(self):
        return len(self._animations)
