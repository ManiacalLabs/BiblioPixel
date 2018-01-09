"""
Print information about BiblioPixel
"""

DESCRIPTION = """
Prints the versions of BiblioPixel's dependencies, and the platform
that the program is running on.
"""

import datetime, os, platform, sys
import bibliopixel, BiblioPixelAnimations, loady

NONE = '(none)'


def run(args):
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    print('Timestamp:     ', now)
    print('Python version:', platform.python_version())
    print('Platform:      ', platform.platform())
    print('`bp` path:     ', sys.argv[0])
    print('Library path:  ', os.path.dirname(bibliopixel.__file__))

    print()
    print('Dependencies:')
    for module in bibliopixel, BiblioPixelAnimations, loady:
        path = os.path.dirname(module.__file__)
        parent = os.path.dirname(path)

        try:
            fp = open(os.path.join(path, 'VERSION'))
        except:
            try:
                fp = open(os.path.join(parent, 'VERSION'))
            except:
                fp = None

        version = fp.read().strip() if fp else NONE

        try:
            import git
            repo = git.Repo(os.path.dirname(path))
        except:
            commit_id = tag = NONE
        else:
            commit_id = repo.commit('HEAD').hexsha[:7]
            tag = repo.tags[-1].name if repo.tags else '(none)'

        print('    %s: version %s, git commit: %s, git tag %s' %
              (module.__name__, version, commit_id, tag))


def set_parser(parser):
    parser.set_defaults(run=run)
