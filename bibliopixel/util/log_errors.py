from .. util import class_name, log


class LogErrors:
    """
    Wraps a function call to catch and report exceptions.
    """

    def __init__(self, function, errors):
        """
        :param function: the function to wrap
        :param errors: either a number, indicating how many errors to report
           before ignoring them, or one of these strings:
           'raise', meaning to raise an exception
           'ignore', meaning to ignore all errors
           'report', meaning to report all errors
        """
        assert isinstance(errors, int) or errors in (
            'raise', 'ignore', 'report')
        self.function = function
        self.errors = errors
        self.error_count = 0

    def __call__(self, *args, **kwds):
        """
        Calls `self.function` with the given arguments and keywords, and
        returns its value - or if the call throws an exception, returns None.
        """
        try:
            return self.function(*args, **kwds)
        except Exception as e:
            self.error_count += 1
            if self.errors == 'raise':
                raise
            if self.errors == 'ignore':
                return
            args = (class_name.class_name(e),) + e.args

        if self.errors == 'report' or self.error_count <= self.errors:
            log.error(str(args))

        elif self.error_count == self.errors + 1:
            log.error('Exceeded errors of %d', self.errors)
