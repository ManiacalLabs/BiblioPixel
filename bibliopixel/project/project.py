from . import attributes, construct, cleanup, defaults, load, recurse
from .. util import exception, json

ROOT_FILE = None


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


def project(*descs, root_file=None):
    def default(o):
        if isinstance(o, type):
            return str(o)
        return str(o.__class__).replace('<class ', '<').replace('>', ' object>')

    desc = defaults.merge(*descs)

    global ROOT_FILE
    ROOT_FILE = root_file

    with load.extender(desc.get('path', '')):
        desc = recurse.recurse(desc)

    project = construct.construct(**desc)
    project.desc = desc
    return project
