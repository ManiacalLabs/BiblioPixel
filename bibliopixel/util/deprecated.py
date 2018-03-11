import os, sys

CHOICES = 'ignore', 'fail', 'warn', 'warn_once'
DEFAULT = 'warn_once'
ACTION = None

HELP = """
Specify what to do when a project uses deprecated features:

  ignore: do nothing
  warn: print warning messages for each feature
  warn_once: print a warning message, but only once for each type of feature
  fail: throw an exception
"""

DEPRECATED = set()
FLAG = '--deprecated'


def allowed():
    _compute_action()
    return ACTION != 'fail'


def deprecated(msg, *args, **kwds):
    _compute_action()

    if ACTION == 'ignore':
        return
    if ACTION == 'warn_once' and msg in DEPRECATED:
        return

    formatted = msg.format(*args, **kwds)
    if ACTION == 'fail':
        raise ValueError(formatted)

    DEPRECATED.add(msg)

    from . import log
    log.warning(formatted)


def _compute_action():
    global ACTION
    if ACTION:
        return

    if FLAG in sys.argv:
        raise ValueError('%s needs an argument (one of %s)' %
                         (FLAG, ', '.join(CHOICES)))

    d = [i for i, v in enumerate(sys.argv) if v.startswith(FLAG + '=')]
    if not d:
        ACTION = DEFAULT

    elif len(d) > 1:
        raise ValueError('Only one %s argument can be used' % FLAG)

    else:
        arg = sys.argv.pop(d[0])
        _, *rest = arg.split('=')

        if len(rest) > 1:
            raise ValueError('Extra = in flag %s' % arg)

        if not (rest and rest[0].strip()):
            raise ValueError('%s needs an argument (one of %s)' %
                             (FLAG, ', '.join(CHOICES)))

        if rest[0] not in CHOICES:
            raise ValueError('Unknown argument to %s (must be one of %s)' %
                             (FLAG, ', '.join(CHOICES)))
            raise ValueError('Bad deprecated value %s' % rest[0])

        ACTION = rest[0]

    return ACTION
