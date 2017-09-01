import copy, loady, functools
from . import aliases, check, importer
from .. project import data_maker

RESERVED_PROPERTIES = 'name', 'data'

ISNT_GIT_PATH_ERROR = """\
Because the --isolate flag is set, all paths must start with //git.
Your path was %s."""


def make_animation(layout, animation, run=None):
    animation = aliases.resolve_section(animation)
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

    loady.sys_path.extend(path)


def project_to_animation(desc, default=None):
    project = copy.deepcopy(desc)
    default = default or {}

    def resolve_section_aliases(name):
        pr = aliases.resolve_section(project.pop(name, {}))
        de = aliases.resolve_section(default.get(name, {}))
        return dict(de, **pr)

    animation = resolve_section_aliases('animation')
    driver = resolve_section_aliases('driver')
    layout = resolve_section_aliases('layout')

    drivers = project.pop('drivers', [])
    maker = project.pop('maker', {})
    path = project.pop('path', default.get('path'))
    run = project.pop('run', default.get('run', {}))

    check.unknown(project, 'section', 'project')

    if not animation:
        raise ValueError('There was no "animation" section in the project')

    if not layout:
        raise ValueError('There was no "layout" section in the project')

    if not (driver or drivers):
        raise ValueError(
            'The project has neither a "driver" nor a "drivers" section')

    extend_path(path)
    maker = data_maker.Maker(**(maker or {}))
    make_object = functools.partial(importer.make_object, maker=maker)

    driver_objects = make_drivers(driver, drivers, make_object)
    layout_object = make_object(driver_objects, **layout)
    return make_animation(layout_object, animation, run)


def make_drivers(driver, drivers, make_object):
    if not drivers:
        return [make_object(**aliases.resolve_section(driver))]

    if driver:
        # driver is a default for each driver.
        drivers = [dict(driver, **d) for d in drivers]

    return [make_object(**aliases.resolve_section(d)) for d in drivers]


def read_project(location, threaded=True, default=None):
    project = loady.data.load(location, use_json=True)
    if threaded is not None:
        project.setdefault('run', {})['threaded'] = threaded
    return project_to_animation(project, default)
