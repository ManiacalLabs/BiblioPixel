import logging, sys

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


def _new_custom_logger(name='BiblioPixel',
                       fmt='%(levelname)s - %(module)s - %(message)s'):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt=fmt)

    if len(logger.handlers) == 0:
        logger.setLevel(logging.INFO)
        h1 = logging.StreamHandler(sys.stdout)
        h1.setLevel(logging.DEBUG)
        h1.addFilter(InfoFilter())
        h1.setFormatter(formatter)

        h2 = logging.StreamHandler(sys.stderr)
        h2.setLevel(logging.WARNING)
        h2.setFormatter(formatter)

        logger.addHandler(h1)
        logger.addHandler(h2)

    return logger


logger = _new_custom_logger()

setLogLevel = logger.setLevel

debug, info, warning, error, critical, exception = (
    logger.debug, logger.info, logger.warning, logger.error, logger.critical,
    logger.exception)
