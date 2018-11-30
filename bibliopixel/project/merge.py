import collections
from . import construct, load

# Elements in the DEFAULT_PROJECT are listed in order of dependency: sections
# can only be dependent on sections that are above them in this list.
# For example, animation is at the bottom which are  dependent on run and
# layout, which depend on drivers, and everything depends on path and typename.
DEFAULT_PROJECT = collections.OrderedDict((
    ('aliases', {}),
    ('colors', {}),
    ('palettes', {}),
    ('path', ''),
    ('typename', 'bibliopixel.project.project.Project'),
    ('numbers', ''),
    ('maker', 'bibliopixel.project.data_maker.Maker'),
    ('driver', {}),
    ('drivers', []),
    ('shape', ()),
    ('layout', {}),
    ('run', {}),
    ('animation', {}),
    ('controls', []),
))

NOT_MERGEABLE = 'controls', 'shape', 'drivers', 'numbers', 'path', 'typename'

# datatype is added when we resolve the typename
# dimensions is a legacy section
SPECIAL_CASE = 'datatype', 'dimensions',
PROJECT_SECTIONS = tuple(DEFAULT_PROJECT.keys()) + SPECIAL_CASE

SECTION_ISNT_DICT_ERROR = 'Project section "%s" is %s, should be dictionary'
UNKNOWN_SECTION_ERROR = 'There is no Project section named "%s"'


def merge(*projects):
    """
    Merge zero or more dictionaries representing projects with the default
    project dictionary and return the result
    """
    result = {}
    for project in projects:
        for name, section in (project or {}).items():
            if name not in PROJECT_SECTIONS:
                raise ValueError(UNKNOWN_SECTION_ERROR % name)

            if section is None:
                result[name] = type(result[name])()
                continue

            if name in NOT_MERGEABLE + SPECIAL_CASE:
                result[name] = section
                continue

            if section and not isinstance(section, (dict, str)):
                cname = section.__class__.__name__
                raise ValueError(SECTION_ISNT_DICT_ERROR % (name, cname))

            if name == 'animation':
                # Useful hack to allow you to load projects as animations.
                adesc = load.load_if_filename(section)
                if adesc:
                    section = adesc.get('animation', {})
                    section['run'] = adesc.get('run', {})

            result_section = result.setdefault(name, {})
            section = construct.to_type(section)
            for k, v in section.items():
                if v is None:
                    result_section.pop(k, None)
                else:
                    result_section[k] = v
    return result
