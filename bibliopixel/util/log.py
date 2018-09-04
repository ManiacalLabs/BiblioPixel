import logging, sys
from logging import DEBUG, INFO, WARNING, ERROR

FRAME = DEBUG - 5
LOG_NAMES = {'frame': FRAME, 'debug': DEBUG, 'info': INFO, 'warning': WARNING,
             'error': ERROR}

SORTED_NAMES = tuple(k for k, v in sorted(LOG_NAMES.items()))


# From https://stackoverflow.com/a/35804945/43839
def _addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError(
            '{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError(
            '{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError(
            '{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def _new_custom_logger(name='BiblioPixel',
                       fmt='%(levelname)s - %(module)s - %(message)s'):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt=fmt)

    def add_handler(level, outfile):
        class Filter(logging.Filter):
            def filter(self, rec):
                return rec.levelno == level

        h = logging.StreamHandler(outfile)
        h.setLevel(level)
        h.addFilter(Filter())
        h.setFormatter(formatter)
        logger.addHandler(h)

    if not logger.handlers:
        logger.setLevel(INFO)
        add_handler(FRAME, sys.stdout)
        add_handler(DEBUG, sys.stdout)
        add_handler(INFO, sys.stdout)
        add_handler(WARNING, sys.stderr)
        add_handler(ERROR, sys.stderr)

    else:  # pragma: no cover
        pass

    return logger


def set_log_level(level):
    """
    :param level: the level to set - either a string level name from
                  'frame', 'debug', 'info', 'warning', 'error'
                  or an integer log level from:
                  log.FRAME, log.DEBUG, log.INFO, log.WARNING, log.ERROR
    """
    if isinstance(level, str):
        level = LOG_NAMES[level.lower()]

    logger.setLevel(level)


def get_log_level():
    return logger.getEffectiveLevel()


def is_debug():
    return get_log_level() <= DEBUG


# Add a new logging level FRAME for messages which appear on every frame.
_addLoggingLevel('FRAME', FRAME)
logger = _new_custom_logger()

frame, debug, info, warning, error = (
    logger.frame, logger.debug, logger.info, logger.warning, logger.error)


# The function `printer` emits text no matter what the loglevel, and without any
# introducers like "INFO".  By default this is the same as the global `print` -
# re-assign this variable if you need to redirect your printing.
printer = print  # noqa: T001, T002


from . import deprecated

if deprecated.allowed():  # pragma: no cover
    def setLogLevel(level):
        deprecated.deprecated('util.setLogLevel')
        set_log_level(level)
