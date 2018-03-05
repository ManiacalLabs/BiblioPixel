import tempfile
from bibliopixel.project import project
from bibliopixel.util import json
from .. mark_tests import SKIP_LONG_TESTS


def make_project(data):
    if isinstance(data, dict):
        desc = data

    elif not isinstance(data, str):
        raise ValueError('Cannot understand data %s' % data)

    else:
        if '{' in data:
            fp = tempfile.NamedTemporaryFile(mode='w')
            fp.write(data)
            fp.seek(0)
            data = fp.name

        desc = json.load(data)

    return project.project(desc)


def make(data, run_start=not SKIP_LONG_TESTS):
    project = make_project(data)

    if run_start:
        project.animation.start()

    return project.animation
