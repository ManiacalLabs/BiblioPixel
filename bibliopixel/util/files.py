import json, os.path


def opener(fname, *args):
    return open(os.path.expanduser(fname), *args)


def read_json(filename):
    try:
        return json.load(opener(filename))
    except:
        return json.loads(filename)
