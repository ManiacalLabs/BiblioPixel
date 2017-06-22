import copy

from . aliases import resolve_aliases

DEFAULTS = {
    'driver': {
        'typename': 'bibliopixel.drivers.SimPixel.SimPixel',
        'num': 1024
    },

    'layout': {
        'typename': 'bibliopixel.layout.matrix.Matrix',
        'width': 32,
        'height': 32,
    },

    'animation': {
        'typename': 'BiblioPixelAnimations.matrix.bloom.Bloom'
    },

    'maker': {},
    'run': {},
}

SECTIONS = tuple(sorted(DEFAULTS.keys()))


def merge(default, *others):
    result = copy.deepcopy(default)
    for o in others:
        for k, v in o.items():
            result[k].update(v)

    return result


def apply_defaults(desc):
    return merge(DEFAULTS, resolve_aliases(desc))
