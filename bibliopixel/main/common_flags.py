from .. util import deprecated, log


def add_arguments(parser):
    log.add_arguments(parser)
    deprecated.add_arguments(parser)
