import os, sys
from . import merge as _merge
from .. util import data_file, log, persistent_dict

# This is set to true during testing.
BYPASS_PROJECT_DEFAULTS = False

USER_DEFAULTS_FILE = os.path.expanduser('~/.bibliopixel/default.json')
USER_DEFAULTS = persistent_dict.PersistentDict(USER_DEFAULTS_FILE)
PROJECT_DEFAULTS = []

SAVE_DIRECTORY = os.path.expanduser('~/.bibliopixel/project_defaults')


def merge(*projects):
    """
    Merge the global project defaults and the user project defaults with a list
    of projects
    """
    defaults = [_merge.DEFAULT_PROJECT]
    if not BYPASS_PROJECT_DEFAULTS:
        defaults += PROJECT_DEFAULTS or [USER_DEFAULTS]

    return _merge.merge(*(defaults + list(projects)))


def show_defaults():
    """List current user defaults in data_file format (JSON or YAML)"""
    _warn_if_empty()
    data_file.dump(USER_DEFAULTS, sys.stdout)
    log.printer()


def reset_defaults(sections):
    """Reset some or all sections of the user defaults file"""
    if _warn_if_empty():
        return
    sections = sorted(_check_sections(sections) or USER_DEFAULTS)

    log.printer('Before reset:')
    show_defaults()

    for s in sections:
        try:
            del USER_DEFAULTS[s]
        except:
            pass

    log.printer('Reset', *sections)


def set_defaults(sections):
    """
    Set user default values for one or more sections, or for an entire project
    at once.
    """
    assignments = _sections_to_assignments(sections)
    USER_DEFAULTS.update(assignments)


def load_defaults(name):
    defaults = _load_defaults(name)
    USER_DEFAULTS.clear()
    USER_DEFAULTS.update(defaults)
    log.printer('Loaded project defaults from', name)


def save_defaults(name):
    if '/' in name or '.' in name:
        path = name
    else:
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)
        path = _default_file(name)

    if os.path.exists(path):
        yn = input('Default %s already exists.  Overwrite? (y/N) ' % name)
        if not yn.lower().startswith('y'):
            return

    with open(path, 'w') as fp:
        data_file.dump(USER_DEFAULTS, fp)

    log.printer('Written project defaults to', name)


def remove_defaults(name):
    if name in _defaults():
        os.remove(_default_file(name))
    else:
        log.printer('No such default:', name)
        list_saved_defaults()


def list_saved_defaults():
    defaults = _defaults()
    if defaults:
        log.printer('Saved project defaults:')
        for i in defaults:
            log.printer('   ', i)
    else:
        log.printer('(no project defaults saved)')


def set_project_defaults(names):
    PROJECT_DEFAULTS[:] = [_load_defaults(n) for n in names]


def _check_sections(sections):
    unknown = set(sections) - set(_merge.PROJECT_SECTIONS)
    if not unknown:
        return sections

    s = '' if len(unknown) == 1 else 's'
    unknown = ' '.join(sorted(unknown))
    raise ValueError('Unknown project section%s: %s' % (s, unknown))


# Fail immediately if the user preferences contain unknown sections.
# This should only ever happen if the user edited the file by hand.
_check_sections(USER_DEFAULTS)


def _sections_to_assignments(sections):
    if not sections:
        raise ValueError('`set` called with no arguments')

    is_json = sections[0].startswith('{')
    if is_json:
        return _check_sections(data_file.loads(' '.join(sections)))

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
            value = data_file.loads(value)
        except Exception as e:
            e.args += ('Bad data in `set` for %s=%s' % (section, value),)
            raise

        *first, last = section.split('.')
        a = assignments
        for i in first:
            a = a.setdefault(i, [] if i.endswith('s') else {})
        a[last] = value

    return _check_sections(assignments)


def _warn_if_empty():
    if not USER_DEFAULTS:
        log.printer('(no entries in defaults file)', file=sys.stderr)
        return True


def _defaults():
    if not os.path.exists(SAVE_DIRECTORY):
        return []
    return [f for f in os.listdir(SAVE_DIRECTORY) if not f.startswith('.')]


def _default_file(name):
    return os.path.join(SAVE_DIRECTORY, name)


def _load_defaults(name):
    n = name
    if not os.path.exists(n):
        n = _default_file(n)
        if not os.path.exists(n):
            list_saved_defaults()
            raise ValueError('No such default: ' + name)
    try:
        return data_file.load(n)
    except Exception as e:
        e.args = ('There was an error in data file ' + name,
                  'Did you edit this file by hand?') + e.args
        raise
