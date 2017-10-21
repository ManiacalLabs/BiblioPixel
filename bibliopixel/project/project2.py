from . import attributes, fix, load, merge, recurse, run_animation
from . construct import construct, construct_reserved
from .. util import exception


class Project:
    fix_children = staticmethod(run_animation.fix)

    @staticmethod
    def children(desc):
        drivers = desc['drivers']
        for i in range(len(drivers)):
            yield i, drivers, 'bibliopixel.drivers'

        yield 'maker', desc
        yield 'run_animation', desc, 'bibliopixel.animation'
        yield 'layout', desc, 'bibliopixel.layout'

    def __init__(self, *, drivers, layout, maker, path, run_animation, **kwds):
        def make_animation(datatype, desc):
            return construct_reserved(self.layout, **desc)

        attributes.check(kwds, 'project')
        self.path = path

        with load.extender(self.path):
            self.maker = construct(**maker)
            self.drivers = [construct(maker=self.maker, **d) for d in drivers]
            with exception.add('Unable to create layout'):
                self.layout = construct(
                    self.drivers, maker=self.maker, **layout)

            with exception.add('Unable to create animation'):
                self.animation = recurse.recurse(
                    run_animation,
                    post=make_animation,
                    python_path='bibliopixel.animation').runnable_animation()

    def make_animation(self):
        return self.animation


def project(*descs):
    desc = merge.merge(*descs)
    fix.fix_drivers(desc)
    desc = recurse.fix(desc)
    fix.fix_layout_and_animation(desc)

    return construct(**desc)
