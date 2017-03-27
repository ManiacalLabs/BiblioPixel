import logging, sys
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_NAMES = {'debug': DEBUG, 'info': INFO, 'warning': WARNING, 'error': ERROR,
             'critical': CRITICAL}


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (DEBUG, INFO)


def _new_custom_logger(name='BiblioPixel',
                       fmt='%(levelname)s - %(module)s - %(message)s'):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt=fmt)

    if not logger.handlers:
        logger.setLevel(INFO)
        h1 = logging.StreamHandler(sys.stdout)
        h1.setLevel(DEBUG)
        h1.addFilter(InfoFilter())
        h1.setFormatter(formatter)

        h2 = logging.StreamHandler(sys.stderr)
        h2.setLevel(WARNING)
        h2.setFormatter(formatter)

        logger.addHandler(h1)
        logger.addHandler(h2)

    else:  # pragma: no cover
        pass

    return logger


def set_log_level(level):
    if isinstance(level, str):
        level = LOG_NAMES[level]

    logger.setLevel(level)


logger = _new_custom_logger()

setLogLevel = set_log_level

debug, info, warning, error, critical, exception = (
    logger.debug, logger.info, logger.warning, logger.error, logger.critical,
    logger.exception)
