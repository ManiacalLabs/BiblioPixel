import collections
from . import construct

# Elements in the DEFAULT_PROJECT are listed in order of dependency: sections
# can only be dependent on sections that are above them in this list.
# For example, animation is at the bottom which are  dependent on run and
# layout, which depend on drivers, and everything depends on path and typename.
DEFAULT_PROJECT = collections.OrderedDict((
    ('aliases', {}),
    ('path', ''),
    ('typename', 'bibliopixel.project.project.Project'),
    ('numbers', 'python'),
    ('maker', 'bibliopixel.project.data_maker.Maker'),
    ('driver', {}),
    ('drivers', []),
    ('shape', ()),
    ('layout', {}),
    ('run', {}),
    ('animation', {}),
    ('controls', []),
))
PROJECT_SECTIONS = tuple(DEFAULT_PROJECT.keys())

NOT_MERGEABLE = (
    'controls', 'datatype', 'dimensions', 'shape', 'drivers', 'numbers', 'path',
    'typename')

SECTION_ISNT_DICT_ERROR = 'Project section "%s" is %s, should be dictionary'


def merge(*projects):
    """
    Merge zero or more dictionaries representing projects with the default
    project dictionary and return the result
    """
    result = {}
    for project in projects:
        for name, section in (project or {}).items():
            if name in NOT_MERGEABLE:
                result[name] = section
            elif section and not isinstance(section, (dict, str)):
                cname = section.__class__.__name__
                raise ValueError(SECTION_ISNT_DICT_ERROR % (name, cname))
            else:
                result.setdefault(name, {}).update(construct.to_type(section))

    return result
