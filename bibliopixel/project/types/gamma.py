import functools, numbers
from ... util.colors import gamma

NAMES = [d for d in dir(gamma) if d.isupper()]

USAGE = """
A Gamma table is represented by one of:

* A number, representing a floating gamma correction value
* A string, representing a name of a standard gamma function
* A list of up to three elements: arguments to Gamma's constructor.
* A dictionary representing arguments to Gamma's constructor.

Possible string names  are """ + ', '.join(NAMES)


@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(numbers.Number)
def _(c):
    return gamma.Gamma(c)


@make.register(str)
def _(c):
    if c not in NAMES:
        raise ValueError('Unknown gamma %s: valid names are %s' % (c, NAMES))

    return getattr(gamma, c)


@make.register(list)
@make.register(tuple)
def _(c):
    return gamma.Gamma(*c)


@make.register(dict)
def _(c):
    return gamma.Gamma(**c)
