from .. util import class_name, log


class LogErrors:
    """
    Wraps a function call to catch and report exceptions.
    """

    def __init__(self, function, max_errors=-1):
        """
        :param function: the function to wrap
        :param int max_errors: if ``max_errors`` is non-zero, then only the
                               first ``max_errors`` error messages are printed
        """
        self.function = function
        self.max_errors = max_errors
        self.errors = 0

    def __call__(self, *args, **kwds):
        """
        Calls ``self.function`` with the given arguments and keywords, and
        returns its value - or if the call throws an exception, returns None.

        If is ``self.max_errors`` is `0`, all the exceptions are reported,
        otherwise just the first ``self.max_errors`` are.
        """
        try:
            return self.function(*args, **kwds)
        except Exception as e:
            args = (class_name.class_name(e),) + e.args

        self.errors += 1
        if self.max_errors < 0 or self.errors <= self.max_errors:
            log.error(str(args))

        elif self.errors == self.max_errors + 1:
            log.error('Exceeded max_errors of %d', self.max_errors)
