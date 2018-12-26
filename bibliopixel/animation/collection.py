import os
from .. project import aliases, construct, load, project
from . import animation, failed, runner
from .. util import log

DEFAULT_ANIMATION = '.animation'
ANIMATION_PATH = 'bibliopixel.animation'


class Collection(animation.Animation):
    """
    A ``Collection`` is a list of ``Animation``s
    """

    @staticmethod
    def pre_recursion(desc):
        animations = desc['animations']
        animations = [_clean_animation(a, desc) for a in animations]
        _make_names_unique(animations)
        desc['animations'] = animations
        return desc

    CHILDREN = 'animations',

    def __init__(
            self, layout, animations=None, **kwds):
        super().__init__(layout, **kwds)
        self.animations = _AnimationList(animations or [])
        self.internal_delay = 0  # never wait
        for a in self.animations:
            a.top_level = False

    def cleanup(self, clean_layout=True):
        self.state = runner.STATE.canceled
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
        # That code should go on ``cls.pre_recursion()``.
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


def _clean_animation(desc, parent):
    """
    Cleans up all sorts of special cases that humans want when entering
    an animation from a yaml file.

    1. Loading it from a file
    2. Using just a typename instead of a dict
    3. A single dict representing an animation, with a run: section.
    4. (Legacy) Having a dict with parallel elements run: and animation:
    5. (Legacy) A tuple or list: (animation, run )

    """
    desc = load.load_if_filename(desc) or desc

    if isinstance(desc, str):
        animation = {'typename': desc}

    elif not isinstance(desc, dict):
        raise TypeError('Unexpected type %s in collection' % type(desc))

    elif 'typename' in desc or 'animation' not in desc:
        animation = desc

    else:
        animation = desc.pop('animation', {})
        if isinstance(animation, str):
            animation = {'typename': animation}

        animation['run'] = desc.pop('run', {})
        if desc:
            raise ValueError('Extra animation fields: ' + ', '.join(desc))

    animation.setdefault('typename', DEFAULT_ANIMATION)
    animation = construct.to_type_constructor(animation, ANIMATION_PATH)
    datatype = animation.setdefault('datatype', failed.Failed)
    animation.setdefault('name', datatype.__name__)

    # Children without fps or sleep_time get it from their parents.
    # TODO: We shouldn't have to rewrite our descriptions here!  The
    # animation engine should be smart enough to figure out the right
    # speed to run a subanimation without a run: section.
    run = animation.setdefault('run', {})
    run_parent = parent.setdefault('run', {})
    if not ('fps' in run or 'sleep_time' in run):
        if 'fps' in run_parent:
            run.update(fps=run_parent['fps'])
        elif 'sleep_time' in run_parent:
            run.update(sleep_time=run_parent['sleep_time'])

    return animation


def _make_names_unique(animations):
    """
    Given a list of animations, some of which might have duplicate names, rename
    the first one to be <duplicate>_0, the second <duplicate>_1,
    <duplicate>_2, etc."""
    counts = {}
    for a in animations:
        c = counts.get(a['name'], 0) + 1
        counts[a['name']] = c
        if c > 1:
            a['name'] += '_' + str(c - 1)

    dupes = set(k for k, v in counts.items() if v > 1)
    for a in animations:
        if a['name'] in dupes:
            a['name'] += '_0'
