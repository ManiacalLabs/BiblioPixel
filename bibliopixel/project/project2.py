from . import check, fix, load, merge, recurse
from .. util import exception


class Project:
    @staticmethod
    def children(desc):
        drivers = desc['drivers']
        for i in range(len(drivers)):
            yield drivers, i, 'bibliopixel.drivers'

        yield desc, 'animation', 'bibliopixel.animation'
        yield desc, 'layout', 'bibliopixel.layout'
        yield desc, 'maker'

    def __init__(self, *, animation, drivers, layout, maker, path, run,
                 datatype=None, typename=None, **kwds):
        def create(*args, datatype, typename=None, **desc):
            return datatype(*args, **desc)

        def make_animation(desc):
            # We need to deal with legacy animations here!
            #
            # In the future, properly-formed animations will always pass
            # extra keywords back to the parent class for error reporting,
            # and for setting the two reserved properties 'name' and 'data'.
            # But existing third-party animations don't do this - so we pop
            # off the reserved properties and then add them on again after
            # construction.
            name, data = desc.pop('name', None), desc.pop('data', None)
            animation = create(self.layout, **desc)
            animation.name, animation.data = name, data
            return animation

        check.unknown(kwds, 'project', 'project')
        self.run = run
        self.path = path

        with load.extender(self.path):
            self.maker = create(**maker)
            self.drivers = [create(maker=self.maker, **d) for d in drivers]
            with exception.add('Unable to create layout'):
                self.layout = create(self.drivers, maker=self.maker, **layout)

            with exception.add('Unable to create animation'):
                self.animation = recurse.recurse(
                    animation,
                    pre=lambda x: x, post=make_animation,
                    python_path='bibliopixel.animation')

    def make_animation(self):
        return self.animation


def project(*descs):
    desc = merge.merge(*descs)
    desc = fix.fix_drivers(desc)
    desc = recurse.recurse(desc)
    desc = fix.fix_layout(desc)
    for section in 'layout', 'animation':
        if not desc.get(section, {}).get('datatype'):
            raise ValueError('Missing "%s" section' % section)

    return Project(**desc)
