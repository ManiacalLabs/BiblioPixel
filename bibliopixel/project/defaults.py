import json, os, sys
from . import merge as _merge
from .. util import datafile

BYPASS_PROJECT_DEFAULTS = False

USER_DEFAULTS_FILE = os.path.expanduser('~/.bibliopixel_defaults')
USER_DEFAULTS = datafile.DataFile(USER_DEFAULTS_FILE)


def merge(*projects):
    """
    Merge the global project defaults and the user project defaults with a list
    of projects
    """
    if BYPASS_PROJECT_DEFAULTS:
        defaults = (_merge.DEFAULT_PROJECT,)
    else:
        defaults = (_merge.DEFAULT_PROJECT, USER_DEFAULTS.data)
    return _merge.merge(*(defaults + projects))


def list_defaults():
    """List all user defaults in JSON format"""
    _warn_if_empty()
    json.dump(USER_DEFAULTS.data, sys.stdout, indent=2, sort_keys=True)
    print()


def reset_defaults(sections):
    """Reset some or all sections of the user defaults file"""
    if _warn_if_empty():
        return
    sections = sorted(_check_sections(sections) or USER_DEFAULTS.data)

    print('Before reset:')
    list_defaults()

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
