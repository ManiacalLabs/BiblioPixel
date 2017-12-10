import json, tempfile
from bibliopixel.project import project
from .. mark_tests import SKIP_LONG_TESTS


def make(data, run_start=not SKIP_LONG_TESTS):
    if '{' in data:
        fp = tempfile.NamedTemporaryFile(mode='w')
        fp.write(data)
        fp.seek(0)
        data = fp.name

    pr = project.read_project(data)
    animation = pr.make_animation()
    if run_start:
        animation.start()

    return animation
