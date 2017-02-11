import sys
from . importer import make_object
from . read_dict import read_dict
from .. import data_maker
from .. led.multimap import MultiMapBuilder
from .. layout import gen_matrix


def make_drivers(multimap=False, **kwds):
    def multi(device_ids, width, height, serpentine=False, **kwds):
        build = MultiMapBuilder()
        drivers = []

        for id in device_ids:
            build.addRow(gen_matrix(width, height, serpentine=serpentine))
            d = make_object(width=width, height=height, deviceID=id, **kwds)
            drivers.append(d)

        return drivers, build.map

    return multi(**kwds) if multimap else ([make_object(**kwds)], None)


class Project(object):
    def __init__(self, driver, led, animation, run, maker=None):
        self.maker = data_maker.Maker(**(maker or {}))
        self.drivers, coordMap = make_drivers(maker=self.maker, **driver)
        if coordMap:
            self.led = make_object(
                self.drivers, coordMap=coordMap, maker=self.maker, **led)
        else:
            self.led = make_object(self.drivers, maker=self.maker, **led)

        self.animation = make_object(self.led, **animation)
        self.run = lambda: self.animation.run(**run)


def run(data):
    return Project(**read_dict(data)).run()


if __name__ == '__main__':
    run(*sys.argv[1:])
