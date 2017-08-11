import copy, loady, functools, sys
from . import aliases, importer
from .. project import data_maker
from .. layout.multimap import MultiMapBuilder
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

    loady.sys_path.extend(path)


def raise_if_unknown(items, name, value):
    if items:
        msg = ', '.join('"%s"' % s for s in sorted(items))
        s = '' if len(items) == 1 else 's'
        raise ValueError('Unknown %s%s for %s: %s' % (name, s, value, msg))


def raise_if_unknown_attributes(items, name, value):
    value = '%s %s' % (name, value.__class__.__name__)
    raise_if_unknown(items, 'attribute', value)


def project_to_animation(desc, default=None):
    project = copy.deepcopy(desc)
    default = default or {}

    def get(name):
        pr = aliases.resolve(project.pop(name, {}))
        de = aliases.resolve(default.get(name, {}))
        return dict(de, **pr)

    animation = get('animation')
    driver = get('driver')
    layout = get('layout')

    drivers = project.pop('drivers', [])
    maker = project.pop('maker', {})
    path = project.pop('path', default.get('path'))
    run = project.pop('run', {})

    raise_if_unknown(project, 'section', 'project')

    if not animation:
        raise ValueError('There was no "animation" section in the project')

    if not layout:
        raise ValueError('There was no "layout" section in the project')

    if not (driver or drivers):
        raise ValueError(
            'The project has neither a "driver" nor a "drivers" sections')

    extend_path(path)
    maker = data_maker.Maker(**(maker or {}))
    make_object = functools.partial(importer.make_object, maker=maker)

    builder = MultiMapBuilder(make_object)
    driver_objects = builder.make_drivers(driver, drivers)
    layout = aliases.resolve(layout)
    coord_map = layout.pop('coord_map', builder.map or None)
    if coord_map:
        layout['coord_map'] = coord_map
    layout_object = make_object(driver_objects, **layout)

    return make_animation(layout_object, animation, run)


def read_project(location, threaded=True, default=None):
    project = loady.data.load(location, json=True)
    if threaded is not None:
        project.setdefault('run', {})['threaded'] = threaded
    return project_to_animation(project, default)
