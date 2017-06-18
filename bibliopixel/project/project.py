import gitty, json, os, sys
from . import defaults
from . importer import make_object
from .. animation import runner
from .. import data_maker
from .. layout import gen_matrix
from .. led.multimap import MultiMapBuilder
from .. util import files
from .. drivers.serial import codes


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


def make_animation(led, animation, run=None):
    animation = make_object(led, **animation)
    animation.set_runner(runner.Runner(**(run or {})))
    return animation


def project_to_animation(*, path=None, **project):
    gitty.sys_path.extend(path)

    kwds = defaults.apply_defaults(project)
    animation = kwds.pop('animation', {})
    run = kwds.pop('run', {})
    led = make_led(**kwds)
    return make_animation(led, animation, run)


def apply_defaults(project, defaults):
    # TODO: consolidate with bp.project.defaults.
    for k, v in defaults.items():
        if k == 'ledtype' or not v:
            continue

        if k not in project:
            project[k] = v

        else:
            existing = project[k]
            if 'typename' not in existing:
                try:
                    existing['typename'] = v
                except:
                    pass

    ledtype = defaults.get('ledtype')
    if ledtype:
        if 'led' not in project:
            project['led'] = {}

        if 'type' not in project['led']:
            project['led']['type'] = ledtype
            # The field in LED should probably be renamed "ledtype" to be
            # consistent across the whole system.


def project_to_runnable(project, defaults=None):
    apply_defaults(project, defaults or {})
    return project_to_animation(**project).start


def run(s, is_filename=True, defaults=None):
    project = files.read_json(s, is_filename)
    runnable = project_to_runnable(project, defaults)
    runnable()
