import os, subprocess

try:
    import git

except ImportError:

    def _execute(*cmd, **kwds):
        try:
            return subprocess.check_output(cmd, **kwds)
        except Exception as e:
            raise ValueError('Couldn\'t execute "%s", errorcode=%s' % (
                             ' '.join(cmd), getattr(e, 'returncode', None)))

    def pull(path, branch):
        _execute('git', 'pull', 'origin', branch, cwd=path)

    def clone(url, branch, path, commit):
        _execute('git', 'clone', url, '-b', branch, path)
        if commit:
            _execute('git', 'reset', '--hard', commit, cwd=path)

else:

    def pull(path, branch):
        repo = git.Repo(path)
        repo.remote().pull(repo.active_branch)

    def clone(url, branch, path, commit):
        repo = git.Repo.init(path)
        origin = repo.create_remote('origin', url)
        origin.fetch()
        origin.pull(branch)

        if commit:
            repo.head.reset(commit, index=True, working_tree=True)
