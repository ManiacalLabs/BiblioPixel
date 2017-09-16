from .. drivers import ledtype
from . import run as _run

"""
Test the all_pixel.

Equivalent to
    bp --num=10 --loglevel=debug --animation=strip_test \
      --driver=serial --fail_on_exception --layout=strip  --ledtype=<argument>
"""

LEDTYPES = """
BiblioPixel currently understands the following types of LED strips:

""" + ', '.join(sorted(ledtype.LEDTYPE.__members__.keys()))

LEDTYPE_HELP = """\
The type of the LED strip that is connected to your AllPixel.
""" + LEDTYPES

NO_LED_ERROR = """No ledtype provided.
""" + LEDTYPES


ARGUMENTS = {
    'animation': 'strip_test',
    'driver': 'serial',
    'fail_on_exception': True,
    'layout': 'strip',
    'loglevel': 'debug',
    'num': 10,
}


def run(args):
    for key, value in ARGUMENTS.items():
        setattr(args, key, value)

    args.ledtype = args.ledtype or args.ledtype_arg
    if not args.ledtype:
        raise ValueError(NO_LED_ERROR)

    _run.run(args)


def set_parser(args):
    _run.set_parser(args)
    args.set_defaults(run=run)
    args.add_argument('ledtype_arg', help=LEDTYPE_HELP, default='')
