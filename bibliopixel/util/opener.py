import os.path


def opener(fname, *args):
    return open(os.path.expanduser(fname), *args)
