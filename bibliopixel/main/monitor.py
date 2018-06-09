"""
Monitor a control source
"""

import sys
from .. project import importer
from .. util import log


def run(args):
    control = args.control[0]
    try:
        tc = importer.import_symbol(control, 'bibliopixel.control')
    except:
        log.error('Do not understand control "%s"', control)
        raise

    control_object = tc(pre_routing='()')
    control_object.set_root(log.printer)

    control_object.start()
    control_object.wait()


def set_parser(parser):
    parser.add_argument(
        'control', nargs=1,
        help='Name of a control to monitor')

    parser.set_defaults(run=run)
