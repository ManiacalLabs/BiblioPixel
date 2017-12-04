import copy
from . import attributes, construct, load, merge, recurse
from .. util import exception

DEFAULT_DRIVERS = [construct.to_type('simpixel')]


class Project:
    @staticmethod
    def pre_recursion(desc):
        if not desc.get('animation'):
            raise ValueError('Missing "animation" section')

        desc['animation'] = construct.to_type_constructor(
            desc['animation'], 'bibliopixel.animation')
        try:
            fix = desc['animation']['datatype'].PROJECT
        except:
            pass
        else:
            desc = merge.merge(fix, desc)

        run = desc.pop('run')
        anim_run = desc['animation'].setdefault('run', {})
        if run:
            desc['animation']['run'] = dict(run, **anim_run)

        driver = construct.to_type(desc.pop('driver', {}))
        drivers = [construct.to_type(d) for d in desc['drivers']]
        if driver:
            if drivers:
                drivers = [dict(driver, **d) for d in drivers]
            else:
                drivers = [driver]

        desc['drivers'] = drivers or DEFAULT_DRIVERS[:]
        return desc

    CHILDREN = 'maker', 'driver', 'drivers', 'layout', 'animation'

    @staticmethod
    def post_recursion(desc):
        animation = desc['animation']
        datatype = animation.get('datatype')
        if not datatype:
            raise ValueError('Missing "datatype" in "animation" section')

        if not desc.get('layout'):
            # Try to fill in the layout if it's missing.
            try:
                args = datatype.LAYOUT_ARGS
                layout_cl = datatype.LAYOUT_CLASS
            except:
                raise ValueError('Missing "layout" section')

            args = {k: animation[k] for k in args if k in animation}
            layout = dict(args, datatype=layout_cl)
            desc['layout'] = layout

        elif not desc['layout'].get('datatype'):
            raise ValueError('Missing "datatype" in "layout" section')

        return desc

    def construct_child(self, datatype, typename=None, **kwds):
        construct = getattr(datatype, 'construct', None)
        if construct:
            return construct(self, **kwds)
        return datatype(**kwds)

    def __init__(self, *, drivers, layout, maker, path, animation, **kwds):
        attributes.check(kwds, 'project')
        self.path = path

        with load.extender(self.path):
            self.maker = self.construct_child(**maker)
            self.drivers = [self.construct_child(**d) for d in drivers]
            with exception.add('Unable to create layout'):
                self.layout = self.construct_child(**layout)

            def post(d, desc):
                return self.construct_child(**desc)

            with exception.add('Unable to create animation'):
                self.animation = recurse.recurse(
                    animation,
                    pre=None,
                    post=post,
                    python_path='bibliopixel.animation')

    def make_animation(self):
        return self.animation


def project(*descs):
    desc = merge.merge(merge.DEFAULT_PROJECT, *descs)
    desc = recurse.recurse(desc)
    return construct.construct(**desc)


def read_project(location, threaded=None, default=None):
    project_data = load.data(location)
    if threaded is not None:
        project_data.setdefault('run', {})['threaded'] = threaded

    return project(default, copy.deepcopy(project_data))
