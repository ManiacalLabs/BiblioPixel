"""
Converts its arguments between color names and color tuples.
"""


from .. project import aliases, alias_lists

DELETE_ALL_PROMPT = 'Delete all aliases - are you sure? (yN) '


def _assign(parts):
    def assign(i):
        name, equals, value = parts[i:i + 3]
        if equals != '=' or not name.isidentifier():
            raise ValueError()

        return name, value

    # Compute all the assignments first to fail early.
    assignments = [assign(i) for i in range(0, len(parts), 3)]
    for name, value in assignments:
        alias_lists.set_alias(name, value)
        print('Set:', name, '=', value)


def run(args):
    if args.delete_all:
        if args.aliases:
            raise ValueError('--delete-all takes no arguments')

        if not input(DELETE_ALL_PROMPT).lower().startswith('y'):
            raise ValueError('--delete-all aborted')

        alias_lists.delete_all_alias()
        print('All aliases deleted.')
        return

    if not args.aliases:
        alias_lists.print_aliases(args.builtin, args.by_value)
        return

    parts = ' = '.join(' '.join(args.aliases).split('=')).split()

    if '=' in parts:
        if args.delete:
            raise ValueError('Cannot --delete %s' % ' '.join(args.aliases))
        try:
            _assign(parts)
        except Exception as e:
            raise ValueError('Bad assignment %s' % ' '.join(args.aliases))

    elif args.delete:
        success = []
        for alias in parts:
            try:
                alias_lists.delete_alias(alias)
                success.append(alias)
            except:
                print('Alias', alias, 'did not exist')
        success and print('Deleted aliases:', *success)

    else:
        for alias in parts:
            value = alias_lists.get_alias(alias, aliases.ISOLATE)
            alias_lists.print_alias(alias, value)


def set_parser(parser):
    parser.set_defaults(run=run)

    parser.add_argument(
        'aliases', nargs='*',
        help='Names of aliases',
        default='')

    parser.add_argument(
        '--builtin', action='store_true',
        help='List the builtin aliases')

    parser.add_argument(
        '--by-value', action='store_true',
        help='Sort aliases by value, not name')

    parser.add_argument(
        '--delete', action='store_true',
        help='Delete one or more built-in aliases')

    parser.add_argument(
        '--delete-all', action='store_true',
        help='Delete all built-in aliases')
