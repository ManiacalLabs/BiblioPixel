from .. util import class_name
from . import attributes
from .. animation import runner


class RunAnimation:
    def __init__(self, layout, *, run, animation):
        self.layout = layout
        self.run = run
        self.animation = animation

    @staticmethod
    def children(desc):
        yield 'run', desc
        yield 'animation', desc

    def runnable_animation(self):
        self.animation.set_runner(self.run)
        return self.animation


def fix(desc):
    if isinstance(desc, str) or 'animation' not in desc:
        desc = {'animation': desc}

    run = desc.pop('run', class_name.class_name(runner.Runner))
    animation = desc.pop('animation', None) or {}

    desc['run_animation'] = {
        'typename': class_name.class_name(RunAnimation),
        'run': run,
        'animation': animation}

    return desc
