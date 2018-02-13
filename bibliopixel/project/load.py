from . import aliases
import loady, os
from .. util import json

guess_name = loady.importer.guess_name
CACHE = os.path.expanduser('~/.bibliopixel/code_cache')
ROOT_FILE = None


def data(name, use_json=True):
    if not name:
        return {}

    try:
        return json.loads(name)
    except:
        return loady.data.load(name, use_json)


def code(name, python_path=None):
    return name and loady.code.load_code(name, python_path)


def module(name, python_path=None):
    return name and loady.code.load_module(name, python_path)


def extender(path):
    parts = [os.getcwd()] + path.split(':')
    return parts and loady.sys_path.extender(':'.join(parts))


def load_if_filename(s):
    if isinstance(s, str) and (s.endswith('.yml') or s.endswith('.json')):
        if not os.path.isabs(s):
            s = os.path.join(os.path.dirname(ROOT_FILE), s)

        return json.load(s)
