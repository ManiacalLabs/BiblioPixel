import re
from .. util import log
from . import alias_lists

ALIAS_MARKER = '@'
SEPARATORS = re.compile(r'([./#]|[^./#]+)')


# This can set from the commamnd line with --isolate
ISOLATE = False


def resolve(typename, user=None):
    def get(s):
        return alias_lists.get_alias(s, ISOLATE) or ''

    def get_all():
        for part in SEPARATORS.split(typename):
            yield get(part[1:]) if part.startswith(ALIAS_MARKER) else part

    return get(typename) or ''.join(get_all())


def resolve_section(section):
    section = section or {}

    if isinstance(section, str):
        typename, section = section, {}
    else:
        typename = section.get('typename')

    if typename:
        section['typename'] = resolve(typename)

    return section
