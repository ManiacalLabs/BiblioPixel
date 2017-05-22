import contextlib, sys


@contextlib.contextmanager
def replace(new_path):
    old_path, sys.path = sys.path, new_path

    try:
        yield
    finally:
        sys.path = old_path


def extend(path):
    try:
        path = (path or '').split(':')
    except:
        path = list(path)

    return replace(sys.path + path)
