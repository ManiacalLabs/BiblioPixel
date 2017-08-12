import re
from .. util import log
from . importer import import_symbol
from . import alias_lists

ALIAS_MARKER = '$'
SEPARATORS = re.compile(r'[./#]|[^./#]+')
DEPRECATE_OLD_ALIASES = False

# This can set from the commamnd line with --isolate
ISOLATE = False


def resolve_one(part):
    if not part.startswith(ALIAS_MARKER):
        return part

    p = alias_lists.get_alias(part[1:], ISOLATE)
    if p:
        return p

    raise ValueError('Do not understand alias %s' % part)


def resolve(value):
    if isinstance(value, str):
        typename, value = value, {}
    else:
        typename = value.get('typename')
        if not typename:
            return value

    alias = alias_lists.get_alias(typename, ISOLATE)

    if alias:
        if DEPRECATE_OLD_ALIASES:
            log.warning('Aliases that do not start with $ are deprecated')

    else:
        parts = SEPARATORS.findall(typename)
        alias = ''.join(resolve_one(p) for p in parts)

    value['typename'] = alias
    return value
