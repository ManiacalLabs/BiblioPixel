import os, shutil, subprocess, sys
from .. util import files
from . import git

GIT_INTRO = '//git/'
CACHE_FILES = os.path.expanduser('~/.bibliopixel_py')

CHECKOUT_ADDRESS = {
    'git': 'git@{provider}:{user}/{project}.git',
    'https': 'https://{provider}/{user}/{project}.git',
}


def split_query(url):
    """Split a query looking like base?x=a&condition&z=c"""

    def split_in_two(s, sep):
        return (s.split(sep, 2) + ['', ''])[:2]

    base, query = split_in_two(url, '?')
    parts = query and query.split('&')
    assignments = dict(split_in_two(p, '=') for p in parts)
    assert len(assignments) == len(parts), 'Duplicate query names in ' + url
    return base, assignments


def get_library_path(base, commit=None, branch='master'):
    # TODO: sanitize base and branch for legal directory characters.
    sub = ['__commits', commit] if commit else [branch]
    return os.path.join(CACHE_FILES, base, *sub)


def commit_id_to_path(base, branch='master', commit=None, transport='https'):
    path = get_library_path(base, commit=commit, branch=branch)

    if os.path.exists(path):
        if not commit:
            git.pull(path)

    else:
        with files.remove_on_failure(path):
            provider, user, project = base.split('/')
            url = CHECKOUT_ADDRESS[transport].format(**locals())
            git.clone(url, branch, path)
            if commit:
                git.reset(commit, path)

    return path


def resolve_one_path(path):
    """If the path starts with //git, try to load it from a git repo"""
    if path.startswith(GIT_INTRO):
        url = path[len(GIT_INTRO):]
        base, assignments = split_query(url)
        return commit_id_to_path(base, **assignments)

    return path


def resolve_paths(paths):
    """Resolve paths to either git or the file system.
    """
    try:
        paths = (paths or '').split(':')
    except:
        pass

    return [resolve_one_path(p) for p in paths]


def extend_sys_path(paths):
    sys.path.extend(resolve_paths(paths))


def clear_cache():
    shutil.rmtree(CACHE_FILES, ignore_errors=True)
