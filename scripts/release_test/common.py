import os, subprocess, sys
import features

ROOT = os.path.dirname(__file__)
printer = print  # noqa: T001
VERBOSE = False
USE_PROMPT = True


def prompt(prompt):
    if USE_PROMPT:
        input('\n' + prompt + ': ')


def test_prompt(name):
    prompt('--> Press return to start %s test' % name)


def execute(*args):
    kwds = {
        'stdout': subprocess.PIPE,
        'shell': features.IS_WINDOWS}

    if VERBOSE:
        printer('$', *args)
        printer()
        po = subprocess.Popen(args, stderr=subprocess.STDOUT, **kwds)
        for line in po.stdout:
            printer(line.decode(), end='')
        if po.returncode:
            sys.exit(po.returncode)

    else:
        po = subprocess.Popen(args, stderr=subprocess.PIPE, **kwds)
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
