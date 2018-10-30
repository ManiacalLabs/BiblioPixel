import functools

NAMES = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0),
}


@functools.singledispatch
def make(c):
    raise ValueError(ERROR % c)


@make.register(str)
def _(c):
    items = [v for k, v in NAMES.items() if k.startswith(c)]
    if len(items) != 1:
        raise ValueError(ERROR % c)
    return items[0]


@make.register(tuple)
def _(c):
    if c not in NAMES.values():
        raise ValueError(ERROR % (c,))
    return c


@make.register(list)
def _(c):
    return make(tuple(c))


USAGE = """Direction values can be
* a string 'up', 'down', 'left', 'right', or
* a string prefix like 'u' or 'ri'
* one of four numeric pairs (0, -1), (0, 1), (-1, 0), (1, 0).
"""

ERROR = 'Don\'t understand direction "%s"\n' + USAGE
