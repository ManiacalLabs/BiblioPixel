import copy

DEFAULTS = {
    'driver': {
        'typename': 'bibliopixel.drivers.SimPixel.DriverSimPixel',
        'num': 1024
    },

    'led': {
        'typename': 'bibliopixel.led.matrix.LEDMatrix',
        'width': 32,
        'height': 32,
    },

    'animation': {
        'typename': 'BiblioPixelAnimations.matrix.bloom.Bloom'
    },

    'maker': {},
    'run': {},
}


def apply_defaults(desc):
    result = copy.deepcopy(DEFAULTS)
    for k, v in desc.items():
        if isinstance(v, str):
            result[k]['typename'] = v
        else:
            result[k].update(v)

    return result
