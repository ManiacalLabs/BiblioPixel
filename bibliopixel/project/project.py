import copy, gitty, functools, sys
from . import aliases, importer
from .. animation import runner
from .. project import data_maker
from .. layout.multimap import MultiMapBuilder
from .. util import files
from .. util import log

RESERVED_PROPERTIES = 'name', 'data'


def make_animation(layout, animation, run=None):
    reserved = {p: animation.pop(p, None) for p in RESERVED_PROPERTIES}
    animation = importer.make_object(layout, **animation)

    # Add the reserved properties back in.
    for k, v in reserved.items():
        (v is not None) and setattr(animation, k, v)

    animation.set_runner(runner.Runner(**(run or {})))
    return animation


def project_to_animation(desc, default):
    project = aliases.resolve(default or {}, desc)

    animation = project.pop('animation', None)
    driver = project.pop('driver', None)
    drivers = project.pop('drivers', None)
    layout = project.pop('layout', None)
    maker = project.pop('maker', None)
    path = project.pop('path', None)
    run = project.pop('run', None)

    if project:
        log.error('Did not understand sections %s', project)

    if not animation:
        raise ValueError('animation was not specified in project')

    if not layout:
        raise ValueError('layout was not specified in project')

    if not (driver or drivers):
        raise ValueError('Projects has neither driver nor drivers sections')

    gitty.sys_path.extend(path or '')
    maker = data_maker.Maker(**(maker or {}))
    make_object = functools.partial(importer.make_object, maker=maker)
    coord_map = layout.pop('coord_map', None)

    if not drivers:
        driver_objects = [make_object(**driver)]
    else:
        if driver:
            # driver is a default for each driver.
            drivers = [dict(driver, **d) for d in drivers]

        build = MultiMapBuilder(make_object)
        driver_objects = [build.make_driver(**d) for d in drivers]
        coord_map = coord_map or build.map

    layout_object = make_object(driver_objects, coord_map=coord_map, **layout)
    return make_animation(layout_object, animation, run)
