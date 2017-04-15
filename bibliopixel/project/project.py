import sys, json
from . defaults import apply_defaults, DEFAULTS
from . importer import make_object
from .. import data_maker
from .. layout import gen_matrix
from .. led.multimap import MultiMapBuilder


def make_animation(driver, led, animation, maker=None):
    maker = data_maker.Maker(**(maker or {}))
    drivers = []

    def multi_drivers(device_ids, width, height, serpentine=False, **kwds):
        build = MultiMapBuilder()

        for id in device_ids:
            build.addRow(gen_matrix(width, height, serpentine=serpentine))
            d = make_object(width=width, height=height, deviceID=id, **kwds)
            drivers.append(d)

        return build.map

    def make_drivers(multimap=False, **kwds):
        if multimap:
            return multi_drivers(**kwds)

        drivers.append(make_object(**kwds))

    coordMap = make_drivers(maker=maker, **driver)
    led = make_object(drivers, coordMap=coordMap, maker=maker, **led)
    return make_object(led, **animation)


def make_runnable(run=None, **kwds):
    animation = make_animation(**kwds)
    return lambda: animation.run(**(run or {}))


def fix_desc(desc):
    if isinstance(desc, str):
        try:
            desc = open(desc).read()
        except:
            pass
        desc = json.loads(desc)

    return apply_defaults(desc)


def run(desc):
    make_runnable(**fix_desc(desc))()


if __name__ == '__main__':
    run(*sys.argv[1:])
