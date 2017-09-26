import loady, os
from . import aliases, check, importer
from .. project import data_maker

RESERVED_PROPERTIES = 'name', 'data'

ISNT_GIT_PATH_ERROR = """\
Because the --isolate flag is set, all paths must start with //git.
Your path was %s."""


def make_animation(layout, animation, run=None):
    animation = aliases.resolve_section(animation)
    reserved = {p: animation.pop(p, None) for p in RESERVED_PROPERTIES}
    animation_obj = importer.make_object(
        layout, base_path='bibliopixel.animation', **animation)

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


class Project:
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
        check.unknown(kwds, 'section', 'project')
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
        self.maker = data_maker.Maker(**(maker or {}))

        self.path = path or default.get('path', '')
        self.run = run or default.get('run', {})

        if not self.animation:
            raise ValueError('There was no "animation" section in the project')

        if not self.layout:
            raise ValueError('There was no "layout" section in the project')

        if not (self.driver or self.drivers):
            raise ValueError(
                'The project has neither a "driver" nor a "drivers" section')

    def make_object(self, *args, base_path=None, **kwds):
        kwds = aliases.resolve_section(kwds)
        return importer.make_object(
            *args, maker=self.maker, base_path=base_path, **kwds)

    def make_animation(self):
        extend_path(self.path)
        driver_objects = self.make_drivers()
        layout_object = self.make_object(
            driver_objects, base_path='bibliopixel.layout', **self.layout)
        return make_animation(layout_object, self.animation, self.run)

    def make_drivers(self):
        def make_object(d):
            return self.make_object(base_path='bibliopixel.drivers', **d)

        if not self.drivers:
            return [make_object(self.driver)]

        if self.driver:
            # driver is a default for each driver.
            self.drivers = [dict(self.driver, **d) for d in self.drivers]

        return [make_object(d) for d in self.drivers]


def read_project(location, threaded=True, default=None):
    project = loady.data.load(location, use_json=True)
    if threaded is not None:
        project.setdefault('run', {})['threaded'] = threaded
    return Project(default=default, **project).make_animation()
