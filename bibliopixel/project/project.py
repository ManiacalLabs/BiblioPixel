import copy
from . import attributes, construct, cleanup, defaults, load, recurse
from .. util import exception


class Project:
    CHILDREN = 'maker', 'drivers', 'layout', 'animation'

    @staticmethod
    def pre_recursion(desc):
        return cleanup.cleanup(desc)

    def construct_child(self, datatype, typename=None, **kwds):
        construct = getattr(datatype, 'construct', None)
        if construct:
            return construct(self, **kwds)
        return datatype(**kwds)

    def __init__(self, *, drivers, layout, maker, path, animation, **kwds):
        attributes.check(kwds, 'project')
        self.path = path
        layout = layout or cleanup.cleanup_layout(animation)

        self.maker = self.construct_child(**maker)

        def post(desc):
            return self.construct_child(**desc)

        def create(root, name):
            with exception.add('Unable to create ' + name):
                return recurse.recurse(
                    root,
                    pre=None,
                    post=post,
                    python_path='bibliopixel.' + name)

        self.drivers = [create(d, 'drivers') for d in drivers]
        with exception.add('Unable to create layout'):
            self.layout = self.construct_child(**layout)
        self.animation = create(animation, 'animation')

    def make_animation(self):
        return self.animation


def project(*descs, **kwds):
    desc = defaults.merge(*descs, **kwds)
    with load.extender(desc.get('path', '')):
        desc = recurse.recurse(desc)
        return construct.construct(**desc)


def read_project(location, threaded=None, default=None, **kwds):
    project_data = load.data(location)
    if threaded is not None:
        project_data.setdefault('run', {})['threaded'] = threaded

    return project(default, copy.deepcopy(project_data), **kwds)
