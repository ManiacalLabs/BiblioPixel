import sys

timedata = None
ColorList = list

if '--disable_timedata' in sys.argv:
    log.info("timedata disabled, using standard Python lists")
else:
    try:
        import timedata
        ColorList = timedata.ColorList
        log.info('Using timedata')
    except:
        log.info('timedata not available. Using standard Python lists')
