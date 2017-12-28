import json, sys, yaml


# Allow open to be patched for tests.
open = __builtins__['open']


def loads(s, filename=''):
    if filename.endswith('.yml'):
        return yaml.load(s)
    return json.loads(s)


def dump(data, file=sys.stdout, **kwds):
    """Dump JSON data to a file or file handle"""
    def dump(fp):
        return json.dump(data, fp, indent=4, sort_keys=True, **kwds)

    if not isinstance(file, str):
        return dump(file)

    with open(file, 'w') as fp:
        return dump(fp)


def load(filename):
    """
    Loads not only JSON files but also YAML files ending in .yml.
    """
    if isinstance(filename, str):
        fp = open(filename)
    else:
        fp = filename
        filename = getattr(fp, 'name', '')

    try:
        return loads(fp.read(), filename)

    except Exception as e:
        e.args = ('There was a error in the data file', filename) + e.args
        raise
