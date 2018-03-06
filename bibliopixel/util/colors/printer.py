from .. import log
from . import names


def printer(colors, use_hex=False):
    if not colors:
        return

    # Try to flatten the list

    try:
        colors[0][0]
    except:
        assert len(colors) % 3 == 0
        colors = zip(*([iter(colors)] * 3))

    for i, color in enumerate(colors):
        log.printer('%2d:' % i, names.color_to_name(color, use_hex))
