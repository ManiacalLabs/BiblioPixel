import copy
from .importer import import_symbol

ALIASES = {
    'driver': {
        'apa102': 'bibliopixel.drivers.APA102.APA102',
        'dummy': 'bibliopixel.drivers.dummy_driver.Dummy',
        'hue': 'bibliopixel.drivers.hue.Hue',
        'image': 'bibliopixel.drivers.image_sequence.ImageSequence',
        'lpd8806': 'bibliopixel.drivers.LPD8806.LPD8806',
        'network': 'bibliopixel.drivers.network.Network',
        'network_udp': 'bibliopixel.drivers.network.NetworkUDP',
        'serial': 'bibliopixel.drivers.serial.Serial',
        'simpixel': 'bibliopixel.drivers.SimPixel.SimPixel',
        'ws2801': 'bibliopixel.drivers.WS2801.WS2801',
    },

    'led': {
        'circle': 'bibliopixel.led.circle.Circle',
        'cube': 'bibliopixel.led.cube.Cube',
        'matrix': 'bibliopixel.led.matrix.Matrix',
        'pov': 'bibliopixel.led.pov.POV',
        'strip': 'bibliopixel.led.strip.Strip',
    },

    'animation': {
        'off': 'bibliopixel.animation.off.OffAnim',
        'matrix_calibration':
        'bibliopixel.animation.tests.MatrixCalibrationTest',
        'matrix_test': 'bibliopixel.animation.tests.MatrixChannelTest',
        'receiver': 'bibliopixel.animation.receiver.BaseReceiver',
        'sequence': 'bibliopixel.animation.Sequence',
        'strip_test': 'bibliopixel.animation.tests.StripChannelTest',
    },
}


def fill_typename(desc, key):
    if isinstance(desc, str):
        return fill_typename({'typename': desc}, key)

    typename = desc.get('typename')
    if typename:
        desc['typename'] = ALIASES[key].get(typename, typename)

    return desc


def resolve_aliases(project):
    result = copy.deepcopy(project)
    for key in ALIASES:
        if key in result:
            result[key] = fill_typename(result[key], key)
    return result
