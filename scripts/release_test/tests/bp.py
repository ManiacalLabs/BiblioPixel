import common
from unittest import mock

FEATURES = 'browser',
MESSAGE = 'Press return to start bp tests.'
ERROR = """For key=color value=wombat
Don't understand color name "wombat"

A Color can be initialized with:

* A list of three numbers: [0, 0, 0] or [255, 0, 255].
* A single number which represents a brightness/gray level: 0, 255, 127
* A string:  "red", "yellow", "gold" naming a color from ...colors.COLORS.

All numbers must be in the range [0, 256) - 0 <= x < 256"""


def run():
    common.run_project('bp.yml', flag='-s')
    common.run_project('bp.yml+{animation: {color: green}}',
                       flag='--simpixel=https://www.simpixel.io')
    common.run_project('bp.yml+{animation: {color: blue}}')

    results = []

    def printer(*args, **kwds):
        results.append(' '.join(args))

    with mock.patch('common.printer', side_effect=printer):
        common.run_project('bp.yml+{animation: {color: wombat}}')

    if ERROR not in ''.join(results):
        common.printer()
        common.printer('ERROR: expected error not found')
        common.printer(''.join(results))
