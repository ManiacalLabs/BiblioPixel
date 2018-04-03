import signal
from . import log

RESTART_REQUESTED = False


def restarter(target, shutdown_function):
    def restart(signum, frame):
        global RESTART_REQUESTED
        RESTART_REQUESTED = True
        shutdown_function()
        log.debug('bp restart requested')

    signal.signal(signal.SIGHUP, restart)

    try:
        while True:
            target()
            if not RESTART_REQUESTED:
                break
            log.info('bp restarting')

    finally:
        signal.signal(signal.SIGHUP, signal.SIG_DFL)
