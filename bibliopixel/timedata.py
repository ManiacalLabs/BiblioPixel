import sys
from . import log

TIMEDATA = None
ENABLED = '--disable_timedata' not in sys.argv

if sys.version_info[0] > 2:
    try:
        import timedata as TIMEDATA
    except:
        pass

if TIMEDATA:
    log.info('timedata %sabled' % ('en' if ENABLED else 'dis'))
else:
    log.info('timedata not available.')

def timedata():
    return ENABLED and TIMEDATA
