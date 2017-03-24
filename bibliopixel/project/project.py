import sys, json
from . defaults import apply_defaults, DEFAULTS
from .. util.importer import make_object
from .. import data_maker
from .. led.multimap import MultiMapBuilder
from .. layout import gen_matrix


def multi_drivers(device_ids, width, height, serpentine=False, **kwds):
    build = MultiMapBuilder()
    drivers = []

    for id in device_ids:
        build.addRow(gen_matrix(width, height, serpentine=serpentine))
        d = make_object(width=width, height=height, deviceID=id, **kwds)
        drivers.append(d)

    return drivers, build.map


def make_drivers(multimap=False, **kwds):
    return multi_drivers(**kwds) if multimap else ([make_object(**kwds)], None)


class Project(object):
    def __init__(self, driver, led, animation, run, maker):
        self.run_arguments = run
        self.maker = data_maker.Maker(**maker)
        self.drivers, coordMap = make_drivers(maker=self.maker, **driver)
        if coordMap:
            self.led = make_object(
                self.drivers, coordMap=coordMap, maker=self.maker, **led)
        else:
            self.led = make_object(self.drivers, maker=self.maker, **led)

        self.animation = make_object(self.led, **animation)

    def run(self):
        return self.animation.run(**self.run_arguments)


def make(desc):
    if isinstance(desc, str):
        try:
            desc = open(desc).read()
        except:
            pass
        desc = json.loads(desc)

    desc = apply_defaults(desc)
    return Project(**desc)


def run(desc):
    return make(desc).run()


if __name__ == '__main__':
    run(*sys.argv[1:])
