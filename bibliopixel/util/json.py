import json, sys
loads = json.loads

# Allow open to be patched for tests.
open = __builtins__['open']


def dump(data, file=sys.stdout, **kwds):
    """Dump JSON data to a file or file handle"""
    def dump(fp):
        return json.dump(data, fp, indent=4, sort_keys=True, **kwds)

    if not isinstance(file, str):
        return dump(file)

    with open(file, 'w') as fp:
        return dump(fp)


def load(file):
    """Load JSON data from a file or file handle"""
    if not isinstance(file, str):
        return json.load(file)

    with open(file) as fp:
        return json.load(fp)
