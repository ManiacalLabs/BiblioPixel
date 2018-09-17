"""
Test the all_pixel
"""

from .. drivers import ledtype
from .. util import log
from bibliopixel.animation.tests import StripChannelTest
from bibliopixel.layout.strip import Strip
from bibliopixel.drivers.serial import Serial
from bibliopixel.project.types import ledtype

DESCRIPTION = """
Equivalent to

.. code-block:: bash

    bp --num=10 --loglevel=debug --animation=strip_test --driver=serial \
      --fail_on_exception --layout=strip --ledtype=<argument>

"""

LEDTYPES = """
BiblioPixel currently understands the following types of LED strips:

""" + ', '.join(sorted(ledtype.LEDTYPE.__members__.keys()))

LEDTYPE_HELP = """\
The type of the LED strip that is connected to your AllPixel
""" + LEDTYPES

NO_LED_ERROR = """ERROR: No ledtype provided
""" + LEDTYPES


def run(args):
    if not args.ledtype:
        log.error(NO_LED_ERROR)
        return -1

    log.set_log_level('DEBUG')

    driver = Serial(ledtype=ledtype.make(args.ledtype), num=10)
    layout = Strip([driver])
    animation = StripChannelTest(layout)
    animation._set_runner(None)
    animation.start()


def set_parser(args):
    args.set_defaults(run=run)
    args.add_argument('ledtype', help=LEDTYPE_HELP, nargs='?')
