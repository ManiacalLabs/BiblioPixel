import sys, json
from . defaults import apply_defaults, DEFAULTS
from . importer import make_object, import_symbol
from .. import data_maker
from .. layout import gen_matrix
from .. led.multimap import MultiMapBuilder


def make_led(driver, led, maker=None):
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
    return make_object(drivers, coordMap=coordMap, maker=maker, **led)


def make_animation(animation, **kwds):
    led = make_led(**kwds)
    animation_type = import_symbol(animation.get('typename'))
    if not getattr(animation_type, 'IS_SEQUENCE', False):
        return make_object(led, **animation)

    anim = animation_type(led)

    def add(run=None, **kwds):
        anim.add_animation(make_object(led, **kwds), **(run or {}))

    for a in animation.get('animations', ()):
        add(**a)

    return anim


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
