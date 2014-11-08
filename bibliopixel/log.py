import logging
from logging import DEBUG, INFO, WARNING, CRITICAL, ERROR
import sys

class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)

logger = logging.getLogger("BiblioPixel")

def setLogLevel(level):
   global logger
   logger.setLevel(level)

def __setup_custom_logger():
    formatter = logging.Formatter(fmt='%(levelname)s - %(module)s - %(message)s')

    global logger

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

__setup_custom_logger()