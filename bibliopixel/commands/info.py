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
from bibliopixel.util.platform import Platform

NONE = '(none)'
MODULES = bibliopixel, BiblioPixelAnimations, loady


def run(args):
    platform = Platform()

    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    bp_path = sys.argv[0]
    library_path = os.path.dirname(bibliopixel.__file__)
    dependencies = '\n'.join(_dependency(m) for m in MODULES)
    if platform.cpuinfo:
        cpuinfo = CPUINFO % '\n'.join(platform.cpuinfo)
    else:
        cpuinfo = ''

    log.printer(MESSAGE.format(**locals()))


def add_arguments(parser):
    parser.set_defaults(run=run)


def _dependency(module):
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

    return ('    %s: version %s, git commit: %s, git tag %s' %
            (module.__name__, version, commit_id, tag))


MESSAGE = """\
Timestamp:        {now}
Python version:   {platform.python_version}
`bp` path:        {bp_path}
Library path:     {library_path}

Platform:         {platform.platform}
Platform version: {platform.platform_version}
Platform release: {platform.release}

Dependencies:
{dependencies}
{cpuinfo}"""

CPUINFO = """
cpuinfo
--------------------------------------------------------------------------------
%s
--------------------------------------------------------------------------------
"""
