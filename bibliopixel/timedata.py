import sys
from . import log

try:
    import timedata as TIMEDATA
except:
    TIMEDATA = None

ENABLED = '--disable_timedata' not in sys.argv


def enabled():
    return ENABLED and TIMEDATA


def message():
    if not TIMEDATA:
        return 'No timedata library in your $PYTHONPATH.'
    return 'timedata %sabled' % ('en' if ENABLED else 'dis')


def ColorList(*arg):
    return TIMEDATA.ColorList(*arg) if enabled() else list(*arg)


def ColorList255(*arg):
    return TIMEDATA.color.rgb.c255.ColorList(*arg) if (
        enabled()) else list(*arg)


def Renderer(**kwds):
    return enabled() and TIMEDATA.Renderer(**kwds).render


log.debug(message())
