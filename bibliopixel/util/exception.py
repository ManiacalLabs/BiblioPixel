import contextlib


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
