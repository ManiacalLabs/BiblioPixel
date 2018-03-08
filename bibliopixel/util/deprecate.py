from . import log

CHOICES = 'ignore', 'fail', 'warn', 'warn_once'
DEFAULT = 'warn'

# This gets changed by --deprecate
ACTION = DEFAULT

HELP = """
Specify what to do when a project uses deprecated features:

  ignore: do nothing
  warn: print warning messages for each feature
  warn_once: print a warning message, but only once for each type of feature
  fail: throw an exception
"""

DEPRECATED = set()


def deprecate(msg, *args, **kwds):
    if ACTION == 'ignore' or (ACTION == 'warn_once' and msg in DEPRECATED):
        return

    formatted = (msg + ' is DEPRECATED').format(*args, **kwds)
    if ACTION == 'fail':
        raise ValueError(formatted)

    DEPRECATED.add(msg)
    log.warning(formatted)
