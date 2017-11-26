from .. util import log
from . import construct

DEFAULT_PROJECT = {
    'animation': {},
    'driver': {},
    'drivers': [],
    'layout': {},
    'maker': 'bibliopixel.project.data_maker.Maker',
    'path': '',
    'run': {},
    'typename': 'bibliopixel.project.project.Project',
}


def merge(*projects):
    """
    Merge zero or more dictionaries representing projects with the default
    project dictionary and return the result
    """
    result = {}
    for project in projects:
        for name, section in (project or {}).items():
            if name in ('drivers', 'path', 'typename'):
                result[name] = section
            else:
                result.setdefault(name, {}).update(construct.to_type(section))

    return result
