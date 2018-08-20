import collections, json, os, sys, yaml

# Allow open to be patched for tests.
open = __builtins__['open']

ALWAYS_LOAD_YAML, ALWAYS_DUMP_YAML = True, True


def dumps(data, use_yaml=None, safe=True, **kwds):
    """
    Dumps data into a nicely formatted JSON string.

    :param dict data: a dictionary to dump
    :param kwds: keywords to pass to json.dumps
    :returns: a string with formatted data
    :rtype: str
    """
    if use_yaml is None:
        use_yaml = ALWAYS_DUMP_YAML

    if use_yaml:
        dumps = yaml.safe_dump if safe else yaml.dump
    else:
        dumps = json.dumps
        kwds.update(indent=4, sort_keys=True)
        if not safe:
            kwds.update(default=repr)
    return dumps(data, **kwds)


def dump(data, file=sys.stdout, use_yaml=None, **kwds):
    """
    Dumps data as nicely formatted JSON string to a file or file handle

    :param dict data: a dictionary to dump
    :param file: a filename or file handle to write to
    :param kwds: keywords to pass to json.dump
    """
    if use_yaml is None:
        use_yaml = ALWAYS_DUMP_YAML

    def dump(fp):
        if use_yaml:
            yaml.safe_dump(data, stream=fp, **kwds)
        else:
            json.dump(data, fp, indent=4, sort_keys=True, **kwds)

    if not isinstance(file, str):
        return dump(file)

    if os.path.isabs(file):
        parent = os.path.dirname(file)
        if not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

    with open(file, 'w') as fp:
        return dump(fp)


def loads(s, use_yaml=None, filename=''):
    if use_yaml is None:
        use_yaml = ALWAYS_LOAD_YAML

    if not (filename.endswith('.yml') or use_yaml):
        return json.loads(s)

    def fix(d):
        if isinstance(d, dict):
            return {str(k): fix(v) for k, v in d.items()}
        if isinstance(d, list):
            return [fix(i) for i in d]
        if not isinstance(d, (int, float, bool, str, type(None))):
            raise ValueError('Wrong type %s' % type(d))
        return d

    return fix(yaml.safe_load(s))


def load(file, use_yaml=None):
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
        return loads(fp.read(), use_yaml, filename)

    except Exception as e:
        e.args = ('There was a error in the data file', filename) + e.args
        raise
