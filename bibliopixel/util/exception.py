import contextlib, traceback


@contextlib.contextmanager
def add(*args):
    """
    A context manager that appends arguments to any exception thrown

    :param args: Arguments to be appended to the ``.args`` attribute of any
                 exception that is thrown while the context manager is active
    """
    try:
        yield
    except Exception as e:
        e.args = args + e.args
        raise


def report(function, *args, **kwds):
    """Run a function, catch, report and discard exceptions"""
    try:
        function(*args, **kwds)
    except Exception:
        traceback.print_exc()
