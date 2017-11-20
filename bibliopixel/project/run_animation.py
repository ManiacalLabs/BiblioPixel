from .. util import class_name
from . import attributes
from .. animation import runner


class RunAnimation:
    def __init__(self, layout, *, run, animation):
        self.layout = layout
        self.run = run
        self.animation = animation

    @staticmethod
    def fix_children(desc):
        run = desc.get('run', {})
        desc['run'] = runner.Runner(**run)

    @staticmethod
    def children(desc):
        yield 'animation', desc

    def runnable_animation(self):
        self.animation.set_runner(self.run)
        return self.animation


def fix(desc):
    if isinstance(desc, str) or 'animation' not in desc:
        desc = {'animation': desc}

    run = desc.pop('run', {})
    datatype = run.pop('typename', None)
    assert not datatype, datatype
    animation = desc.pop('animation', None) or {}

    desc['run_animation'] = {
        'datatype': RunAnimation,
        'run': run,
        'animation': animation}

    return desc
