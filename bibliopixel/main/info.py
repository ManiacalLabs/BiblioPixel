"""
Print information about BiblioPixel
"""

DESCRIPTION = """
Prints the versions of BiblioPixel's dependencies, and the platform
that the program is running on.
"""

import datetime, os, platform, sys
import bibliopixel, BiblioPixelAnimations, loady
from bibliopixel.util import log

NONE = '(none)'


def run(args):
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    log.printer('Timestamp:     ', now)
    log.printer('Python version:', platform.python_version())
    log.printer('Platform:      ', platform.platform())
    log.printer('`bp` path:     ', sys.argv[0])
    log.printer('Library path:  ', os.path.dirname(bibliopixel.__file__))

    log.printer()
    log.printer('Dependencies:')
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

        log.printer('    %s: version %s, git commit: %s, git tag %s' %
                    (module.__name__, version, commit_id, tag))


def set_parser(parser):
    parser.set_defaults(run=run)
