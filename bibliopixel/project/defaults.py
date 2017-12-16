import json, os, sys
from . import merge as _merge
from .. util import datafile

# This set to true during testing.
BYPASS_PROJECT_DEFAULTS = False

USER_DEFAULTS_FILE = os.path.expanduser('~/.bibliopixel_defaults')
USER_DEFAULTS = datafile.DataFile(USER_DEFAULTS_FILE)
PROJECT_DEFAULTS = None

SAVE_DIRECTORY = os.path.expanduser('~/.bibliopixel_save')


def merge(*projects):
    """
    Merge the global project defaults and the user project defaults with a list
    of projects
    """
    if BYPASS_PROJECT_DEFAULTS:
        defaults = (_merge.DEFAULT_PROJECT,)
    elif PROJECT_DEFAULTS is None:
        defaults = (_merge.DEFAULT_PROJECT, USER_DEFAULTS.data)
    else:
        defaults = (_merge.DEFAULT_PROJECT, PROJECT_DEFAULTS)

    return _merge.merge(*(defaults + projects))


def show_defaults():
    """List current user defaults in JSON format"""
    _warn_if_empty()
    json.dump(USER_DEFAULTS.data, sys.stdout, indent=2, sort_keys=True)
    print()


def reset_defaults(sections):
    """Reset some or all sections of the user defaults file"""
    if _warn_if_empty():
        return
    sections = sorted(_check_sections(sections) or USER_DEFAULTS.data)

    print('Before reset:')
    show_defaults()

    for s in sections:
        try:
            USER_DEFAULTS.delete(s)
        except:
            pass

    print('Reset', *sections)


def set_defaults(sections):
    """
    Set user default values for one or more sections, or for an entire project
    at once.
    """
    assignments = _sections_to_assignments(sections)
    USER_DEFAULTS.set_items(assignments.items())


def load_defaults(name):
    if name in _defaults():
        defaults = _load_json(name)
        USER_DEFAULTS.set_items(defaults.items())
        print('Loaded project defaults from', name)
    else:
        print('No such default:', name)
        list_saved_defaults()


def save_defaults(name):
    if name in _defaults():
        yn = input('Default', name, 'already exists.  Overwrite? (y/N) ')
        if not yn.lower().startswith('y'):
            return
    os.makedirs(SAVE_DIRECTORY, exist_ok=True)
    fp = open(_default_file(name), 'w')
    json.dump(USER_DEFAULTS.data, fp, indent=2, sort_keys=True)
    print('Written project defaults to', name)


def remove_defaults(name):
    if name in _defaults():
        os.remove(_default_file(name))
    else:
        print('No such default:', name)
        list_saved_defaults()


def list_saved_defaults():
    defaults = _defaults()
    if defaults:
        print('Saved project defaults:')
        for i in defaults:
            print('   ', i)
    else:
        print('(no project defaults saved)')


def set_project_defaults(name):
    if name not in _defaults():
        raise ValueError('No such default: ' + name)

    global PROJECT_DEFAULTS
    PROJECT_DEFAULTS = _load_json(name)


def _check_sections(sections):
    unknown = set(sections) - set(_merge.PROJECT_SECTIONS)
    if not unknown:
        return sections

    s = '' if len(unknown) == 1 else 's'
    unknown = ' '.join(sorted(unknown))
    raise ValueError('Unknown project section%s: %s' % (s, unknown))


# Fail immediately if the user preferences contain unknown sections.
# This should only ever happen if the user edited the file by hand.
_check_sections(USER_DEFAULTS.data)


def _sections_to_assignments(sections):
    if not sections:
        raise ValueError('`set` called with no arguments')

    is_json = sections[0].startswith('{')
    if is_json:
        return _check_sections(json.loads(' '.join(sections)))

    assignments = {}
    for s in sections:
        try:
            section, value = s.split('=', 1)
        except:
            raise ValueError('All arguments to `set` must contain =')

        # Help the user out a little if they use strings without quotes by
        # wrapping them in quotes.

        if value.isalpha() and (value not in ('true', 'false', 'null')):
            value = '"%s"' % value

        try:
            value = json.loads(value)
        except Exception as e:
            e.args += ('Bad JSON in `set` for %s=%s' % (section, value),)
            raise

        *first, last = section.split('.')
        a = assignments
        for i in first:
            a = a.setdefault(i, [] if i.endswith('s') else {})
        a[last] = value

    return _check_sections(assignments)


def _warn_if_empty():
    if not USER_DEFAULTS.data:
        print('(no entries in defaults file)', file=sys.stderr)
        return True


def _defaults():
    if not os.path.exists(SAVE_DIRECTORY):
        return []
    return [f for f in os.listdir(SAVE_DIRECTORY) if not f.startswith('.')]


def _default_file(name):
    return os.path.join(SAVE_DIRECTORY, name)


def _load_json(name):
    name = _default_file(name)
    try:
        return json.load(open(name))
    except Exception as e:
        e.args = ('There was a JSON error in file ' + name,
                  'Did you edit this file by hand?') + e.args
        raise
