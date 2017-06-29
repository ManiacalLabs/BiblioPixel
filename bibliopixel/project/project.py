import gitty, sys
from . import aliases, importer
from . types.defaults import FIELD_TYPES
from .. animation import runner
from .. import data_maker
from .. layout.geometry import gen_matrix
from .. layout.multimap import MultiMapBuilder
from .. util import files


def _make_object(*args, field_types=FIELD_TYPES, **kwds):
    return importer.make_object(*args, field_types=field_types, **kwds)


def _make_layout(driver, layout, maker=None):
    maker = data_maker.Maker(**(maker or {}))
    drivers = []

    def multi_drivers(device_ids, width, height, serpentine=False, **kwds):
        build = MultiMapBuilder()

        for id in device_ids:
            build.addRow(gen_matrix(width, height, serpentine=serpentine))
            d = _make_object(width=width, height=height, deviceID=id, **kwds)
            drivers.append(d)

        return build.map

    def make_drivers(multimap=False, **kwds):
        if multimap:
            return multi_drivers(**kwds)

        drivers.append(_make_object(**kwds))

    coordMap = make_drivers(maker=maker, **driver)
    return _make_object(drivers, coordMap=coordMap, maker=maker, **layout)


def make_animation(layout, animation, run=None):
    animation = _make_object(layout, **animation)
    animation.set_runner(runner.Runner(**(run or {})))
    return animation


def _make_project(path=None, animation=None, run=None, **kwds):
    gitty.sys_path.extend(path)
    layout = _make_layout(**kwds)
    return make_animation(layout, animation or {}, run or {})


def project_to_animation(desc, default):
    project = aliases.resolve(default or {}, desc)
    return _make_project(**project)
