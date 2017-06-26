import contextlib, gitty, json, os.path, shutil


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
    url = gitty.raw.raw(fname)
    response = requests.get(url)
    if response.ok:
        response.read = lambda: response.text
        return response

    raise IOError('%s: Can\'t open URL %s' % (response.status_code, url))


@contextlib.contextmanager
def remove_on_failure(dirname, remove=True):
    """Tries to create and fill a directory, removes it on failure."""
    os.makedirs(dirname)
    try:
        yield
    except:
        if remove:
            shutil.rmtree(dirname)
        raise
