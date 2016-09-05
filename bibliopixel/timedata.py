import sys
from . import log

TIMEDATA = None
ENABLED = '--disable_timedata' not in sys.argv

try:
    import timedata as TIMEDATA
    log.info('timedata %sabled' % ('en' if ENABLED else 'dis'))
except:
    log.info('timedata not available. Using standard Python lists.')


def timedata():
    return ENABLED and TIMEDATA
