import loady, json, tempfile
from bibliopixel.project import project
from .. mark_tests import SKIP_LONG_TESTS


def make(data, run_start=not SKIP_LONG_TESTS):
    if '{' in data:
        with tempfile.NamedTemporaryFile(mode='w') as fp:
            fp.write(data)
            fp.seek(0)
            print('!!!', fp.name)
            animation = project.read_project(fp.name, threaded=None)
    else:
        animation = project.read_project(data, threaded=None)

    if run_start:
        animation.start()
    return animation
