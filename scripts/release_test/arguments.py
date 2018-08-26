import argparse, common, sys, tests
from features import check_features, get_features, FEATURES


def arguments(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    names = [t.__name__.split('.')[1] for t in tests.__all__]
    names = ', '.join(names)

    parser.add_argument(
        'tests', nargs='*',
        help='The list of tests to run.  Tests are:' + names)

    features = ', '.join(FEATURES)
    parser.add_argument(
        '--features', '-f', default=[], action='append',
        help='A list of features separated by colons.  Features are: ' +
        features)

    args = parser.parse_args(argv)

    if args.tests:
        all_tests = [(t, getattr(tests, t, None)) for t in args.tests]
        bad_tests = [t for (t, a) in all_tests if a is None]
        if bad_tests:
            raise ValueError('Bad test names: ' + ', '.join(bad_tests))
        all_tests = tuple(a for (t, a) in all_tests)
    else:
        all_tests = tests.__all__

    if args.features:
        features = set(':'.join(args.features).split(':'))
        check_features(features)

    else:
        features = get_features()

    return all_tests, features


if __name__ == '__main__':
    common.printer(arguments())
