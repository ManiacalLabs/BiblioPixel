from .. project import construct
from . driver_base import DriverBase

import copy


class Mirror(DriverBase):
    @staticmethod
    def pre_recursion(desc):
        if 'drivers' not in desc:
            raise ValueError('MirrorDriver must have a drivers section')

        DriverBase.pre_recursion(desc)

        old_desc, desc = desc, {}
        for name in 'typename', 'datatype', 'drivers':
            value = old_desc.pop(name, None)
            if value is not None:
                desc[name] = value

        desc['drivers'] = [construct.to_type(d) for d in desc['drivers']]
        desc['drivers'] = [dict(d, **old_desc) for d in desc['drivers']]
        desc['num'] = old_desc['num']
        return desc

    CHILDREN = 'drivers',

    def __init__(self, num=0, *, drivers, **kwds):
        super().__init__(num, **kwds)
        self.drivers = drivers

        def forward(name):
            def method(*args, **kwds):
                for d in self.drivers:
                    getattr(d, name)(*args, **kwds)

            return method

        self.cleanup = forward('cleanup')
        self.set_colors = forward('set_colors')
        self.set_pixel_positions = forward('set_pixel_positions')
        self.start = forward('start')
        self.sync = forward('sync')
        self.update_colors = forward('update_colors')


from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    MirrorDriver = Mirror
