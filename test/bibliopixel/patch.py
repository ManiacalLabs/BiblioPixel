from bibliopixel.project import importer
import contextlib


@contextlib.contextmanager
def patch(object, name, value):
    saved_value = getattr(object, name)
    setattr(object, name, value)
    try:
        yield
    finally:
        setattr(object, name, saved_value)
