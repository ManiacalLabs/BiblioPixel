import os, subprocess, sys
import features

ROOT = os.path.dirname(__file__)
printer = print  # noqa: T001


def execute(*args, verbose=False):
    if verbose:
        printer('$', *args)
    cwd = os.path.dirname(os.path.dirname(ROOT))
    po = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd,
        shell=features.IS_WINDOWS)
    stdout, stderr = po.communicate()
    if po.returncode:
        printer()
        printer('*** ERROR ***')
        printer(stderr.decode())
        printer()
        printer('--------------')
        printer()
        printer('stdout follows:')
        printer()
        printer('--------------')
        printer(stdout.decode())
        printer('--------------')
        sys.exit(po.returncode)


def run_project(*projects, flag=None):
    projects = [make_project(p) for p in projects]
    if flag:
        projects.append(flag)
    execute('bp', '-v', *projects)


def make_project(project):
    return os.path.join(ROOT, 'projects', project)
