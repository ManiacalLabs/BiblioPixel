import copy, json, tempfile
from bibliopixel.project import load, project
from .. mark_tests import SKIP_LONG_TESTS


def make(data, run_start=not SKIP_LONG_TESTS):
    if '{' in data:
        fp = tempfile.NamedTemporaryFile(mode='w')
        fp.write(data)
        fp.seek(0)
        data = fp.name

    project_data = load.data(data)
    pr, _ = project.project(copy.deepcopy(project_data))
    animation = pr.animation
    if run_start:
        animation.start()

    return animation
