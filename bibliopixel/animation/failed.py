import traceback
from .. util import log
from . import animation


class Failed(animation.Animation):
    """
    An animation that's created when we fail to load or construct the
    animation that was originally specified
    """

    def __init__(self, layout, desc, exception):
        super().__init__(layout)
        self._set_runner({})
        log.error('Unable to create animation for %s', desc)
        debug = log.get_log_level() <= log.DEBUG
        msg = traceback.format_exc() if debug else str(exception)
        log.error('\n%s', msg)
        self.desc = desc
        self.exception = exception
        self.empty = True
