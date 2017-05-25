import subprocess


def execute(*cmd, **kwds):
    try:
        return subprocess.check_output(cmd, **kwds)
    except Exception as e:
        raise ValueError('Couldn\'t execute "%s", errorcode=%s' % (
                         ' '.join(cmd), getattr(e, 'returncode', None)))


def pull(path=None):
    execute('git', 'pull', cwd=path)


def clone(url, branch, path):
    execute('git', 'clone', url, '-b', branch, path)


def reset(commit, path):
    execute('git', 'reset', '--hard', commit, cwd=path)
