from bibliopixel.main import main, run
from .. mark_tests import SKIP_LONG_TESTS


def make(name, is_json=True, run_start=not SKIP_LONG_TESTS):
    args = main.get_args(['none', 'run'])
    animation = run.make_animation(name, is_json, args)
    if run_start:
        animation.start()
    return animation
