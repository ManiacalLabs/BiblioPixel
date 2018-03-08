from . import log

WARN_ON_DEPRECATED = False
DEPRECATED = set()


def deprecate(msg, *args, **kwds):
    if not WARN_ON_DEPRECATED or msg in DEPRECATED:
        return

    DEPRECATED.add(msg)
    log.warn(msg.format(*args, **kwds))
