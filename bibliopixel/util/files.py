import json, os.path

GITHUB_BASE = 'github.com'
GITHUB_RAW = 'raw.githubusercontent.com'


def munge_url(url):
    if not (url.endswith('.json') and ('://%s/' % GITHUB_BASE) in url):
        return url

    parts = url.split('/')
    assert parts[0] in 'https:', 'http:'
    assert not parts[1]
    assert parts[2] == GITHUB_BASE
    assert parts[5] == 'blob'
    parts[2] = GITHUB_RAW
    parts.pop(5)
    return '/'.join(parts)


def opener(fname, mode='r', *args, **kwds):
    requests = None
    if ':' in fname:
        try:
            import requests
        except:
            pass

    if not requests:
        return open(os.path.expanduser(fname), mode, *args, **kwds)

    assert not (set(mode) & set('wax')), 'Cannot write to remote file ' + fname
    url = munge_url(fname)
    response = requests.get(url)
    if response.ok:
        response.read = lambda: response.text
        return response

    raise IOError('%s: Can\'t open URL %s' % (response.status_code, url))


def read_json(s, is_filename=True):
    data = opener(s).read() if is_filename else s

    try:
        return json.loads(data)
    except ValueError as e:
        e.args = ['%s\nin filename %s' % (e.args[0], s)]
        raise
