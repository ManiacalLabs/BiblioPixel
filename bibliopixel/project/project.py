import copy
from . import attributes, construct, cleanup, load, merge, recurse
from .. util import exception


class Project:
    CHILDREN = 'maker', 'drivers', 'layout', 'animation'

    @staticmethod
    def pre_recursion(desc):
        return cleanup.cleanup_drivers(cleanup.cleanup_animation(desc))

    def construct_child(self, datatype, typename=None, **kwds):
        construct = getattr(datatype, 'construct', None)
        if construct:
            return construct(self, **kwds)
        return datatype(**kwds)

    def __init__(
            self, *, drivers, layout, maker, path, animation, aliases, **kwds):
        attributes.check(kwds, 'project')
        self.path = path
        self.aliases = aliases
        layout = layout or cleanup.cleanup_layout(animation)

        with load.extender(self.path):
            self.maker = self.construct_child(**maker)
            self.drivers = [self.construct_child(**d) for d in drivers]
            with exception.add('Unable to create layout'):
                self.layout = self.construct_child(**layout)

            def post(desc):
                return self.construct_child(**desc)

            with exception.add('Unable to create animation'):
                self.animation = recurse.recurse(
                    animation,
                    pre=None,
                    post=post,
                    python_path='bibliopixel.animation',
                    aliases=self.aliases)

    def make_animation(self):
        return self.animation


def project(*descs):
    desc = merge.merge(merge.DEFAULT_PROJECT, *descs)
    desc = recurse.recurse(desc, aliases=desc['aliases'])
    return construct.construct(**desc)


def read_project(location, threaded=None, default=None):
    project_data = load.data(location)
    if threaded is not None:
        project_data.setdefault('run', {})['threaded'] = threaded

    return project(default, copy.deepcopy(project_data))
