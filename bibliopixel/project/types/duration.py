import functools, numbers
from ... util import duration


USAGE = """
A time can be initialized with:

* A number that is greater than or equal to zero, representing a time in
  seconds.

* A string:

2 weeks, 1 day, 1 hours, 3 minutes, 45 seconds, 340.4ms..."""


@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(numbers.Number)
def _(t):
    if t < 0:
        raise ValueError('Times must not be negative', USAGE)
    return t


@make.register(str)
def _(s):
    return duration.parse(s)
