import json, os, sys, yaml

# Allow open to be patched for tests.
open = __builtins__['open']


def dumps(data, **kwds):
    return json.dumps(data, indent=4, sort_keys=True, **kwds)


def loads(s, filename=''):
    if filename.endswith('.yml'):
        return yaml.load(s)
    return json.loads(s)


def dump(data, file=sys.stdout, **kwds):
    """Dump JSON data to a file or file handle"""
    def dump(fp):
        json.dump(data, fp, indent=4, sort_keys=True, **kwds)

    if not isinstance(file, str):
        return dump(file)

    if os.path.isabs(file):
        parent = os.path.dirname(file)
        if not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

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
