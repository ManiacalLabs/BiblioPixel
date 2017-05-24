import sys


def append_path(path):
    sys.path.append(path)


def extend_paths(paths):
    if paths:
        try:
            paths = paths.split(':')
        except:
            pass

        for path in paths:
            append_path(path)
