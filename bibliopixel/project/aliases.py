import re
from .. util import log
from . import alias_lists

ALIAS_MARKERS = '@$'
SEPARATORS = re.compile(r'([./#]|[^./#]+)')


def resolve(typename, aliases=None):
    aliases = aliases or {}

    def get(s):
        return aliases.get(s) or alias_lists.get_alias(s) or s

    def get_all(typename):
        for part in SEPARATORS.split(typename):
            is_alias = part and (part[0] in ALIAS_MARKERS)
            yield get(part[1:]) if is_alias else part

    return ''.join(get_all(get(typename)))
