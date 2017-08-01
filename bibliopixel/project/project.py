import copy, gitty, functools, sys
from . import aliases, importer
from .. project import data_maker
from .. layout.multimap import MultiMapBuilder
from .. util import files
from .. util import log

RESERVED_PROPERTIES = 'name', 'data'

ISNT_GIT_PATH_ERROR = """\
Because the --isolate flag is set, all paths must start with //git.
Your path was %s."""


def make_animation(layout, animation, run=None):
    animation = aliases.resolve(animation)
    reserved = {p: animation.pop(p, None) for p in RESERVED_PROPERTIES}
    animation_obj = importer.make_object(layout, **animation)

    # Add the reserved properties back in.
    for k, v in reserved.items():
        animation[k] = v
        (v is not None) and setattr(animation_obj, k, v)

    animation_obj.set_runner(run)
    return animation_obj


def extend_path(path):
    if not path:
        return

    if aliases.ISOLATE:
        if not all(x.startswith('//git/') for x in path.split(':')):
            raise ValueError(ISNT_GIT_PATH_ERROR % path)

    gitty.sys_path.extend(path)


def project_to_animation(desc, default):
    project = copy.deepcopy(desc)

    def get(name):
        return project.pop(name, default.get(name))

    animation = get('animation')
    driver = get('driver')
    drivers = get('drivers')
    layout = get('layout')
    maker = get('maker')
    path = get('path')
    run = get('run')

    if project:
        log.error('Did not understand sections %s', project)

    if not animation:
        raise ValueError('animation was not specified in project')

    if not layout:
        raise ValueError('layout was not specified in project')

    if not (driver or drivers):
        raise ValueError('Projects has neither driver nor drivers sections')

    extend_path(path)
    maker = data_maker.Maker(**(maker or {}))
    make_object = functools.partial(importer.make_object, maker=maker)

    builder = MultiMapBuilder(make_object)
    driver_objects = builder.make_drivers(driver, drivers)

    layout = aliases.resolve(layout)
    coord_map = layout.pop('coord_map', builder.map or None)
    layout_object = make_object(driver_objects, coord_map=coord_map, **layout)

    return make_animation(layout_object, animation, run)
