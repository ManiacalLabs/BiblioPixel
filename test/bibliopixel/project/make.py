import tempfile
from bibliopixel.project import project
from bibliopixel.util import json
from .. mark_tests import SKIP_LONG_TESTS


def make(data, run_start=not SKIP_LONG_TESTS):
    if '{' in data:
        fp = tempfile.NamedTemporaryFile(mode='w')
        fp.write(data)
        fp.seek(0)
        data = fp.name

    desc = json.load(data)
    pr, desc = project.project(desc)
    animation = pr.animation
    if run_start:
        animation.start()

    return animation
