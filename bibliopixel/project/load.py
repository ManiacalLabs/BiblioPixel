from . import aliases
import loady, os
from .. util import data_file, log

guess_name = loady.importer.guess_name
CACHE = os.path.expanduser('~/.bibliopixel/code_cache')
ROOT_FILE = None


def data(name, use_json=True):
    if not name:
        return {}

    try:
        return data_file.loads(name)
    except:
        return loady.data.load(name, use_json)


def code(name, python_path=None):
    return name and loady.code.load_code(name, python_path, recurse=True)


def module(name, python_path=None):
    return name and loady.code.load_module(name, python_path)


def extender(path):
    parts = [os.getcwd()]
    if path:
        parts.extend(path.split(':'))

    missing = [p for p in parts if not os.path.exists(p)]
    if missing:
        msg = ('This "path" entry does not exist' if len(missing) == 1
               else 'These "path" entries do not exist')
        m2 = ['"%s"' % p for p in missing]
        log.warning('%s: %s', msg, ', '.join(m2))
        parts = [p for p in parts if os.path.exists(p)]

    return parts and loady.sys_path.extender(':'.join(parts))


def load_if_filename(s):
    if isinstance(s, str) and (s.endswith('.yml') or s.endswith('.json')):
        if ROOT_FILE and not os.path.isabs(s):
            s = os.path.join(os.path.dirname(ROOT_FILE), s)

        return data_file.load(s)
