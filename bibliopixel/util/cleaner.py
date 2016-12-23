import contextlib


@contextlib.contextmanager
def cleaner(x):
    """A context manager which calls x.cleanup()."""
    try:
        yield
    finally:
        x.cleanup()
