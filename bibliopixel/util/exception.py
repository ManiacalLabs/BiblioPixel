import contextlib


@contextlib.contextmanager
def add(*args):
    try:
        yield
    except Exception as e:
        e.args = args + e.args
        raise
