import common


def run():
    from . import __all__
    common.printer('\n', *__all__)
