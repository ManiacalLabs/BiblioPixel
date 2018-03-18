"""
Monitor a control source
"""

import sys
from .. project import importer
from .. util import log


def run(args):
    try:
        tc = importer.import_module(args.control[0], 'bibliopixel.control')
    except:
        log.error('Do not understand control "%s"', args.control[0])
        raise

    try:
        main = tc.main
    except:
        log.error('No main() function for control "%s"', args.control)
        raise

    main()


def set_parser(parser):
    parser.add_argument(
        'control', nargs=1,
        help='Name of a control to monitor')

    parser.set_defaults(run=run)
