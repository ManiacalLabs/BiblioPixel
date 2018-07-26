"""
Toggle between color names and color tuples
"""

from .. util import colors, log


def run(args):
    if args.list:
        log.printer(*sorted(colors.COLOR_DICT.items()), sep='\n')

    if not args.colors:
        if not args.list:
            raise ValueError('No colors supplied!')

    failures = []
    for c in args.colors:
        try:
            log.printer(c, colors.toggle(c), sep=': ')
        except Exception as e:
            failures.append(c)
    if failures:
        s = '' if len(failures) == 1 else 's'
        failures = ', '.join('"%s"' % f for f in failures)
        raise ValueError('Did not understand color%s %s' % (s, failures))


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument(
        'colors', nargs='*',
        help='Color names or tuples',
        default='')

    parser.add_argument(
        '-l', '--list', action='store_true',
        help='List all the colors')
