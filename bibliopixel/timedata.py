import sys
from . import log

try:
    import timedata as TIMEDATA
except:
    TIMEDATA = None

ENABLED = '--disable_timedata' not in sys.argv



def message():
    if not TIMEDATA:
        return 'No timedata library in your $PYTHONPATH.'
    return 'timedata %sabled' % ('en' if ENABLED else 'dis')


def ColorList(*arg):
    return TIMEDATA.ColorList(*arg) if ENABLED and TIMEDATA else list(*arg)


def ColorList255(*arg):
    return TIMEDATA.color.rgb.c255.ColorList(*arg) if (
        ENABLED and TIMEDATA) else list(*arg)


def Renderer(**kwds):
    return ENABLED and TIMEDATA and TIMEDATA.Renderer(**kwds).render


log.info(message())
