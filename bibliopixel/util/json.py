import json, os, sys, yaml

# Allow open to be patched for tests.
open = __builtins__['open']


def dumps(data, **kwds):
    """
    Dumps data into a nicely formatted JSON string.

    :param dict data: a dictionary to dump
    :param kwds: keywords to pass to json.dumps
    :returns: a string with formatted data
    :rtype: str
    """
    return json.dumps(data, indent=4, sort_keys=True, **kwds)


def loads(s, filename=''):
    if filename.endswith('.yml'):
        return yaml.load(s)
    return json.loads(s)


def dump(data, file=sys.stdout, **kwds):
    """
    Dumps data as nicely formatted JSON string to a file or file handle

    :param dict data: a dictionary to dump
    :param file: a filename or file handle to write to
    :param kwds: keywords to pass to json.dump
    """
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


def load(file):
    """
    Loads not only JSON files but also YAML files ending in .yml.

    :param file: a filename or file handle to read from
    :returns: the data loaded from the JSON or YAML file
    :rtype: dict
    """
    if isinstance(file, str):
        fp = open(file)
        filename = file
    else:
        fp = file
        filename = getattr(fp, 'name', '')

    try:
        return loads(fp.read(), filename)

    except Exception as e:
        e.args = ('There was a error in the data file', filename) + e.args
        raise
