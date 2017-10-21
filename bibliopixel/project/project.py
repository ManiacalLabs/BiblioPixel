import copy, loady, os
from . import aliases, attributes, importer, load, project2
from .. project import data_maker

RESERVED_PROPERTIES = 'name', 'data'

ISNT_GIT_PATH_ERROR = """\
Because the --isolate flag is set, all paths must start with //git.
Your path was %s."""


def make_animation(layout, animation, run=None):
    animation = aliases.resolve_section(animation)
    reserved = {p: animation.pop(p, None) for p in RESERVED_PROPERTIES}
    animation_obj = importer.make_object(
        layout, python_path='bibliopixel.animation', **animation)

    # Add the reserved properties back in.
    for k, v in reserved.items():
        animation[k] = v
        (v is not None) and setattr(animation_obj, k, v)

    animation_obj.set_runner(run)
    return animation_obj


def extend_path(path):
    parts = path.split(':')

    if aliases.ISOLATE:
        if not all(x.startswith('//git/') for x in parts):
            raise ValueError(ISNT_GIT_PATH_ERROR % path)
    else:
        parts.insert(0, os.getcwd())

    parts and loady.sys_path.extend(':'.join(parts))


def _create(*args, datatype, typename=None, **desc):
    return datatype(*args, **desc)


class Project:
    SUBOBJECTS = 'animation', 'driver', 'drivers', 'maker'

    def __init__(self, *,
                 animation=None,
                 default=None,
                 driver=None,
                 drivers=None,
                 layout=None,
                 maker=None,
                 path=None,
                 run=None,
                 **kwds):
        attributes.check(kwds, 'project')
        default = default or {}

        def resolve(name, value):
            pr = aliases.resolve_section(value)
            de = aliases.resolve_section(default.get(name))
            return dict(de, **pr)

        self.animation = resolve('animation', animation)
        self.driver = resolve('driver', driver)
        self.layout = resolve('layout', layout)
        self.path = resolve('path', path)

        self.drivers = drivers or []
        maker = maker or {}
        maker_type = maker.pop('datatype', data_maker.Maker)
        maker.pop('typename', None)
        self.maker = maker_type(**maker)

        self.path = path or default.get('path', '')
        self.run = run or default.get('run', {})

        if not self.animation:
            raise ValueError('There was no "animation" section in the project')

        if not self.layout:
            raise ValueError('There was no "layout" section in the project')

        if not (self.driver or self.drivers):
            raise ValueError(
                'The project has neither a "driver" nor a "drivers" section')

    def _make_object(self, *args, python_path=None, **kwds):
        kwds = aliases.resolve_section(kwds)
        return importer.make_object(
            *args, maker=self.maker, python_path=python_path, **kwds)

    def make_animation(self):
        extend_path(self.path)
        driver_objects = self._make_drivers()
        layout_object = self._make_object(
            driver_objects, python_path='bibliopixel.layout', **self.layout)
        return make_animation(layout_object, self.animation, self.run)

    def _make_drivers(self):
        def make_driver(d):
            return self._make_object(python_path='bibliopixel.drivers', **d)

        if not self.drivers:
            return [make_driver(self.driver)]

        if self.driver:
            # driver is a default for each driver.
            self.drivers = [dict(self.driver, **d) for d in self.drivers]

        return [make_driver(d) for d in self.drivers]


USE_NEW_PROJECTS = False


def read_project(location, threaded=None, default=None):
    project = load.data(location)
    if threaded is not None:
        project.setdefault('run', {})['threaded'] = threaded

    new_project = project2.project(default, copy.deepcopy(project))
    if USE_NEW_PROJECTS:
        return new_project

    return Project(default=default, **project)
