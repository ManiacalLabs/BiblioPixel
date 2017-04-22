import sys, json
from . aliases import resolve_aliases
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


def make_runnable(**kwds):
    def make(run=None, **kwds):
        animation = make_animation(**kwds)
        return lambda: animation.run(**(run or {}))

    return make(**apply_defaults(kwds))


def read_json(s):
    try:
        return json.load(open(s))
    except:
        return json.loads(s)


def run(s):
    make_runnable(**read_json(s))()


if __name__ == '__main__':
    run(*sys.argv[1:])
