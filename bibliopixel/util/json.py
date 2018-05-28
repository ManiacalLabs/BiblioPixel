import json, os, sys, yaml, io

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
    if isinstance(s, io.IOBase):  # is file stream
        s = s.read()  # convert to raw str

    def fix(d):
        if isinstance(d, dict):
            return {str(k): fix(v) for k, v in d.items()}
        if isinstance(d, list):
            return [fix(i) for i in d]
        assert isinstance(d, (int, float, bool, str))
        return d

    yaml_error = None
    try:
        res = fix(yaml.load(s))
    except (yaml.scanner.ScannerError, yaml.parser.ParserError) as e:
        yaml_error = str(e).replace('<unicode string>', filename)

    if yaml_error:
        raise Exception(yaml_error)

    return res


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
    open_local = False
    if isinstance(file, str):
        fp = open(file)
        filename = file
        open_local = True
    else:
        fp = file
        filename = getattr(fp, 'name', '')

    try:
        return loads(fp.read(), filename)

    except Exception as e:
        e.args = ('There was an error in the data file', filename) + e.args
        raise
    finally:
        if open_local:
            fp.close()
