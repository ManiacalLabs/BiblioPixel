import argparse
from .. util import deprecated, log

ARGS = None


def set_args(description, argv, *argument_addders):
    parser = argparse.ArgumentParser(description=description)
    for adder in (deprecated, log) + argument_addders:
        adder.add_arguments(parser)

    global ARGS
    ARGS = parser.parse_args(argv)
    log.apply_args(ARGS)
    return ARGS
