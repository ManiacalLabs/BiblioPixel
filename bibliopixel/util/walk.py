import os


def walk(roots):
    if isinstance(roots, str):
        roots = [roots]

    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            for f in filenames:
                yield root, os.path.join(dirpath, f)


def walk_suffix(roots, suffixes):
    for root, filename in walk(roots):
        if any(filename.endswith(s) for s in suffixes):
            yield root, filename
